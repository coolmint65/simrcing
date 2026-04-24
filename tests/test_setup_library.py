"""Tests for the setup library scanner and fuzzy search."""

import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rf2 import setup_library


class LibraryScanTests(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self._make("BMW_M4_GT3/Spa_Francorchamps/quali.svm")
        self._make("BMW_M4_GT3/Spa_Francorchamps/race.svm")
        self._make("BMW_M4_GT3/Monza/quali.svm")
        self._make("Porsche_911_GT3_R/Spa_Francorchamps/wet.svm")
        self._make("Shelby_Cobra/Road_America/baseline.svm")
        self._make("BMW_M4_GT3/Spa_Francorchamps/notes.txt")  # should be ignored

    def _make(self, relpath):
        full = os.path.join(self.tmpdir, *relpath.split("/"))
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as f:
            f.write("[General]\nSymmetric=1\n")

    def test_scan_finds_only_svm(self):
        index = setup_library.scan([self.tmpdir])
        self.assertEqual(index.count(), 5)  # .txt excluded

    def test_car_track_extracted_from_path(self):
        index = setup_library.scan([self.tmpdir])
        by_name = {e.name: e for e in index.entries}
        self.assertEqual(by_name["wet"].car, "porsche 911 gt3 r")
        self.assertEqual(by_name["wet"].track, "spa francorchamps")

    def test_search_car(self):
        index = setup_library.scan([self.tmpdir])
        results = index.search(car_query="BMW M4", track_query="")
        self.assertEqual(len(results), 3)
        for r in results:
            self.assertIn("bmw m4", r.car)

    def test_search_car_and_track(self):
        index = setup_library.scan([self.tmpdir])
        results = index.search(car_query="BMW M4", track_query="Spa")
        self.assertEqual(len(results), 2)

    def test_search_no_match(self):
        index = setup_library.scan([self.tmpdir])
        self.assertEqual(index.search("Ferrari", ""), [])

    def test_all_cars_and_tracks(self):
        index = setup_library.scan([self.tmpdir])
        self.assertEqual(len(index.all_cars()), 3)
        self.assertEqual(len(index.all_tracks()), 3)

    def test_nonexistent_root_is_skipped(self):
        index = setup_library.scan([self.tmpdir, "/no/such/directory/anywhere"])
        self.assertEqual(index.count(), 5)


class FuzzyScoreTests(unittest.TestCase):

    def test_exact_match_scores_highest(self):
        exact = setup_library._fuzzy_score("bmw m4 gt3", "bmw m4 gt3")
        substring = setup_library._fuzzy_score("bmw m4", "bmw m4 gt3")
        self.assertGreater(exact, substring)

    def test_token_overlap(self):
        # No substring match but shared tokens
        score = setup_library._fuzzy_score("spa francorchamps", "francorchamps gp")
        self.assertGreater(score, 0)

    def test_case_insensitive(self):
        self.assertGreater(
            setup_library._fuzzy_score("PORSCHE 911", "porsche 911 gt3 r"),
            0)

    def test_empty_returns_zero(self):
        self.assertEqual(setup_library._fuzzy_score("", "anything"), 0)
        self.assertEqual(setup_library._fuzzy_score("anything", ""), 0)


if __name__ == "__main__":
    unittest.main()
