"""Car database loader.

The actual car definitions live in `data/cars.json` so community additions
can be made via PR without touching Python code. This module loads that file
once at import time and exposes the same `CARS` dict and `find_car()` API
the rest of the app used to get from the hard-coded version.
"""

import json
import os


_DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "cars.json",
)


def _load_cars():
    with open(_DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


CARS = _load_cars()


def find_car(query):
    """Return a list of (name, data) pairs matching the query.

    Matches are case-insensitive substring on the car name.
    """
    if not query:
        return []
    q = query.lower().strip()
    exact = []
    contains = []
    for name, data in CARS.items():
        lname = name.lower()
        if lname == q:
            exact.append((name, data))
        elif q in lname:
            contains.append((name, data))
    return exact + contains
