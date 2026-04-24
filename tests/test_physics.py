"""Tests for physics calculations."""

import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rf2 import physics


class WeightTransferTests(unittest.TestCase):

    def test_zero_accel_no_transfer(self):
        delta = physics.longitudinal_weight_transfer(1300, 450, 2700, 0)
        self.assertEqual(delta, 0)

    def test_braking_transfers_forward(self):
        # 1g braking on a 1300kg car with 450mm CoG / 2700mm wheelbase
        delta = physics.longitudinal_weight_transfer(1300, 450, 2700, 1.0)
        # ΔW = 1300 × 9.81 × (450/2700) × 1 = 2125 N
        self.assertAlmostEqual(delta, 2125, delta=5)

    def test_corner_loads_sum_to_static_when_no_accel(self):
        loads = physics.dynamic_corner_loads(1300, 50, 450, 2700, 1600,
                                               long_g=0, lat_g=0)
        self.assertAlmostEqual(sum(loads.values()), 1300 * physics.G, delta=1)

    def test_corner_loads_unload_inside_wheels_in_corner(self):
        # Right-hand turn (lat_g > 0 = right-side loaded)
        loads = physics.dynamic_corner_loads(1300, 50, 450, 2700, 1600,
                                               long_g=0, lat_g=1.0)
        # left side should unload, right side should gain
        self.assertLess(loads["FL"], loads["FR"])
        self.assertLess(loads["RL"], loads["RR"])

    def test_static_corner_loads_with_fwd_bias(self):
        loads = physics.static_corner_loads(1300, 60)
        # 60% front means each front corner carries 30% of total
        self.assertAlmostEqual(loads["FL"], 1300 * physics.G * 0.3, delta=1)
        self.assertAlmostEqual(loads["RL"], 1300 * physics.G * 0.2, delta=1)


class FrequencyTests(unittest.TestCase):

    def test_natural_frequency_typical_gt3(self):
        # 90 N/mm on 300kg corner should give ~2.76 Hz
        f = physics.natural_frequency(90, 300)
        self.assertAlmostEqual(f, 2.76, delta=0.05)

    def test_higher_spring_higher_frequency(self):
        f_low = physics.natural_frequency(60, 300)
        f_high = physics.natural_frequency(120, 300)
        self.assertGreater(f_high, f_low)

    def test_roundtrip_target_to_actual(self):
        target = 3.0
        mass = 300
        k = physics.target_spring_rate(target, mass)
        actual = physics.natural_frequency(k, mass)
        self.assertAlmostEqual(actual, target, delta=0.02)

    def test_negative_mass_rejected(self):
        with self.assertRaises(ValueError):
            physics.natural_frequency(90, -1)

    def test_motion_ratio_effect(self):
        # Half motion ratio quarters the wheel rate, halving freq
        f_full = physics.natural_frequency(100, 300, motion_ratio=1.0)
        f_half = physics.natural_frequency(100, 300, motion_ratio=0.5)
        self.assertAlmostEqual(f_half / f_full, 0.5, delta=0.01)


class AeroTests(unittest.TestCase):

    def test_balance_symmetric(self):
        self.assertAlmostEqual(physics.aero_balance(500, 500), 50.0)

    def test_balance_rear_heavy(self):
        b = physics.aero_balance(300, 700)
        self.assertAlmostEqual(b, 30.0)

    def test_balance_no_downforce_defaults_to_50(self):
        self.assertEqual(physics.aero_balance(0, 0), 50.0)

    def test_downforce_scales_with_speed_squared(self):
        f1, r1 = physics.estimate_downforce(15, 20, 5, 5, 100, "medium")
        f2, r2 = physics.estimate_downforce(15, 20, 5, 5, 200, "medium")
        # v² law: 200 km/h should give 4x the downforce of 100 km/h
        self.assertAlmostEqual((f2 + r2) / (f1 + r1), 4, delta=0.1)

    def test_higher_aero_class_more_downforce(self):
        _, r_low = physics.estimate_downforce(15, 20, 5, 5, 200, "low")
        _, r_high = physics.estimate_downforce(15, 20, 5, 5, 200, "extreme")
        self.assertGreater(r_high, r_low * 2)


class PhysicsForCarTests(unittest.TestCase):

    def test_fallback_to_class_defaults(self):
        p = physics.physics_for_car({"class": "GT3"})
        self.assertEqual(p["mass_kg"], 1300)
        self.assertEqual(p["wheelbase_mm"], 2700)

    def test_car_overrides_take_precedence(self):
        p = physics.physics_for_car({"class": "GT3", "weight": 1350,
                                       "wheelbase_mm": 2750})
        self.assertEqual(p["mass_kg"], 1350)
        self.assertEqual(p["wheelbase_mm"], 2750)

    def test_unknown_class_still_returns_something(self):
        p = physics.physics_for_car({"class": "Unknown"})
        self.assertGreater(p["mass_kg"], 0)


if __name__ == "__main__":
    unittest.main()
