"""Tests for baseline setup generation."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rf2.knowledge import (CAR_CLASSES, TRACK_TYPES,
                            generate_baseline, generate_smart_baseline)
from rf2.parameters import SETUP_CATEGORIES


class BaselineTests(unittest.TestCase):

    def test_every_class_produces_valid_baseline(self):
        """Every car class should generate a complete setup with all 48 parameters."""
        for cls_name in CAR_CLASSES:
            setup, _tips, _warnings = generate_baseline(cls_name, "High-Speed Circuit")
            self.assertIsNotNone(setup, f"No setup for {cls_name}")
            for cat, params in SETUP_CATEGORIES.items():
                self.assertIn(cat, setup, f"{cls_name}: missing category {cat}")
                for param in params:
                    self.assertIn(param, setup[cat],
                                   f"{cls_name}: missing {cat}/{param}")

    def test_all_values_within_bounds(self):
        """Every generated parameter should be within the SETUP_CATEGORIES (min, max)."""
        for cls_name in CAR_CLASSES:
            for track_type in TRACK_TYPES:
                setup, _t, _w = generate_baseline(cls_name, track_type)
                for cat, params in setup.items():
                    for param, val in params.items():
                        info = SETUP_CATEGORIES.get(cat, {}).get(param)
                        if not info:
                            continue
                        vmin, vmax = info[0], info[1]
                        self.assertGreaterEqual(val, vmin,
                                                 f"{cls_name}/{track_type}: {cat}/{param}={val} < {vmin}")
                        self.assertLessEqual(val, vmax,
                                              f"{cls_name}/{track_type}: {cat}/{param}={val} > {vmax}")

    def test_unknown_class_returns_error(self):
        setup, _t, warnings = generate_baseline("Nonexistent Class", "High-Speed Circuit")
        self.assertIsNone(setup)
        self.assertTrue(len(warnings) > 0)

    def test_historic_warns_about_aids(self):
        _setup, _tips, warnings = generate_baseline("Historic GT / Sports Car",
                                                      "Technical / Tight Circuit")
        text = " ".join(warnings).lower()
        self.assertIn("abs", text)

    def test_smart_baseline_with_car_data(self):
        car = {
            "class": "GT3",
            "engine": "mid",
            "drivetrain": "RWD",
            "aero": "medium",
            "weight": 1300,
            "power": 550,
            "has_abs": True,
            "has_tc": True,
            "bias": {"Aero": {"Rear Wing Angle": 2}},
            "notes": "test car",
        }
        setup, tips, warnings, meta = generate_smart_baseline(car, None, apply_meta=False)
        self.assertIsNotNone(setup)
        # Bias should have shifted rear wing by +2 from the class default
        self.assertGreater(setup["Aero"]["Rear Wing Angle"],
                            CAR_CLASSES["GT3"]["defaults"]["Aero"]["Rear Wing Angle"] - 1)


if __name__ == "__main__":
    unittest.main()
