#!/usr/bin/env python3
"""Build a deterministic case index from validated case manifests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from validate_case import iter_case_dirs, validate_case


def build_index(skill_root: Path) -> dict:
    cases = []
    for case_dir in iter_case_dirs(skill_root / "examples"):
        manifest_path = case_dir / "manifest.json"
        if not manifest_path.exists():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("status") == "template":
            continue
        errors = validate_case(case_dir)
        if errors:
            raise ValueError("; ".join(errors))
        cases.append(
            {
                "case_id": manifest["case_id"],
                "title": manifest["title"],
                "date": manifest["date"],
                "status": manifest["status"],
                "relationship_types": manifest["relationship_types"],
                "tags": manifest["tags"],
                "path": str(case_dir.relative_to(skill_root)).replace("\\", "/"),
                "public_summary": manifest.get("public_summary", ""),
            }
        )
    cases.sort(key=lambda item: item["case_id"])
    return {"version": "0.1.0", "case_count": len(cases), "cases": cases}


def render(index: dict) -> str:
    return json.dumps(index, ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    skill_root = Path(__file__).resolve().parents[1]
    target = skill_root / "case_index.json"
    try:
        expected = render(build_index(skill_root))
    except ValueError as exc:
        print(f"INDEX BUILD FAILED: {exc}")
        return 1

    if args.check:
        actual = target.read_text(encoding="utf-8") if target.exists() else ""
        if actual != expected:
            print("CASE INDEX OUT OF DATE")
            return 1
        print("CASE INDEX CHECK PASSED")
        return 0

    target.write_text(expected, encoding="utf-8")
    print(f"WROTE {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
