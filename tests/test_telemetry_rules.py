"""Tests for the telemetry rules engine."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rf2 import telemetry_rules


def _reading(overrides):
    """overrides: dict with (wheel, field) keys, e.g. {('FL', 'brake_temp'): 750}"""
    r = telemetry_rules.TelemetryReading.empty()
    for (wheel, field), val in overrides.items():
        setattr(r.wheels[wheel], field, val)
    return r


class CamberRuleTests(unittest.TestCase):

    def test_inner_way_hotter_suggests_less_camber(self):
        r = _reading({
            ("FL", "tire_temp_inner"): 110,
            ("FL", "tire_temp_outer"): 90,    # 20°C hotter inside
        })
        suggestions = telemetry_rules._camber_rule(r)
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0].param, "Front Camber")
        self.assertEqual(suggestions[0].direction, "increase")

    def test_even_temps_suggest_more_camber(self):
        r = _reading({
            ("RL", "tire_temp_inner"): 95,
            ("RL", "tire_temp_outer"): 94,    # inner only 1°C hotter
        })
        suggestions = telemetry_rules._camber_rule(r)
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0].param, "Rear Camber")
        self.assertEqual(suggestions[0].direction, "decrease")

    def test_ideal_temps_no_suggestion(self):
        r = _reading({
            ("FL", "tire_temp_inner"): 100,
            ("FL", "tire_temp_outer"): 92,    # 8°C inside hotter = ideal
        })
        self.assertEqual(telemetry_rules._camber_rule(r), [])


class BrakeRuleTests(unittest.TestCase):

    def test_hot_fronts_suggest_opening_ducts(self):
        r = _reading({
            ("FL", "brake_temp"): 750,
            ("FR", "brake_temp"): 720,
        })
        suggestions = telemetry_rules._brake_duct_rule(r)
        self.assertTrue(any(s.param == "Brake Ducts Front" and s.direction == "increase"
                             for s in suggestions))

    def test_cold_rears_suggest_closing_ducts(self):
        r = _reading({
            ("RL", "brake_temp"): 250,
            ("RR", "brake_temp"): 250,
        })
        suggestions = telemetry_rules._brake_duct_rule(r)
        self.assertTrue(any(s.param == "Brake Ducts Rear" and s.direction == "decrease"
                             for s in suggestions))

    def test_normal_brakes_no_suggestion(self):
        r = _reading({(w, "brake_temp"): 500 for w in telemetry_rules.WHEEL_NAMES})
        self.assertEqual(telemetry_rules._brake_duct_rule(r), [])


class PressureRuleTests(unittest.TestCase):

    def test_high_rise_suggests_raising_cold(self):
        r = _reading({
            ("FL", "tire_pressure_cold"): 140,
            ("FL", "tire_pressure_hot"): 170,   # +30 kPa
        })
        suggestions = telemetry_rules._tire_pressure_rule(r)
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0].direction, "increase")


class BalanceRuleTests(unittest.TestCase):

    def test_front_way_hotter_suggests_less_front_bias(self):
        r = telemetry_rules.TelemetryReading.empty()
        for w in ("FL", "FR"):
            r.wheels[w].tire_temp_middle = 110
        for w in ("RL", "RR"):
            r.wheels[w].tire_temp_middle = 85      # 25°C cooler rears
        suggestions = telemetry_rules._front_rear_balance_rule(r)
        self.assertTrue(any(s.param == "Brake Bias" and s.direction == "decrease"
                             for s in suggestions))

    def test_left_right_imbalance_flags_weight_dist(self):
        r = telemetry_rules.TelemetryReading.empty()
        r.wheels["FL"].tire_temp_middle = 110
        r.wheels["FR"].tire_temp_middle = 90       # 20°C difference
        suggestions = telemetry_rules._left_right_balance_rule(r)
        self.assertTrue(any(s.param == "Weight Distribution" for s in suggestions))


class AnalyzeTests(unittest.TestCase):

    def test_priority_sorted(self):
        r = _reading({
            ("FL", "brake_temp"): 750,          # priority 1
            ("FL", "tire_temp_inner"): 110,
            ("FL", "tire_temp_outer"): 90,      # priority 2
            ("RL", "tire_temp_inner"): 94,
            ("RL", "tire_temp_outer"): 93,      # priority 3
        })
        suggestions = telemetry_rules.analyze(r)
        priorities = [s.priority for s in suggestions]
        self.assertEqual(priorities, sorted(priorities))

    def test_empty_reading_no_suggestions(self):
        self.assertEqual(
            telemetry_rules.analyze(telemetry_rules.TelemetryReading.empty()),
            [])


if __name__ == "__main__":
    unittest.main()
