from __future__ import annotations

import sys
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_case import parse_front_matter, validate_case  # noqa: E402
from build_case_index import build_index  # noqa: E402


class SkillTests(unittest.TestCase):
    def test_case_001_validates(self) -> None:
        errors = validate_case(SKILL_ROOT / "examples" / "case_001_yao_interview")
        self.assertEqual(errors, [])

    def test_case_002_validates(self) -> None:
        errors = validate_case(SKILL_ROOT / "examples" / "case_002_zisha_auction_pilot")
        self.assertEqual(errors, [])

    def test_index_contains_two_cases(self) -> None:
        index = build_index(SKILL_ROOT)
        self.assertEqual(index["case_count"], 2)
        self.assertEqual([case["case_id"] for case in index["cases"]], ["CASE-001", "CASE-002"])

    def test_front_matter_parser(self) -> None:
        data = parse_front_matter("---\ncase_id: CASE-001\nasset_type: case_card\n---\n# Title\n")
        self.assertEqual(data["case_id"], "CASE-001")
        self.assertEqual(data["asset_type"], "case_card")


if __name__ == "__main__":
    unittest.main()
