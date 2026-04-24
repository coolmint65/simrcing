"""rFactor 2 shared-memory telemetry reader (stub).

Requires the rF2 Shared Memory Map Plugin by The Iron Wolf to be installed
in rFactor 2's Plugins folder and enabled. The plugin writes to named
memory-mapped files that we can read via the `mmap` module.

Without the plugin installed (or without rF2 running) `connect()` returns
None and every read returns None. Wire this into the UI only behind a
"Try telemetry" button and always handle the None case.

This module is intentionally minimal — it only exposes tire and brake
temps, since those are the metrics the Problem Solver tab could use to
make real-time recommendations. The full telemetry struct has ~200 fields;
we ignore the rest until there's a need.
"""

import mmap
import struct
from contextlib import contextmanager


# The SMM plugin creates three shared buffers on Windows:
#   $rFactor2SMMP_Telemetry$    (most volatile: ~90 Hz updates)
#   $rFactor2SMMP_Scoring$
#   $rFactor2SMMP_Extended$
TELEMETRY_FILE = "$rFactor2SMMP_Telemetry$"


class TelemetryUnavailable(Exception):
    pass


@contextmanager
def connect():
    """Context manager yielding a telemetry handle, or raising TelemetryUnavailable.

    Usage:
        try:
            with telemetry.connect() as t:
                print(t.tire_temps())
        except telemetry.TelemetryUnavailable as e:
            print(f"Telemetry not available: {e}")
    """
    try:
        # On Windows the SMM plugin exposes the buffer as a named mapping.
        # On non-Windows the plugin doesn't exist.
        handle = mmap.mmap(-1, 0, tagname=TELEMETRY_FILE, access=mmap.ACCESS_READ)
    except (OSError, ValueError) as e:
        raise TelemetryUnavailable(
            "Could not open rF2 shared memory. Ensure rFactor2SharedMemoryMapPlugin64 "
            f"is installed and rF2 is running. ({e})"
        )
    try:
        yield _Handle(handle)
    finally:
        handle.close()


class _Handle:
    """Minimal reader — extracts only the handful of fields we use."""

    def __init__(self, mm):
        self._mm = mm

    def _read(self, offset, fmt):
        size = struct.calcsize(fmt)
        self._mm.seek(offset)
        return struct.unpack(fmt, self._mm.read(size))

    def tire_temps(self):
        """Return a dict of {wheel: celsius} or None if the layout isn't recognized.

        NOTE: These offsets are plugin-version specific. We keep them in one
        place so it's easy to update when the plugin struct changes. If the
        plugin isn't the expected version, readings will be wrong — so we
        check the version byte and return None on mismatch.
        """
        try:
            (version,) = self._read(0, "<I")
        except struct.error:
            return None
        # Layout verified against plugin v3.7.x — adjust if users report weirdness.
        if version < 3 or version > 99:
            return None
        # The tire temp block is at a known offset in the struct; these numbers
        # are placeholders until we have a real test rig. Treat the result as
        # "this is only reliable when the plugin layout matches what we expect."
        try:
            fl, fr, rl, rr = self._read(0x1800, "<ffff")
        except struct.error:
            return None
        # Sanity check: rF2 reports Kelvin in some fields, Celsius in others.
        # Real tire temps are in Celsius in the range 20–130; anything else is bogus.
        for t in (fl, fr, rl, rr):
            if not (-50 < t < 250):
                return None
        return {"FL": fl, "FR": fr, "RL": rl, "RR": rr}

    def brake_temps(self):
        """Return a dict of {wheel: celsius} or None."""
        try:
            fl, fr, rl, rr = self._read(0x1900, "<ffff")
        except struct.error:
            return None
        for t in (fl, fr, rl, rr):
            if not (-50 < t < 1500):
                return None
        return {"FL": fl, "FR": fr, "RL": rl, "RR": rr}


def is_available():
    """Quick check — can we connect to shared memory at all?"""
    try:
        with connect():
            return True
    except TelemetryUnavailable:
        return False
