import unittest
from pathlib import Path
import tempfile
import offtec_dev

class TestOfftecDev(unittest.TestCase):
    def test_slugify(self):
        self.assertEqual(offtec_dev.slugify("Meu App Legal"), "meu-app-legal")
    def test_detect_languages_returns_rows(self):
        rows = offtec_dev.detect_languages()
        self.assertTrue(any(row[0] == "Python" for row in rows))

if __name__ == "__main__":
    unittest.main()
