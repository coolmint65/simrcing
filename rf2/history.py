"""Setup change journal — append-only log of every parameter change.

Persisted to user_profiles/journal.jsonl (one JSON object per line). The log
survives across sessions so you can review what you changed last time and why.
"""

import json
import os
from datetime import datetime


_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JOURNAL_DIR = os.path.join(_PROJECT_ROOT, "user_profiles")
JOURNAL_FILE = os.path.join(JOURNAL_DIR, "journal.jsonl")


def _ensure_dir():
    os.makedirs(JOURNAL_DIR, exist_ok=True)


def append_entry(entry):
    """Append a single journal entry (dict) to the log."""
    _ensure_dir()
    entry = dict(entry)
    entry.setdefault("ts", datetime.utcnow().isoformat(timespec="seconds") + "Z")
    with open(JOURNAL_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def log_change(car, track, category, param, old_value, new_value, reason=""):
    """Record a single parameter change."""
    append_entry({
        "kind": "change",
        "car": car,
        "track": track,
        "category": category,
        "param": param,
        "old": old_value,
        "new": new_value,
        "reason": reason,
    })


def log_baseline(car, track):
    """Record baseline generation — serves as a 'session start' anchor."""
    append_entry({
        "kind": "baseline",
        "car": car,
        "track": track,
    })


def log_event(kind, **fields):
    """Record an arbitrary event (load/save/import/export etc)."""
    fields["kind"] = kind
    append_entry(fields)


def read_entries(limit=200):
    """Load the most recent `limit` entries, newest first."""
    if not os.path.exists(JOURNAL_FILE):
        return []
    with open(JOURNAL_FILE, encoding="utf-8") as f:
        lines = f.readlines()
    entries = []
    for line in lines[-limit:]:
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    entries.reverse()
    return entries


def format_entry(entry):
    """One-line human-readable summary of a journal entry."""
    ts = entry.get("ts", "?")
    kind = entry.get("kind", "?")
    car = entry.get("car") or "-"
    track = entry.get("track") or "-"
    prefix = f"{ts}  [{car} @ {track}]"

    if kind == "change":
        return (f"{prefix}  {entry.get('category')}/{entry.get('param')}: "
                f"{entry.get('old')} -> {entry.get('new')}"
                + (f"  — {entry['reason']}" if entry.get("reason") else ""))
    if kind == "baseline":
        return f"{prefix}  BASELINE generated"
    if kind == "save":
        return f"{prefix}  SAVED {entry.get('path', '?')}"
    if kind == "load":
        return f"{prefix}  LOADED {entry.get('path', '?')}"
    if kind == "import_svm":
        return f"{prefix}  IMPORTED .svm {entry.get('path', '?')}"
    if kind == "export_svm":
        return f"{prefix}  EXPORTED .svm {entry.get('path', '?')}"
    return f"{prefix}  {kind} {entry}"
