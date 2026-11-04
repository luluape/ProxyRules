#!/usr/bin/env python3
"""Offline tests for fail-closed publishing checks."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import validate_release_guard as guard

class GuardTests(unittest.TestCase):
    def test_rule_count(self):
        self.assertEqual(guard.rule_count("domain_set:\n  - example.com\n", "fixture"), 1)
        with self.assertRaisesRegex(ValueError, "empty rule set"):
            guard.rule_count("domain_set: []\n", "fixture")
        with self.assertRaisesRegex(ValueError, "unsupported keys"):
            guard.rule_count("bad_key:\n  - item\n", "fixture")

    def test_public_placeholder_only(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "Config/Egern").mkdir(parents=True)
            def profile(ipv6, url):
                groups = [{"select": {"name": f"group{i}", "urls": [url] if i == 0 else []}} for i in range(29)]
                rules = [{"rule_set": {"match": "https://example.invalid/rule"}} for _ in range(30)]
                rules.append({"default": {"policy": "选择代理"}})
                import yaml
                return yaml.safe_dump({"ipv6": ipv6, "dns": {"bootstrap": ["system"]}, "policy_groups": groups, "rules": rules}, allow_unicode=True)
            for filename, flag in guard.PROFILES.items():
                (root / "Config/Egern" / filename).write_text(profile(flag, guard.PLACEHOLDER))
            guard.validate_profiles(root)
            filename = "Egern_config.yaml"
            path = root / "Config/Egern" / filename
            path.write_text(profile(True, "https://private.example/secret"))
            with self.assertRaisesRegex(ValueError, "non-placeholder"):
                guard.validate_profiles(root)

    def test_detect_rule_collapse(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            rules = root / "Rules/Egern"
            rules.mkdir(parents=True)
            for i in range(30):
                (rules / f"rule{i}.yaml").write_text("domain_set:\n  - a.example\n")
            original = "domain_set:\n" + "".join(f"  - x{i}.example\n" for i in range(20))
            with patch.object(guard, "git_head", return_value=original), patch.object(guard.subprocess, "run") as git:
                git.return_value.stdout = ""
                with self.assertRaisesRegex(ValueError, "rule collapse"):
                    guard.validate_rules(root, 0.5, 0.7)

if __name__ == "__main__":
    unittest.main()
