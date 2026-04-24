"""Setup library — scan rF2 UserData folders for .svm files and index them
by car + track so the Advisor can surface real setups (not just generated
baselines) for a given combo.

Path convention assumed:
    <root>/.../Car_Folder/Track_Folder/setup_name.svm

rFactor 2's UserData path on Windows is typically:
    %USERPROFILE%\\Documents\\rFactor 2\\UserData\\player\\Settings\\

but the scanner just walks whatever roots you give it. It will index
anything with a .svm extension and infer car/track from the two
containing folder names.
"""

import json
import os
from dataclasses import dataclass, asdict, field
from typing import List


@dataclass
class SetupEntry:
    path: str
    car: str                # normalized, lowercase-space
    track: str              # normalized, lowercase-space
    name: str               # filename without .svm
    mtime: float
    raw_car_folder: str     # as it appears on disk
    raw_track_folder: str


@dataclass
class LibraryIndex:
    entries: List[SetupEntry] = field(default_factory=list)
    roots: List[str] = field(default_factory=list)

    def search(self, car_query="", track_query=""):
        """Rank entries by fuzzy match to the queries. Empty query = match all.

        When both queries are given, both must match (AND). When only one is
        given, only that field is checked.
        """
        results = []
        for e in self.entries:
            car_score = _fuzzy_score(car_query, e.car) if car_query else 0
            track_score = _fuzzy_score(track_query, e.track) if track_query else 0

            if car_query and car_score <= 0:
                continue
            if track_query and track_score <= 0:
                continue

            if not car_query and not track_query:
                score = 1
            else:
                score = car_score + track_score
            results.append((score, e))
        results.sort(key=lambda x: -x[0])
        return [e for _, e in results]

    def all_cars(self):
        return sorted({e.car for e in self.entries if e.car})

    def all_tracks(self):
        return sorted({e.track for e in self.entries if e.track})

    def count(self):
        return len(self.entries)


def scan(roots):
    """Walk each root for .svm files and return a fresh LibraryIndex.

    Non-existent roots are skipped silently (so you can list optional
    guesses like Steam and Documents paths and scan whichever exists).
    """
    entries = []
    for root in roots:
        if not root or not os.path.isdir(root):
            continue
        for dirpath, _dirnames, filenames in os.walk(root):
            for fn in filenames:
                if not fn.lower().endswith(".svm"):
                    continue
                path = os.path.join(dirpath, fn)
                entry = _classify(path, root)
                if entry is not None:
                    entries.append(entry)
    return LibraryIndex(entries=entries, roots=list(roots))


def _classify(path, root):
    rel = os.path.relpath(path, root)
    parts = rel.replace("\\", "/").split("/")
    raw_car = parts[-3] if len(parts) >= 3 else (parts[-2] if len(parts) >= 2 else "")
    raw_track = parts[-2] if len(parts) >= 2 else ""
    name = os.path.splitext(parts[-1])[0]
    try:
        mtime = os.path.getmtime(path)
    except OSError:
        return None
    return SetupEntry(
        path=path,
        car=_normalize(raw_car),
        track=_normalize(raw_track),
        name=name,
        mtime=mtime,
        raw_car_folder=raw_car,
        raw_track_folder=raw_track,
    )


def _normalize(s):
    """Convert folder names like 'BMW_M4_GT3' -> 'bmw m4 gt3' for matching."""
    if not s:
        return ""
    return (s.replace("_", " ")
             .replace("-", " ")
             .lower()
             .strip())


def _fuzzy_score(query, target):
    """Simple scoring: exact > substring > token-overlap > 0."""
    q = _normalize(query)
    t = _normalize(target)
    if not q or not t:
        return 0
    if q == t:
        return 100
    if q in t:
        return 50 + len(q)
    if t in q:
        return 40 + len(t)
    qtokens = set(q.split())
    ttokens = set(t.split())
    overlap = qtokens & ttokens
    if overlap:
        return 10 * len(overlap)
    return 0


# ---------------------------------------------------------------------------
# Disk cache
# ---------------------------------------------------------------------------

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_FILE = os.path.join(_PROJECT_ROOT, "user_profiles", "library_index.json")


def save_cache(index):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "roots": index.roots,
            "entries": [asdict(e) for e in index.entries],
        }, f, indent=2)


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return None
    try:
        with open(CACHE_FILE, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError):
        return None
    entries = [SetupEntry(**e) for e in data.get("entries", [])]
    return LibraryIndex(entries=entries, roots=data.get("roots", []))


# ---------------------------------------------------------------------------
# Path guessing
# ---------------------------------------------------------------------------

def default_rf2_paths():
    """Return likely rF2 UserData Settings paths that exist on this machine.

    The Advisor/Library UI uses these as candidate defaults so first-run
    works without any configuration in the common case.
    """
    home = os.path.expanduser("~")
    candidates = [
        os.path.join(home, "Documents", "rFactor 2", "UserData", "player", "Settings"),
        os.path.join(home, "OneDrive", "Documents", "rFactor 2", "UserData", "player", "Settings"),
    ]
    for drive in ("C:", "D:", "E:", "F:", "G:"):
        candidates.append(os.path.join(
            drive + "\\", "Program Files (x86)", "Steam", "steamapps",
            "common", "rFactor 2", "UserData", "player", "Settings"))
        candidates.append(os.path.join(
            drive + "\\", "SteamLibrary", "steamapps", "common",
            "rFactor 2", "UserData", "player", "Settings"))
    return [p for p in candidates if os.path.isdir(p)]
