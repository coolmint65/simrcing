"""Tests for the fuel and gear-ratio calculators."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rf2.calculators import (fuel_needed, final_drive_for_top_speed,
                              top_speed_for_final_drive)


class FuelCalcTests(unittest.TestCase):

    def test_zero_laps_still_includes_buffer(self):
        self.assertEqual(fuel_needed(0, 2.5, 1), 2.5)

    def test_rounds_up_to_half_liter(self):
        # 10 laps * 2.33 L/lap + 1 * 2.33 = 25.63 L → 26.0 L
        self.assertEqual(fuel_needed(10, 2.33, 1), 26.0)

    def test_no_safety(self):
        self.assertEqual(fuel_needed(20, 2.5, 0), 50.0)

    def test_negative_inputs_rejected(self):
        with self.assertRaises(ValueError):
            fuel_needed(-1, 2.0, 1)
        with self.assertRaises(ValueError):
            fuel_needed(10, -2.0, 1)


class GearCalcTests(unittest.TestCase):

    def test_roundtrip(self):
        fd = final_drive_for_top_speed(280, 8000, 1.08, 0.33)
        computed_top = top_speed_for_final_drive(fd, 8000, 1.08, 0.33)
        # Rounding the final drive to 2 decimals drops ~0.1-0.5 kph fidelity
        self.assertAlmostEqual(computed_top, 280, delta=1.5)

    def test_higher_rev_limit_gives_higher_top_speed(self):
        v1 = top_speed_for_final_drive(3.0, 8000, 1.0, 0.33)
        v2 = top_speed_for_final_drive(3.0, 12000, 1.0, 0.33)
        self.assertGreater(v2, v1)

    def test_negative_rejected(self):
        with self.assertRaises(ValueError):
            final_drive_for_top_speed(-1, 8000, 1.0, 0.33)
        with self.assertRaises(ValueError):
            top_speed_for_final_drive(3.0, 0, 1.0, 0.33)


if __name__ == "__main__":
    unittest.main()
