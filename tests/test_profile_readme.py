"""The org profile README uses the current feature names."""

import pathlib
import unittest

README = pathlib.Path(__file__).resolve().parents[1] / "profile" / "README.md"


class ProfileReadmeTest(unittest.TestCase):
    def test_uses_discover_not_cook_ideas(self):
        text = README.read_text(encoding="utf-8")
        self.assertNotIn("cook ideas", text.lower())
        self.assertIn("Discover", text)


if __name__ == "__main__":
    unittest.main()
