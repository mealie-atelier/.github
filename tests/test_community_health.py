"""The community files GitHub counts for the community profile all exist in this repository."""

import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
FILES = [
    "README.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
]


class CommunityHealth(unittest.TestCase):
    def test_every_counted_file_exists_and_is_not_empty(self):
        for name in FILES:
            path = ROOT / name
            self.assertTrue(path.is_file(), f"{name} is missing")
            self.assertGreater(len(path.read_text(encoding="utf-8").strip()), 100, name)

    def test_license_is_mit(self):
        self.assertTrue((ROOT / "LICENSE").read_text(encoding="utf-8").startswith("MIT License"))


if __name__ == "__main__":
    unittest.main()
