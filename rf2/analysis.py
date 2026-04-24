"""Setup corpus analysis.

Given a set of library entries (typically all .svm files for the same
car + track), read them and compute per-parameter statistics: how
consensual each parameter is, which setups deviate, how your current
setup compares to the median.

Use cases:
  - "Show me what parameters everyone agrees on for BMW M4 GT3 @ Spa"
  - "Is my current brake bias an outlier?"
  - "Which saved setup is closest to the median?"
"""

import statistics

from rf2 import svm as svm_io


OUTLIER_SIGMA = 2.0


def load_setups(entries):
    """Read every entry's .svm. Returns list of (entry, partial_setup).

    Unreadable files are skipped silently — a corrupted setup on disk
    shouldn't break the whole analysis.
    """
    loaded = []
    for entry in entries:
        try:
            partial, _unmapped = svm_io.read_svm(entry.path)
        except (OSError, UnicodeDecodeError):
            continue
        if partial:
            loaded.append((entry, partial))
    return loaded


def param_stats(loaded):
    """Compute per-parameter stats across all loaded setups.

    Returns {(category, param): {n, mean, median, stdev, min, max,
                                 values: [(entry, value)]}}.
    Only numeric values are included; non-numeric (unusual) are dropped.
    """
    collected = {}
    for entry, setup in loaded:
        for cat, params in setup.items():
            for param, val in params.items():
                if not isinstance(val, (int, float)):
                    continue
                collected.setdefault((cat, param), []).append((entry, val))

    stats = {}
    for key, pairs in collected.items():
        values = [v for _, v in pairs]
        if not values:
            continue
        stats[key] = {
            "n": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "stdev": statistics.stdev(values) if len(values) > 1 else 0.0,
            "min": min(values),
            "max": max(values),
            "values": pairs,
        }
    return stats


def outliers_vs(stats, setup):
    """Return parameters where `setup`'s value is > OUTLIER_SIGMA z-score
    from the median across the corpus.

    Yields (category, param, our_value, median, z_score, stdev) sorted
    by descending z-score. Parameters with stdev = 0 (perfect consensus)
    are flagged iff our value differs at all.
    """
    out = []
    for (cat, param), s in stats.items():
        ours = setup.get(cat, {}).get(param)
        if ours is None:
            continue
        median = s["median"]
        stdev = s["stdev"]
        if stdev == 0:
            if ours != median:
                out.append((cat, param, ours, median, float("inf"), 0.0))
            continue
        z = abs(ours - median) / stdev
        if z >= OUTLIER_SIGMA:
            out.append((cat, param, ours, median, z, stdev))
    out.sort(key=lambda r: -r[4])
    return out


def consensus_rank(stats):
    """Rank parameters from most-consensual (low stdev relative to range)
    to least. Useful for highlighting 'everyone does this' settings.

    Returns list of (category, param, coefficient_of_variation) sorted
    ascending by CoV. Parameters where everyone agrees on the exact
    same value come first.
    """
    ranked = []
    for (cat, param), s in stats.items():
        if s["n"] < 2:
            continue
        mean = s["mean"]
        if mean == 0:
            cov = s["stdev"]
        else:
            cov = s["stdev"] / abs(mean)
        ranked.append((cat, param, cov))
    ranked.sort(key=lambda r: r[2])
    return ranked


def closest_to_median(loaded, stats):
    """Find the single setup in `loaded` whose parameters deviate least
    from the corpus median overall. Useful for 'if I had to pick one,
    which would be the most representative?'.

    Distance metric: sum of (value - median)^2 / stdev^2 across all
    parameters present in both the setup and the stats. Parameters
    with stdev=0 are skipped so one unanimous value can't dominate.
    """
    best = None
    best_distance = None
    for entry, setup in loaded:
        d = 0.0
        counted = 0
        for (cat, param), s in stats.items():
            if s["stdev"] == 0:
                continue
            val = setup.get(cat, {}).get(param)
            if val is None:
                continue
            d += ((val - s["median"]) / s["stdev"]) ** 2
            counted += 1
        if counted == 0:
            continue
        normalized = d / counted
        if best is None or normalized < best_distance:
            best = entry
            best_distance = normalized
    return best, best_distance
