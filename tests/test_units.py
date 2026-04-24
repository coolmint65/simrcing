"""Tests for metric <-> imperial unit conversion."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rf2.units import convert, format_value


class UnitTests(unittest.TestCase):

    def test_mm_to_in(self):
        v, u = convert(25.4, "mm", "imperial")
        self.assertAlmostEqual(v, 1.0, places=3)
        self.assertEqual(u, "in")

    def test_kpa_to_psi(self):
        v, u = convert(145, "kPa", "imperial")
        self.assertAlmostEqual(v, 21.03, places=1)
        self.assertEqual(u, "psi")

    def test_metric_noop(self):
        v, u = convert(145, "kPa", "metric")
        self.assertEqual(v, 145)
        self.assertEqual(u, "kPa")

    def test_unknown_unit_noop(self):
        v, u = convert(5, "widgets", "imperial")
        self.assertEqual(v, 5)
        self.assertEqual(u, "widgets")

    def test_format_imperial(self):
        s = format_value(145, "kPa", "imperial")
        self.assertIn("psi", s)


if __name__ == "__main__":
    unittest.main()
