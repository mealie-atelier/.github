"""The org profile screenshot is the same capture the cards and bridge READMEs show."""

import hashlib
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
IMAGE = ROOT / "profile" / "dashboard-light.webp"
README = ROOT / "profile" / "README.md"
# md5 of mealie-atelier-cards assets/screens/dashboard-light.webp at release 0.12.1
CARDS_CAPTURE_MD5 = "f08c183fc53332debc5c44a392279e50"


class ProfileScreenshotTest(unittest.TestCase):
    def test_matches_cards_capture(self):
        digest = hashlib.md5(IMAGE.read_bytes()).hexdigest()
        self.assertEqual(digest, CARDS_CAPTURE_MD5)

    def test_readme_points_at_org_copy(self):
        text = README.read_text(encoding="utf-8")
        self.assertIn("mealie-atelier/.github/main/profile/dashboard-light.webp", text)


if __name__ == "__main__":
    unittest.main()
