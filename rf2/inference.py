"""Smart inference engine for rF2 cars and tracks.

When a car or track isn't in the database, this module tries to figure out
what it is from the name alone using keyword matching. If it can't determine
enough, it returns questions for the wizard to ask."""

import json
import os
import re

# ---------------------------------------------------------------------------
# Car inference — keyword patterns
# ---------------------------------------------------------------------------

# Keywords that strongly suggest a car class
CAR_CLASS_KEYWORDS = {
    "GT3": [
        "gt3", "gt 3",
    ],
    "GTE / GT2": [
        "gte", "gt2", "gt 2", "gt-e", "lmgte", "rsr",
    ],
    "LMP2 / Prototype": [
        "lmp2", "lmp 2", "prototype", "p217", "oreca 07",
    ],
    "Open-Wheel / Formula": [
        "formula", "f1", "f2", "f3", "indycar", "indy car", "gp2", "gp3",
        "formula one", "formula 1", "formula 2", "formula 3", "formula e",
        "dallara f", "single seater", "open wheel", "open-wheel",
    ],
    "Touring Car": [
        "touring", "wtcc", "btcc", "dtm", "tcr", "super touring",
        "v8 supercar", "supercars",
    ],
    "Historic GT / Sports Car": [
        "cobra", "250 gto", "gto", "gt40", "e-type", "e type",
        "db4", "db5", "dbr1", "daytona coupe", "917", "904", "906", "910",
        "250 lm", "250 testa", "275 gtb", "365 gtb", "330 p4", "dino",
        "300 slr", "d-type", "d type", "lola t70", "chaparral",
        "pantera", "935", "934", "3.0 csl", "csf sierra", "rs500",
        "f1 gtr", "mclaren f1", "clk-gtr", "clk gtr", "r390",
        "911 gt1", "bmw v12 lmr",
    ],
    "Historic Formula / Open-Wheel": [
        "lotus 49", "lotus 25", "lotus 72", "lotus 79", "lotus 98t",
        "brabham bt", "march 7", "tyrrell", "cooper t", "cooper t51",
        "eagle t1g", "brm", "matra", "ferrari 312",
        "mclaren m23", "tyrrell p34", "ferrari 312t",
        "williams fw07", "williams fw14", "mclaren mp4",
        "ferrari 640", "brabham bt52",
    ],
    "Group C / Can-Am / Historic Prototype": [
        "group c", "group-c", "can-am", "canam", "can am",
        "962", "956", "xjr", "787b", "r89", "r90", "c9",
        "gt1", "lmp1", "lmp 1", "lc2", "88c", "ts020",
        "gt-one", "sauber c9", "toyota gt-one",
    ],
    "Stock Car / Oval": [
        "nascar", "stock car", "stockcar", "cup car",
        "xfinity", "truck series", "arca",
    ],
}

# Keywords that suggest engine layout
ENGINE_KEYWORDS = {
    "front": ["front engine", "front-engine", "fr layout",
              "cobra", "mustang", "camaro", "corvette c1", "corvette c2", "corvette c3",
              "e-type", "e type", "gto", "gt40 mk iv",
              "bmw m4", "mercedes-amg", "aston martin", "vantage",
              "bentley", "jaguar e"],
    "mid": ["mid engine", "mid-engine", "mr layout",
            "mclaren", "ferrari 488", "ferrari 296", "ferrari sf",
            "lamborghini", "ford gt", "gt40", "oreca", "dallara",
            "corvette c8"],
    "rear": ["rear engine", "rear-engine", "rr layout",
             "porsche 911", "porsche 917", "porsche 934", "porsche 935",
             "porsche 956", "porsche 962", "porsche 964", "porsche 993",
             "porsche 996", "porsche 997", "porsche 991", "porsche 992",
             "lotus 49", "lotus 25", "lotus 72", "lotus 79",
             "brabham", "cooper"],
}

# Keywords that suggest era / historic
HISTORIC_KEYWORDS = [
    "historic", "vintage", "classic", "retro", "60s", "70s", "50s",
    "1960", "1961", "1962", "1963", "1964", "1965", "1966", "1967",
    "1968", "1969", "1970", "1971", "1972", "1973", "1974", "1975",
    "1976", "1977", "1978", "1979", "group c", "group a", "group b",
    "can-am", "can am",
]

# Keywords that suggest drivetrain
DRIVETRAIN_KEYWORDS = {
    "FWD": ["fwd", "front wheel drive", "front-wheel-drive",
            "civic", "golf", "megane", "clio", "leon"],
    "AWD": ["awd", "4wd", "all wheel", "all-wheel", "quattro",
            "impreza", "lancer evo", "gt-r r3"],
    "RWD": ["rwd", "rear wheel", "rear-wheel"],
}

# Keywords for aero level
AERO_KEYWORDS = {
    "none": ["no aero", "no wings", "no downforce", "pre-wing"],
    "low": ["low downforce", "low aero", "touring", "stock car", "nascar"],
    "medium": ["gt3", "gt 3", "gt2", "gt 2"],
    "high": ["gte", "lmp2", "group c", "high downforce"],
    "very_high": ["lmp1", "formula 1", "f1", "indycar"],
    "extreme": ["hypercar", "x2010", "x2014"],
}

# Keywords for turbo
TURBO_KEYWORDS = ["turbo", "turbocharged", "twin-turbo", "biturbo", "twinturbo"]


def infer_car(name):
    """Try to infer car characteristics from its name.

    Returns a dict with:
      - 'confidence': float 0-1 (how sure we are)
      - 'inferred': dict of what we figured out
      - 'missing': list of what we couldn't determine
      - 'questions': list of (key, question, options) for the wizard
    """
    name_lower = name.lower().strip()
    inferred = {}
    confidence = 0.0

    # 1. Try to match car class
    best_class = None
    best_class_score = 0
    for cls, keywords in CAR_CLASS_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                score = len(kw)  # longer match = more specific
                if score > best_class_score:
                    best_class = cls
                    best_class_score = score
    if best_class:
        inferred["class"] = best_class
        confidence += 0.3

    # 2. Try to determine engine layout
    for layout, keywords in ENGINE_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                inferred["engine"] = layout
                confidence += 0.15
                break
        if "engine" in inferred:
            break

    # 3. Try to determine drivetrain
    for dt, keywords in DRIVETRAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                inferred["drivetrain"] = dt
                confidence += 0.1
                break
        if "drivetrain" in inferred:
            break

    # Default drivetrain based on class
    if "drivetrain" not in inferred and "class" in inferred:
        if "FWD" not in name_lower:
            inferred["drivetrain"] = "RWD"  # Most race cars are RWD
            confidence += 0.05

    # 4. Check if historic
    is_historic = False
    for kw in HISTORIC_KEYWORDS:
        if kw in name_lower:
            is_historic = True
            break
    if is_historic and "class" not in inferred:
        # Try to narrow down historic type
        if any(kw in name_lower for kw in ["formula", "f1", "lotus", "brabham",
                                            "march", "tyrrell", "cooper", "brm"]):
            inferred["class"] = "Historic Formula / Open-Wheel"
        elif any(kw in name_lower for kw in ["962", "xjr", "787", "group c",
                                              "can-am", "lmp"]):
            inferred["class"] = "Group C / Can-Am / Historic Prototype"
        else:
            inferred["class"] = "Historic GT / Sports Car"
        confidence += 0.2

    # 5. Aero level
    for level, keywords in AERO_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                inferred["aero"] = level
                confidence += 0.1
                break
        if "aero" in inferred:
            break
    # Infer aero from class if not found
    if "aero" not in inferred and "class" in inferred:
        class_aero = {
            "GT3": "medium", "GTE / GT2": "high",
            "LMP2 / Prototype": "very_high", "Open-Wheel / Formula": "very_high",
            "Touring Car": "low", "Historic GT / Sports Car": "none",
            "Historic Formula / Open-Wheel": "none",
            "Group C / Can-Am / Historic Prototype": "high",
            "Stock Car / Oval": "low",
        }
        inferred["aero"] = class_aero.get(inferred["class"], "medium")

    # 6. ABS / TC inference
    if is_historic or any(kw in name_lower for kw in HISTORIC_KEYWORDS):
        inferred["has_abs"] = False
        inferred["has_tc"] = False
    elif inferred.get("class") in ("Open-Wheel / Formula", "Stock Car / Oval"):
        inferred["has_abs"] = False
        inferred["has_tc"] = False
    elif inferred.get("class") in ("LMP2 / Prototype",):
        inferred["has_abs"] = False
        inferred["has_tc"] = True
    else:
        inferred["has_abs"] = True
        inferred["has_tc"] = True

    # 7. Turbo
    inferred["turbo"] = any(kw in name_lower for kw in TURBO_KEYWORDS)

    # 8. Estimate weight and power from class
    class_defaults = {
        "GT3": (1300, 570), "GTE / GT2": (1250, 500),
        "LMP2 / Prototype": (930, 600), "Open-Wheel / Formula": (700, 500),
        "Touring Car": (1200, 380), "Historic GT / Sports Car": (1000, 350),
        "Historic Formula / Open-Wheel": (550, 380),
        "Group C / Can-Am / Historic Prototype": (870, 700),
        "Stock Car / Oval": (1450, 670),
    }
    if "class" in inferred:
        w, p = class_defaults.get(inferred["class"], (1200, 450))
        inferred.setdefault("weight", w)
        inferred.setdefault("power", p)

    # Build questions for anything we couldn't determine
    questions = []
    missing = []

    if "class" not in inferred:
        missing.append("class")
        questions.append(("class", "What type of car is this?", [
            "GT3 (modern GT racing)", "GTE / GT2 (factory GT)",
            "LMP2 / Prototype", "Open-Wheel / Formula",
            "Touring Car (BTCC, DTM, TCR)", "Historic GT / Sports Car",
            "Historic Formula / Open-Wheel",
            "Group C / Can-Am / Historic Prototype", "Stock Car / Oval",
        ]))

    if "engine" not in inferred:
        missing.append("engine")
        questions.append(("engine", "Where is the engine?", [
            "Front", "Mid", "Rear",
        ]))

    # Only ask about driver aids if we're not confident
    if confidence < 0.3:
        missing.append("has_abs")
        questions.append(("has_abs", "Does this car have ABS?", [
            "Yes", "No",
        ]))

    confidence = min(confidence, 1.0)

    return {
        "confidence": confidence,
        "inferred": inferred,
        "missing": missing,
        "questions": questions,
    }


# ---------------------------------------------------------------------------
# Track inference
# ---------------------------------------------------------------------------

TRACK_TYPE_KEYWORDS = {
    "High-Speed Circuit": [
        "high speed", "fast circuit", "monza", "spa", "silverstone", "le mans",
        "mugello", "watkins glen", "road america", "suzuka", "fuji",
        "hockenheim", "paul ricard",
    ],
    "Technical / Tight Circuit": [
        "technical", "tight", "twisty", "monaco", "hungaroring", "zandvoort",
        "barcelona", "imola", "albert park", "marina bay", "singapore",
    ],
    "Street Circuit": [
        "street", "city circuit", "baku", "long beach", "singapore",
        "jeddah", "miami", "las vegas",
    ],
    "Bumpy / Old-School Circuit": [
        "bumpy", "rough", "old school", "nordschleife", "nurburgring north",
        "green hell", "sebring", "cota", "bathurst", "mount panorama",
        "brands hatch", "goodwood", "portimao", "interlagos",
    ],
    "Oval / Banked Circuit": [
        "oval", "superspeedway", "daytona oval", "indianapolis oval",
        "talladega", "bristol", "martinsville", "richmond",
    ],
}

TRACK_SURFACE_KEYWORDS = {
    1: ["very bumpy", "concrete", "airfield", "sebring"],
    2: ["bumpy", "street", "old surface", "rough"],
    3: ["mixed", "some bumps", "average"],
    4: ["smooth", "new surface", "good surface", "modern"],
    5: ["glass smooth", "perfect", "billiard"],
}

TRACK_SPEED_KEYWORDS = {
    1: ["very slow", "tight", "monaco", "hairpins everywhere"],
    2: ["slow", "technical", "lots of corners"],
    3: ["mixed", "medium speed", "all-rounder"],
    4: ["fast", "high speed", "long straights"],
    5: ["very fast", "top speed", "monza", "le mans"],
}


def infer_track(name):
    """Try to infer track characteristics from its name.

    Returns similar structure to infer_car.
    """
    name_lower = name.lower().strip()
    inferred = {}
    confidence = 0.0

    # 1. Try to match track type
    best_type = None
    best_score = 0
    for ttype, keywords in TRACK_TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                score = len(kw)
                if score > best_score:
                    best_type = ttype
                    best_score = score
    if best_type:
        inferred["type"] = best_type
        confidence += 0.4

    # 2. Surface quality
    for quality, keywords in TRACK_SURFACE_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                inferred["surface"] = quality
                confidence += 0.1
                break
        if "surface" in inferred:
            break
    inferred.setdefault("surface", 3)

    # 3. Speed importance
    for speed, keywords in TRACK_SPEED_KEYWORDS.items():
        for kw in keywords:
            if kw in name_lower:
                inferred["top_speed"] = speed
                confidence += 0.1
                break
        if "top_speed" in inferred:
            break
    inferred.setdefault("top_speed", 3)

    # Default values
    inferred.setdefault("slow_corners", 4)
    inferred.setdefault("elevation", "medium")
    inferred.setdefault("length_km", 5.0)

    # Build questions
    questions = []
    missing = []

    if "type" not in inferred:
        missing.append("type")
        questions.append(("type", "What type of circuit is this?", [
            "High-Speed Circuit (long straights, fast sweepers)",
            "Technical / Tight Circuit (lots of slow corners)",
            "Street Circuit (walls close, bumpy surface)",
            "Bumpy / Old-School Circuit (rough surface, elevation)",
            "Oval / Banked Circuit",
        ]))

    confidence = min(confidence, 1.0)

    return {
        "confidence": confidence,
        "inferred": inferred,
        "missing": missing,
        "questions": questions,
    }


# ---------------------------------------------------------------------------
# User profile persistence — remember learned cars and tracks
# ---------------------------------------------------------------------------

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROFILE_DIR = os.path.join(_PROJECT_ROOT, "user_profiles")
PROFILE_FILE = os.path.join(PROFILE_DIR, "learned.json")


def _ensure_profile_dir():
    os.makedirs(PROFILE_DIR, exist_ok=True)


def load_learned():
    """Load previously learned car/track profiles."""
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {"cars": {}, "tracks": {}}


def save_learned(data):
    """Save learned car/track profiles."""
    _ensure_profile_dir()
    with open(PROFILE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def remember_car(name, profile):
    """Save a car profile for future use."""
    data = load_learned()
    data["cars"][name] = profile
    save_learned(data)


def remember_track(name, profile):
    """Save a track profile for future use."""
    data = load_learned()
    data["tracks"][name] = profile
    save_learned(data)


def get_learned_car(name):
    """Check if we've seen this car before."""
    data = load_learned()
    return data["cars"].get(name)


def get_learned_track(name):
    """Check if we've seen this track before."""
    data = load_learned()
    return data["tracks"].get(name)
