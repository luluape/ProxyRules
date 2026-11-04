#!/usr/bin/env python3
"""Validate cross-client policy coverage and ordered rule bindings.

Read-only/offline. Base/Rules/RemoteRules.yaml and PolicyConfig.yaml are the
source of truth. Differences in client syntax are handled explicitly.
"""
import argparse
from pathlib import Path
from urllib.parse import urlparse
import re
import sys
import yaml


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load_yaml(path):
    result = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(isinstance(result, dict), f"{path}: YAML root must be mapping")
    return result


def expected_bindings(config):
    parents = dict(config["BaseRules"])
    parents.update(config.get("CustomRules", {}))
    result = []
    for category in ("BaseRules", "CustomRules"):
        for rule_id, spec in config.get(category, {}).items():
            policy = spec.get("policyname")
            if not policy and spec.get("parenttag"):
                policy = parents[spec["parenttag"]].get("policyname")
            require(bool(policy), f"Rule {rule_id}: cannot determine policy")
            result.append((rule_id, policy, spec))
    require(len(result) >= 30, f"Only {len(result)} expected rule bindings")
    return result


def named_groups(policy):
    entries = policy["policyname"]
    require(isinstance(entries, dict), "policyname must be mapping")
    all_names = [n for n, p in entries.items() if not p.get("SurgeOnly")]
    common = [n for n, p in entries.items()
              if not p.get("SurgeOnly") and not p.get("MihomoOnly")]
    surge = [n for n, p in entries.items() if not p.get("MihomoOnly")]
    return {"Mihomo": all_names, "Stash": common, "Loon": common,
            "Surge": surge, "Egern": common}


def compare(name, actual, expected, label):
    if actual != expected:
        mismatch = next((i for i in range(min(len(actual), len(expected)))
                         if actual[i] != expected[i]), min(len(actual), len(expected)))
        a = actual[mismatch] if mismatch < len(actual) else "<missing>"
        b = expected[mismatch] if mismatch < len(expected) else "<missing>"
        raise ValueError(f"{name} {label}: mismatch at #{mismatch+1}: "
                         f"actual={a!r}, expected={b!r} "
                         f"(counts {len(actual)}/{len(expected)})")


def section(text, name):
    marker = f"[{name}]"
    require(marker in text, f"Missing [{name}] section")
    part = text.split(marker, 1)[1]
    return re.split(r"(?m)^\[[^\]\n]+\]\s*$", part, maxsplit=1)[0]


def entries(text):
    return [line.strip() for line in text.splitlines()
            if line.strip() and not line.lstrip().startswith(("#", ";"))]


def section_groups(text):
    return [x.split(" = ", 1)[0].strip()
            for x in entries(text) if " = " in x]


def section_rules(text, client):
    lines = entries(section(text, "Remote Rule" if client == "Loon" else "Rule"))
    if client == "Loon":
        rules = []
        for line in lines:
            require(", policy = " in line, f"Loon remote rule malformed: {line[:100]}")
            url, rest = line.split(", policy = ", 1)
            policy = rest.split(",", 1)[0].strip()
            require(urlparse(url).scheme == "https", f"Loon remote rule not HTTPS: {url[:100]}")
            rules.append(policy)
        return rules
    rules = []
    for line in lines:
        if line.startswith("RULE-SET,"):
            parts = line.split(",", 3)
            require(len(parts) >= 3, f"Surge malformed RULE-SET: {line[:100]}")
            if parts[1] == "LAN":  # Surge's built-in extra LAN match
                require(parts[2] == "DIRECT", "Surge LAN must use DIRECT")
                continue
            require(urlparse(parts[1]).scheme == "https",
                    f"Surge remote rule not HTTPS: {parts[1][:100]}")
            rules.append(parts[2].strip())
    return rules


def egern_filename(rule_id, spec):
    category = spec["category"]
    if category == "Loyalsoldier":
        return Path(spec["remotefile"]).stem + ".yaml"
    if category in ("blackmatrix", "Higanoneko"):
        return f"external_{rule_id}.yaml"
    if category in ("Sukka", "dler", "ADBlock"):
        return f"external_{category}_{rule_id}.yaml"
    raise ValueError(f"Unknown Egern category: {category}")


def validate(root):
    base = root / "Base/Rules"
    bindings = expected_bindings(load_yaml(base / "RemoteRules.yaml"))
    groups = named_groups(load_yaml(base / "PolicyConfig.yaml"))
    ids = [r for r, _, _ in bindings]
    policies = [p for _, p, _ in bindings]
    for client in ("Mihomo", "Stash"):
        path = root / ("Config/Mihomo/mihomo_config_ipv6-1_dns-1_full-0.yaml"
                       if client == "Mihomo" else "Config/Stash/Stash_config_full.yaml")
        doc = load_yaml(path)
        names = [g["name"] for g in doc["proxy-groups"]]
        compare(client, names, groups[client], "policy group order")
        rule_lines = [r for r in doc["rules"] if isinstance(r, str) and r.startswith("RULE-SET,")]
        parsed = [r.split(",", 2)[1:] for r in rule_lines]
        compare(client, [(r, p) for r, p in parsed],
                list(zip(ids, policies)), "rule binding order")
        providers = doc.get("rule-providers")
        require(isinstance(providers, dict), f"{client}: missing rule-providers")
        compare(client, list(providers), ids, "provider order")
        for item in rule_lines:
            require(item.split(",", 2)[1] in providers, f"{client}: unknown provider")
        require(doc["rules"][-2:] == ["GEOIP,CN,直接连接", "MATCH,选择代理"],
                f"{client}: fallback rule order changed")
        print(f"PASS {client}: {len(names)} groups, {len(parsed)} bindings")

    for client, filename in (("Loon", "Config/Loon/Loon_config.lcf"),
                             ("Surge", "Config/Surge/Surge_config.conf")):
        text = (root / filename).read_text(encoding="utf-8")
        names = section_groups(section(text, "Proxy Group"))
        compare(client, names, groups[client], "policy group order")
        actual = section_rules(text, client)
        compare(client, actual, policies, "rule policy order")
        if client == "Loon":
            final = entries(section(text, "Rule"))
            require(final[-2:] == ["GEOIP, CN, 直接连接", "FINAL, 选择代理"],
                    "Loon fallback changed")
        else:
            lines = entries(section(text, "Rule"))
            require(lines[-2:] == ["GEOIP,CN,直接连接", "FINAL,选择代理,dns-failed"],
                    "Surge fallback changed")
        print(f"PASS {client}: {len(names)} groups, {len(actual)} bindings")

    for filename, ipv6 in (("Egern_config.yaml", True),
                           ("Egern_config_no_ipv6.yaml", False)):
        doc = load_yaml(root / "Config/Egern" / filename)
        require(doc.get("ipv6") is ipv6, f"Egern {filename}: incorrect ipv6")
        names = [next(iter(x.values()))["name"] for x in doc["policy_groups"]]
        compare(filename, names, groups["Egern"], "policy group order")
        rules = doc["rules"]
        actual = [(Path(urlparse(x["rule_set"]["match"]).path).name,
                   x["rule_set"]["policy"]) for x in rules if "rule_set" in x]
        expected = [(egern_filename(rule_id, spec), policy)
                    for rule_id, policy, spec in bindings]
        compare(filename, actual, expected, "rule binding order")
        for rule in rules[:-1]:
            url = urlparse(rule["rule_set"]["match"])
            require(url.scheme == "https" and url.hostname == "raw.githubusercontent.com"
                    and url.path.startswith("/luluape/ProxyRules/main/Rules/Egern/"),
                    f"{filename}: invalid rule source URL")
        require(rules[-1] == {"default": {"policy": "选择代理"}},
                f"{filename}: final rule changed")
        print(f"PASS {filename}: {len(names)} groups, {len(actual)} bindings")

    print("PASS: cross-client coverage and rule ordering verified")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        validate(args.root.resolve())
    except (ValueError, KeyError, TypeError, IndexError, OSError, yaml.YAMLError) as exc:
        sys.exit(f"BLOCK PUBLICATION: {exc}")


if __name__ == "__main__":
    main()
