"""Tests for the library corpus analysis module."""

import os
import sys
import unittest
from dataclasses import dataclass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rf2 import analysis


@dataclass
class FakeEntry:
    path: str
    car: str = ""
    track: str = ""
    name: str = ""
    mtime: float = 0.0
    raw_car_folder: str = ""
    raw_track_folder: str = ""


def _make_loaded(values_per_setup):
    """values_per_setup: list of dicts like [{'Aero': {'Front Wing Angle': 10}}, ...]"""
    out = []
    for i, setup in enumerate(values_per_setup):
        out.append((FakeEntry(path=f"fake{i}.svm", name=f"s{i}"), setup))
    return out


class ParamStatsTests(unittest.TestCase):

    def test_basic_stats(self):
        loaded = _make_loaded([
            {"Aero": {"Front Wing Angle": 10}},
            {"Aero": {"Front Wing Angle": 12}},
            {"Aero": {"Front Wing Angle": 14}},
        ])
        stats = analysis.param_stats(loaded)
        s = stats[("Aero", "Front Wing Angle")]
        self.assertEqual(s["n"], 3)
        self.assertEqual(s["median"], 12)
        self.assertEqual(s["min"], 10)
        self.assertEqual(s["max"], 14)
        self.assertGreater(s["stdev"], 0)

    def test_skips_non_numeric(self):
        loaded = _make_loaded([
            {"Aero": {"Front Wing Angle": "high"}},
            {"Aero": {"Front Wing Angle": 10}},
        ])
        stats = analysis.param_stats(loaded)
        self.assertEqual(stats[("Aero", "Front Wing Angle")]["n"], 1)


class OutlierTests(unittest.TestCase):

    def test_detects_outlier(self):
        loaded = _make_loaded([
            {"Aero": {"Rear Wing Angle": 10}},
            {"Aero": {"Rear Wing Angle": 11}},
            {"Aero": {"Rear Wing Angle": 12}},
            {"Aero": {"Rear Wing Angle": 11}},
            {"Aero": {"Rear Wing Angle": 10}},
        ])
        stats = analysis.param_stats(loaded)
        outliers = analysis.outliers_vs(stats, {"Aero": {"Rear Wing Angle": 30}})
        self.assertEqual(len(outliers), 1)
        cat, param, ours, median, z, _stdev = outliers[0]
        self.assertEqual((cat, param), ("Aero", "Rear Wing Angle"))
        self.assertEqual(ours, 30)
        self.assertGreater(z, analysis.OUTLIER_SIGMA)

    def test_no_outlier_when_within_sigma(self):
        loaded = _make_loaded([
            {"Aero": {"Rear Wing Angle": 10}},
            {"Aero": {"Rear Wing Angle": 12}},
            {"Aero": {"Rear Wing Angle": 14}},
        ])
        stats = analysis.param_stats(loaded)
        outliers = analysis.outliers_vs(stats, {"Aero": {"Rear Wing Angle": 13}})
        self.assertEqual(outliers, [])

    def test_unanimous_corpus_any_difference_is_outlier(self):
        loaded = _make_loaded([
            {"Aero": {"Rear Wing Angle": 10}},
            {"Aero": {"Rear Wing Angle": 10}},
        ])
        stats = analysis.param_stats(loaded)
        outliers = analysis.outliers_vs(stats, {"Aero": {"Rear Wing Angle": 11}})
        self.assertEqual(len(outliers), 1)


class ClosestToMedianTests(unittest.TestCase):

    def test_picks_closest(self):
        loaded = _make_loaded([
            {"A": {"x": 10}, "A": {"y": 10}},   # same key "A" — merge by overwrite
            {"A": {"x": 20, "y": 20}},
            {"A": {"x": 30, "y": 30}},
        ])
        # Fix the above: each loaded should be its own dict
        loaded = [
            (FakeEntry(path="a.svm", name="a"), {"A": {"x": 10, "y": 10}}),
            (FakeEntry(path="b.svm", name="b"), {"A": {"x": 20, "y": 20}}),
            (FakeEntry(path="c.svm", name="c"), {"A": {"x": 30, "y": 30}}),
        ]
        stats = analysis.param_stats(loaded)
        best, _d = analysis.closest_to_median(loaded, stats)
        self.assertEqual(best.name, "b")


if __name__ == "__main__":
    unittest.main()
