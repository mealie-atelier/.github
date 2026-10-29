"""GitHub detects a code of conduct only from the verbatim Contributor Covenant text."""

import pathlib
import unittest

TEXT = (pathlib.Path(__file__).resolve().parents[1] / "CODE_OF_CONDUCT.md").read_text(encoding="utf-8")


class CodeOfConduct(unittest.TestCase):
    def test_is_the_verbatim_covenant_2_1(self):
        for needle in (
            "# Contributor Covenant Code of Conduct",
            "## Our Pledge",
            "## Our Standards",
            "## Enforcement Guidelines",
            "### 4. Permanent Ban",
            "This Code of Conduct is adapted from the [Contributor Covenant][homepage], version 2.1",
            "Community Impact Guidelines were inspired by [Mozilla's code of conduct enforcement ladder]",
        ):
            self.assertIn(needle, TEXT)

    def test_contact_placeholder_is_filled(self):
        self.assertNotIn("[INSERT CONTACT METHOD]", TEXT)
        self.assertIn("security/advisories/new", TEXT)


if __name__ == "__main__":
    unittest.main()
