#!/usr/bin/env python3
import copy
import importlib.util
import unittest
from pathlib import Path

p = Path(__file__).with_name("validate_cross_client.py")
spec = importlib.util.spec_from_file_location("validate_cross_client", p)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class TestClientValidator(unittest.TestCase):
    def test_expected_policy_inheritance(self):
        data = {"BaseRules": {"AI": {"policyname": "AI", "category": "dler"},
                              "Child": {"parenttag": "AI", "category": "dler"}},
                "CustomRules": {f"X{i}": {"policyname": "DIRECT", "category": "Sukka"}
                                for i in range(28)}}
        bindings = m.expected_bindings(data)
        self.assertEqual(len(bindings), 30)
        self.assertEqual(bindings[1][:2], ("Child", "AI"))

    def test_client_specific_groups(self):
        data = {"policyname": {
            "A": {}, "GLOBAL": {"MihomoOnly": True},
            "B": {}, "Proxies": {"SurgeOnly": True}}}
        names = m.named_groups(data)
        self.assertEqual(names["Mihomo"], ["A", "GLOBAL", "B"])
        self.assertEqual(names["Stash"], ["A", "B"])
        self.assertEqual(names["Egern"], ["A", "B"])
        self.assertEqual(names["Surge"], ["A", "B", "Proxies"])

    def test_drift_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "mismatch at #2"):
            m.compare("Egern", [("a","A"), ("b","WRONG")],
                      [("a","A"), ("b","B")], "rule binding order")

    def test_egern_names(self):
        self.assertEqual(m.egern_filename("LS_Direct", {
            "category": "Loyalsoldier", "remotefile": "direct"}), "direct.yaml")
        self.assertEqual(m.egern_filename("AI", {"category": "dler"}),
                         "external_dler_AI.yaml")

    def test_sections(self):
        text = "[Proxy Group]\nA = select, DIRECT\nB = select, A\n[Rule]\nFINAL,A\n"
        self.assertEqual(m.section_groups(m.section(text, "Proxy Group")), ["A", "B"])


if __name__ == "__main__":
    unittest.main()
