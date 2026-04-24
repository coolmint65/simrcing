"""Race weekend / session planning.

A RaceWeekend ties together the sessions you plan to run at one event:
practice, qualifying, warm-up, race. Each session carries a fuel plan,
tire plan, reference lap time, and an optional pointer to a specific
library setup (.svm path).

Planning data persists to user_profiles/sessions/*.json — one file per
weekend, named "<car>__<track>__<date>.json" (slugified).
"""

import json
import os
import re
from dataclasses import dataclass, asdict, field
from typing import List


_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSION_DIR = os.path.join(_PROJECT_ROOT, "user_profiles", "sessions")


SESSION_TYPES = ("Practice", "Qualifying", "Warm-Up", "Race", "Sprint Race")


@dataclass
class Session:
    name: str = "Race"
    duration_min: float = 0.0       # 0 means lap-count-based
    duration_laps: int = 0          # 0 means time-based
    expected_lap_time_s: float = 0.0
    fuel_per_lap_l: float = 2.5
    starting_compound: str = "medium"
    setup_path: str = ""
    notes: str = ""

    def estimated_laps(self):
        if self.duration_laps > 0:
            return self.duration_laps
        if self.duration_min > 0 and self.expected_lap_time_s > 0:
            return int(self.duration_min * 60 // self.expected_lap_time_s) + 1
        return 0

    def required_fuel_l(self, safety_laps=1.0):
        laps = self.estimated_laps()
        if laps <= 0 or self.fuel_per_lap_l <= 0:
            return 0.0
        return (laps + safety_laps) * self.fuel_per_lap_l


@dataclass
class RaceWeekend:
    car: str = ""
    track: str = ""
    date: str = ""              # ISO yyyy-mm-dd
    sessions: List[Session] = field(default_factory=list)
    notes: str = ""


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------

def _slug(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[^\w]+", "_", s)
    return s.strip("_") or "unknown"


def weekend_filename(weekend):
    return f"{_slug(weekend.car)}__{_slug(weekend.track)}__{_slug(weekend.date)}.json"


def save(weekend):
    os.makedirs(SESSION_DIR, exist_ok=True)
    path = os.path.join(SESSION_DIR, weekend_filename(weekend))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(weekend), f, indent=2)
    return path


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    sessions = [Session(**s) for s in data.get("sessions", [])]
    return RaceWeekend(
        car=data.get("car", ""),
        track=data.get("track", ""),
        date=data.get("date", ""),
        sessions=sessions,
        notes=data.get("notes", ""),
    )


def list_weekends():
    """Return list of (filename, weekend) sorted by date descending."""
    if not os.path.isdir(SESSION_DIR):
        return []
    out = []
    for name in os.listdir(SESSION_DIR):
        if not name.endswith(".json"):
            continue
        path = os.path.join(SESSION_DIR, name)
        try:
            w = load(path)
        except (OSError, json.JSONDecodeError, TypeError):
            continue
        out.append((path, w))
    out.sort(key=lambda x: x[1].date, reverse=True)
    return out


def delete(path):
    if os.path.exists(path):
        os.remove(path)


def new_default_weekend(car="", track=""):
    """Create a default 3-session weekend for a typical sim race."""
    return RaceWeekend(
        car=car, track=track, date="",
        sessions=[
            Session(name="Qualifying", duration_min=15, fuel_per_lap_l=2.5,
                    starting_compound="soft"),
            Session(name="Warm-Up", duration_min=10, fuel_per_lap_l=2.5,
                    starting_compound="medium"),
            Session(name="Race", duration_min=45, fuel_per_lap_l=2.5,
                    starting_compound="medium"),
        ],
    )
