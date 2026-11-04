#!/usr/bin/env python3
"""Fail closed before publishing generated ProxyRules artifacts.

Compares Egern rule-set populations with checked-in HEAD and checks public
profiles remain credentials-free. Does not modify repo files or call network.
"""
import argparse
import subprocess
from pathlib import Path

import yaml

PLACEHOLDER = "https://example.invalid/REPLACE_WITH_YOUR_EGERN_SUBSCRIPTION"
PROFILES = {"Egern_config.yaml": True, "Egern_config_no_ipv6.yaml": False}
REQUIRED = (
    "Config/Stash/Stash_config_full.yaml",
    "Config/Loon/Loon_config.lcf",
    "Config/Surge/Surge_config.conf",
)

def read_yaml(content, label):
    try:
        result = yaml.safe_load(content)
    except yaml.YAMLError as exc:
        raise ValueError(f"{label}: invalid YAML: {exc}") from exc
    if not isinstance(result, dict):
        raise ValueError(f"{label}: expected mapping")
    return result

def rule_count(content, label):
    data = read_yaml(content, label)
    allowed = {
        "domain_set", "domain_suffix_set", "domain_keyword_set", "domain_regex_set",
        "domain_wildcard_set", "ip_cidr_set", "ip_cidr6_set", "user_agent_set",
        "url_regex_set", "geoip_set", "asn_set", "dest_port_set", "ssid_set",
        "bssid_set", "cellular_set", "protocol_set", "and_set", "or_set", "not_set",
    }
    extra = set(data).difference(allowed | {"no_resolve"})
    if extra:
        raise ValueError(f"{label}: unsupported keys: {sorted(extra)}")
    count = 0
    for key in allowed.intersection(data):
        items = data[key]
        if not isinstance(items, list):
            raise ValueError(f"{label}: {key} must be list")
        if not all(isinstance(x, (str, int)) for x in items):
            raise ValueError(f"{label}: malformed rule item in {key}")
        count += len(items)
    if count == 0:
        raise ValueError(f"{label}: empty rule set")
    return count

def git_head(root, relative):
    proc = subprocess.run(
        ["git", "show", f"HEAD:{relative}"], cwd=root,
        capture_output=True, check=False,
    )
    if proc.returncode:
        return None
    return proc.stdout.decode("utf-8")

def validate_profiles(root):
    egern = root / "Config/Egern"
    urls_by_profile = {}
    for name, ipv6 in PROFILES.items():
        path = egern / name
        if not path.is_file():
            raise ValueError(f"missing public Egern profile: {path}")
        source = path.read_text(encoding="utf-8")
        doc = read_yaml(source, name)
        if doc.get("ipv6") is not ipv6:
            raise ValueError(f"{name}: incorrect IPv6 setting")
        groups = doc.get("policy_groups")
        rules = doc.get("rules")
        if not isinstance(groups, list) or len(groups) != 29:
            raise ValueError(f"{name}: expected 29 policy groups")
        if not isinstance(rules, list) or len(rules) != 31:
            raise ValueError(f"{name}: expected 31 ordered rules")
        if rules[-1] != {"default": {"policy": "选择代理"}}:
            raise ValueError(f"{name}: missing final default")
        if sum(isinstance(x, dict) and "rule_set" in x for x in rules) != 30:
            raise ValueError(f"{name}: expected 30 remote rules")
        urls = []
        names = []
        for entry in groups:
            if not isinstance(entry, dict) or len(entry) != 1:
                raise ValueError(f"{name}: malformed policy group")
            details = next(iter(entry.values()))
            if not isinstance(details, dict):
                raise ValueError(f"{name}: malformed policy group details")
            names.append(details.get("name"))
            urls.extend(details.get("urls", []))
        if len(set(names)) != 29 or any(not isinstance(n, str) for n in names):
            raise ValueError(f"{name}: duplicate or invalid policy group names")
        if urls != [PLACEHOLDER] or source.count(PLACEHOLDER) != 1:
            raise ValueError(f"{name}: refusing to publish non-placeholder subscription")
        if not isinstance(doc.get("dns"), dict) or doc["dns"].get("bootstrap") != ["system"]:
            raise ValueError(f"{name}: unexpected DNS configuration")
        urls_by_profile[name] = urls
        print(f"PASS public profile: {name}")
    return urls_by_profile

def validate_rules(root, min_ratio, total_ratio):
    folder = root / "Rules/Egern"
    current = sorted(folder.glob("*.yaml"))
    if len(current) < 30:
        raise ValueError(f"only {len(current)} Egern rule files (minimum 30)")
    total_now, total_old, checked = 0, 0, 0
    for path in current:
        relative = path.relative_to(root).as_posix()
        now = rule_count(path.read_text(encoding="utf-8"), relative)
        total_now += now
        old_text = git_head(root, relative)
        if old_text is None:
            continue
        old = rule_count(old_text, "HEAD:" + relative)
        total_old += old
        checked += 1
        if now < old * min_ratio:
            raise ValueError(f"{relative}: rule collapse {old} -> {now} (< {min_ratio:.0%})")
    # Reject deletion of previously tracked Egern rule files.
    result = subprocess.run(
        ["git", "ls-tree", "-r", "--name-only", "HEAD", "Rules/Egern"],
        cwd=root, capture_output=True, text=True, check=True,
    )
    for relative in result.stdout.splitlines():
        if relative.endswith(".yaml") and not (root / relative).is_file():
            raise ValueError(f"tracked Egern rules disappeared: {relative}")
    if checked and total_now < total_old * total_ratio:
        raise ValueError(f"Egern total rule collapse: {total_old} -> {total_now}")
    print(f"PASS Egern rule populations: {len(current)} files, {total_now} rules; baseline {total_old} ({checked} files)")

def validate_outputs(root):
    for relative in REQUIRED:
        path = root / relative
        if not path.is_file() or path.stat().st_size < 100:
            raise ValueError(f"missing or truncated generated output: {relative}")
    mihomo = root / "Config/Mihomo"
    if not any(p.is_file() and p.stat().st_size > 100 for p in mihomo.glob("*.yaml")):
        raise ValueError("missing Mihomo YAML output")
    print("PASS core client outputs: Mihomo, Stash, Loon, Surge")

def run(root, min_ratio=0.5, total_ratio=0.7):
    validate_outputs(root)
    validate_profiles(root)
    validate_rules(root, min_ratio, total_ratio)
    print("PASS: publication guard")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--min-file-ratio", type=float, default=0.5)
    parser.add_argument("--min-total-ratio", type=float, default=0.7)
    args = parser.parse_args()
    if not (0 < args.min_file_ratio <= 1 and 0 < args.min_total_ratio <= 1):
        parser.error("ratios must be in (0,1]")
    try:
        run(args.root.resolve(), args.min_file_ratio, args.min_total_ratio)
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        parser.exit(1, f"BLOCK PUBLICATION: {exc}\n")

if __name__ == "__main__":
    main()
