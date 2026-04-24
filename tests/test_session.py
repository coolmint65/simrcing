"""Tests for the race weekend planner."""

import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rf2 import session as session_mod


class SessionTests(unittest.TestCase):

    def test_estimated_laps_from_time(self):
        s = session_mod.Session(duration_min=30, expected_lap_time_s=90, fuel_per_lap_l=2)
        # 30 min = 1800 s; 1800 / 90 = 20 laps; +1 buffer
        self.assertEqual(s.estimated_laps(), 21)

    def test_estimated_laps_explicit(self):
        s = session_mod.Session(duration_laps=42, fuel_per_lap_l=2)
        self.assertEqual(s.estimated_laps(), 42)

    def test_required_fuel(self):
        s = session_mod.Session(duration_laps=20, fuel_per_lap_l=2.5)
        # 20 laps + 1 safety lap = 21 * 2.5 = 52.5 L
        self.assertAlmostEqual(s.required_fuel_l(safety_laps=1), 52.5)

    def test_zero_lap_time_no_laps(self):
        s = session_mod.Session(duration_min=30, expected_lap_time_s=0)
        self.assertEqual(s.estimated_laps(), 0)


class PersistTests(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.patcher = mock.patch.object(session_mod, "SESSION_DIR", self.tmpdir)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def test_round_trip(self):
        w = session_mod.RaceWeekend(car="BMW M4 GT3", track="Spa", date="2026-04-23")
        w.sessions.append(session_mod.Session(name="Race", duration_laps=24,
                                                fuel_per_lap_l=2.3))
        path = session_mod.save(w)
        loaded = session_mod.load(path)
        self.assertEqual(loaded.car, "BMW M4 GT3")
        self.assertEqual(loaded.track, "Spa")
        self.assertEqual(len(loaded.sessions), 1)
        self.assertEqual(loaded.sessions[0].duration_laps, 24)

    def test_filename_is_deterministic(self):
        w = session_mod.RaceWeekend(car="Porsche 911 GT3 R",
                                      track="Spa-Francorchamps",
                                      date="2026-04-23")
        self.assertEqual(
            session_mod.weekend_filename(w),
            "porsche_911_gt3_r__spa_francorchamps__2026_04_23.json",
        )

    def test_list_weekends_sorted_by_date(self):
        session_mod.save(session_mod.RaceWeekend(car="a", track="b", date="2026-01-01"))
        session_mod.save(session_mod.RaceWeekend(car="c", track="d", date="2026-05-01"))
        session_mod.save(session_mod.RaceWeekend(car="e", track="f", date="2026-03-01"))
        entries = session_mod.list_weekends()
        dates = [w.date for _, w in entries]
        self.assertEqual(dates, ["2026-05-01", "2026-03-01", "2026-01-01"])


if __name__ == "__main__":
    unittest.main()
