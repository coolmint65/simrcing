"""Track database loader.

The actual track definitions live in `data/tracks.json` so community
additions can be made via PR without touching Python code.
"""

import json
import os


_DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "tracks.json",
)


def _load_tracks():
    with open(_DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


TRACKS = _load_tracks()


def find_track(query):
    """Return a list of (name, data) pairs matching the query."""
    if not query:
        return []
    q = query.lower().strip()
    exact = []
    contains = []
    for name, data in TRACKS.items():
        lname = name.lower()
        if lname == q:
            exact.append((name, data))
        elif q in lname:
            contains.append((name, data))
    return exact + contains
