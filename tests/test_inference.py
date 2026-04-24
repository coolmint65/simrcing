"""Regression tests for the keyword inference engine.

If a keyword gets removed from rf2/inference.py, one of these expectations
should fail — that's the point. Don't weaken these without adding a better
replacement keyword.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rf2.inference import infer_car, infer_track


class CarInferenceTests(unittest.TestCase):

    def _assert_class(self, name, expected_class):
        result = infer_car(name)
        self.assertEqual(result["inferred"].get("class"), expected_class,
                         f"{name!r} should infer as {expected_class}, "
                         f"got {result['inferred'].get('class')}")

    def test_gt3_keyword(self):
        self._assert_class("Some Mod Car GT3", "GT3")

    def test_gte_keyword(self):
        self._assert_class("Random GTE Mod", "GTE / GT2")

    def test_lmp2_keyword(self):
        self._assert_class("Oreca 07 LMP2", "LMP2 / Prototype")

    def test_formula_keyword(self):
        self._assert_class("Modern Formula Car", "Open-Wheel / Formula")

    def test_touring_car_keyword(self):
        self._assert_class("BTCC Honda", "Touring Car")

    def test_historic_cobra(self):
        self._assert_class("Shelby Cobra 427", "Historic GT / Sports Car")

    def test_historic_917(self):
        self._assert_class("Porsche 917K", "Historic GT / Sports Car")

    def test_historic_formula_lotus_49(self):
        self._assert_class("Lotus 49 Cosworth", "Historic Formula / Open-Wheel")

    def test_group_c_962(self):
        self._assert_class("Porsche 962C", "Group C / Can-Am / Historic Prototype")

    def test_stock_car_nascar(self):
        self._assert_class("NASCAR Cup Car", "Stock Car / Oval")

    def test_unknown_car_triggers_wizard(self):
        result = infer_car("Squiggle Flargon 3000")
        self.assertLess(result["confidence"], 0.5)
        self.assertTrue(len(result["questions"]) > 0,
                        "Unknown car should return wizard questions")

    def test_historic_disables_driver_aids(self):
        result = infer_car("Ferrari 250 GTO")
        self.assertFalse(result["inferred"].get("has_abs", True))
        self.assertFalse(result["inferred"].get("has_tc", True))

    def test_formula_has_no_abs(self):
        result = infer_car("Modern Formula 1")
        self.assertFalse(result["inferred"].get("has_abs", True))

    def test_porsche_911_is_rear_engine(self):
        result = infer_car("Porsche 911 RSR")
        self.assertEqual(result["inferred"].get("engine"), "rear")

    def test_turbo_detected(self):
        result = infer_car("Porsche 935 Turbo")
        self.assertTrue(result["inferred"].get("turbo"))

    def test_non_turbo_not_flagged(self):
        result = infer_car("Ferrari 250 GTO")
        self.assertFalse(result["inferred"].get("turbo"))


class TrackInferenceTests(unittest.TestCase):

    def test_high_speed_keyword(self):
        result = infer_track("Monza GP")
        # Monza should at least get classified as something
        self.assertIn("type", result["inferred"])

    def test_unknown_track_triggers_wizard(self):
        result = infer_track("Bloop Trackway")
        self.assertLess(result["confidence"], 0.5)


if __name__ == "__main__":
    unittest.main()
