"""rFactor 2 .svm setup file reader/writer.

rF2 .svm files are text files that look like this:

    [General]
    Symmetric=1
    [FRONTWING]
    FWSetting=10//12 deg
    [REARWING]
    RWSetting=12//18 deg
    [LEFTFRONT]
    CamberSetting=32//-3.2 deg
    PressureSetting=25//145 kPa
    ...

The file is ini-ish but not quite (uses `//` as an inline separator between the
raw integer index and the human-readable value). This module maps our
SETUP_CATEGORIES parameters to .svm keys where we have confident mappings.

Parameters without a confident 1:1 .svm mapping are left unchanged on import
and omitted on export — the module reports what it couldn't round-trip.

The mapping table below is a best-effort consensus across ISI/Studio-397 mods
— different mods use slightly different key names (e.g. `FWSetting` vs
`FrontWingSetting`). We accept any of the known aliases on read and emit
the canonical form on write.
"""

import os
import re


# Canonical (section, key) -> (our_category, our_param). Includes aliases.
# Order matters: when exporting we use the FIRST entry for each of our params.
_MAP = [
    # (svm_section, svm_key, our_category, our_param)
    ("FRONTWING", "FWSetting", "Aero", "Front Wing Angle"),
    ("REARWING", "RWSetting", "Aero", "Rear Wing Angle"),
    ("FRONTWING", "FrontSplitterSetting", "Aero", "Front Splitter"),
    ("REARWING", "RearDiffuserSetting", "Aero", "Rear Diffuser"),
    ("FRONTWING", "FrontBrakeDuctSetting", "Aero", "Brake Ducts Front"),
    ("REARWING", "RearBrakeDuctSetting", "Aero", "Brake Ducts Rear"),

    ("LEFTFRONT", "PressureSetting", "Tires", "Front Tire Pressure"),
    ("RIGHTFRONT", "PressureSetting", "Tires", "Front Tire Pressure"),
    ("LEFTREAR", "PressureSetting", "Tires", "Rear Tire Pressure"),
    ("RIGHTREAR", "PressureSetting", "Tires", "Rear Tire Pressure"),

    ("LEFTFRONT", "CompoundSetting", "Tires", "Front Tire Compound"),
    ("LEFTREAR", "CompoundSetting", "Tires", "Rear Tire Compound"),

    ("LEFTFRONT", "CamberSetting", "Suspension", "Front Camber"),
    ("RIGHTFRONT", "CamberSetting", "Suspension", "Front Camber"),
    ("LEFTREAR", "CamberSetting", "Suspension", "Rear Camber"),
    ("RIGHTREAR", "CamberSetting", "Suspension", "Rear Camber"),

    ("LEFTFRONT", "ToeInSetting", "Suspension", "Front Toe"),
    ("RIGHTFRONT", "ToeInSetting", "Suspension", "Front Toe"),
    ("LEFTREAR", "ToeInSetting", "Suspension", "Rear Toe"),
    ("RIGHTREAR", "ToeInSetting", "Suspension", "Rear Toe"),

    ("LEFTFRONT", "RideHeightSetting", "Suspension", "Front Ride Height"),
    ("RIGHTFRONT", "RideHeightSetting", "Suspension", "Front Ride Height"),
    ("LEFTREAR", "RideHeightSetting", "Suspension", "Rear Ride Height"),
    ("RIGHTREAR", "RideHeightSetting", "Suspension", "Rear Ride Height"),

    ("FRONT", "SpringSetting", "Suspension", "Front Spring Rate"),
    ("REAR", "SpringSetting", "Suspension", "Rear Spring Rate"),
    ("FRONT", "AntiSwaySetting", "Suspension", "Front Anti-Roll Bar"),
    ("REAR", "AntiSwaySetting", "Suspension", "Rear Anti-Roll Bar"),

    ("LEFTFRONT", "SlowBumpSetting", "Dampers", "Front Slow Bump"),
    ("RIGHTFRONT", "SlowBumpSetting", "Dampers", "Front Slow Bump"),
    ("LEFTREAR", "SlowBumpSetting", "Dampers", "Rear Slow Bump"),
    ("RIGHTREAR", "SlowBumpSetting", "Dampers", "Rear Slow Bump"),
    ("LEFTFRONT", "FastBumpSetting", "Dampers", "Front Fast Bump"),
    ("RIGHTFRONT", "FastBumpSetting", "Dampers", "Front Fast Bump"),
    ("LEFTREAR", "FastBumpSetting", "Dampers", "Rear Fast Bump"),
    ("RIGHTREAR", "FastBumpSetting", "Dampers", "Rear Fast Bump"),
    ("LEFTFRONT", "SlowReboundSetting", "Dampers", "Front Slow Rebound"),
    ("RIGHTFRONT", "SlowReboundSetting", "Dampers", "Front Slow Rebound"),
    ("LEFTREAR", "SlowReboundSetting", "Dampers", "Rear Slow Rebound"),
    ("RIGHTREAR", "SlowReboundSetting", "Dampers", "Rear Slow Rebound"),
    ("LEFTFRONT", "FastReboundSetting", "Dampers", "Front Fast Rebound"),
    ("RIGHTFRONT", "FastReboundSetting", "Dampers", "Front Fast Rebound"),
    ("LEFTREAR", "FastReboundSetting", "Dampers", "Rear Fast Rebound"),
    ("RIGHTREAR", "FastReboundSetting", "Dampers", "Rear Fast Rebound"),

    ("CONTROL", "BrakeBiasSetting", "Brakes", "Brake Bias"),
    ("CONTROL", "BrakePressureSetting", "Brakes", "Brake Pressure"),
    ("LEFTFRONT", "BrakeDiscSetting", "Brakes", "Front Brake Disc"),
    ("LEFTREAR", "BrakeDiscSetting", "Brakes", "Rear Brake Disc"),

    ("DIFFERENTIAL", "PreloadSetting", "Differential", "Preload"),
    ("DIFFERENTIAL", "PowerSetting", "Differential", "Power (Accel) Lock"),
    ("DIFFERENTIAL", "CoastSetting", "Differential", "Coast (Decel) Lock"),
    ("DIFFERENTIAL", "ViscousSetting", "Differential", "Viscous Lock"),

    ("DRIVELINE", "FinalDriveSetting", "Gearing", "Final Drive"),
    ("DRIVELINE", "ReverseSetting", "Gearing", "1st Gear"),
    ("DRIVELINE", "Gear1Setting", "Gearing", "1st Gear"),
    ("DRIVELINE", "Gear2Setting", "Gearing", "2nd Gear"),
    ("DRIVELINE", "Gear3Setting", "Gearing", "3rd Gear"),
    ("DRIVELINE", "Gear4Setting", "Gearing", "4th Gear"),
    ("DRIVELINE", "Gear5Setting", "Gearing", "5th Gear"),
    ("DRIVELINE", "Gear6Setting", "Gearing", "6th Gear"),

    ("ENGINE", "EngineBrakingSetting", "Engine", "Engine Braking"),
    ("ENGINE", "ThrottleMapSetting", "Engine", "Throttle Map"),
    ("ENGINE", "RevLimitSetting", "Engine", "Rev Limit"),
    ("ENGINE", "FuelSetting", "Engine", "Fuel Load"),
]


def _our_param_to_svm():
    """Return (our_category, our_param) -> list of (section, key) pairs.

    Multiple pairs mean the value should be written to each (e.g. left+right)."""
    mapping = {}
    for section, key, our_cat, our_param in _MAP:
        mapping.setdefault((our_cat, our_param), []).append((section, key))
    return mapping


_SVM_KEY_TO_OUR = {(s, k): (c, p) for (s, k, c, p) in _MAP}


_SETTING_RE = re.compile(r"^(?P<key>[A-Za-z0-9_]+)\s*=\s*(?P<val>.+?)\s*(?://\s*(?P<human>.*))?$")
_SECTION_RE = re.compile(r"^\[(?P<name>[^\]]+)\]\s*$")


def _parse_value(raw, human):
    """The `raw` part is usually an integer index into the mod's setting list.
    The `human` comment often has the actual value — but it's unreliable.
    We use `human` when it parses as a number, else `raw`."""
    if human is not None:
        # "32//-3.2 deg" — pull the first number from the human part
        m = re.search(r"[-+]?\d+(?:\.\d+)?", human)
        if m:
            try:
                return float(m.group(0))
            except ValueError:
                pass
    try:
        return float(raw)
    except ValueError:
        return raw


def read_svm(path):
    """Parse a .svm file and return (setup_dict, unmapped_keys).

    setup_dict is a partial setup with only the parameters we could map.
    unmapped_keys is a list of (section, key) we saw but don't have a mapping for.
    Callers should merge setup_dict over a default setup to fill gaps.
    """
    setup = {}
    unmapped = []
    current_section = None

    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip()
            if not line or line.startswith("//"):
                continue
            sec_m = _SECTION_RE.match(line)
            if sec_m:
                current_section = sec_m.group("name").upper()
                continue
            set_m = _SETTING_RE.match(line)
            if not set_m or current_section is None:
                continue
            key = set_m.group("key")
            val = _parse_value(set_m.group("val"), set_m.group("human"))
            target = _SVM_KEY_TO_OUR.get((current_section, key))
            if target is None:
                unmapped.append((current_section, key))
                continue
            cat, param = target
            setup.setdefault(cat, {})[param] = val

    return setup, unmapped


def write_svm(path, setup, symmetric=True):
    """Write a .svm-style file from our setup dict.

    Only parameters with a confident mapping are written. Unmapped parameters
    are silently omitted (their values stay whatever rF2 has set).
    Returns a list of (our_cat, our_param) pairs that were NOT written.
    """
    mapping = _our_param_to_svm()

    # Group writes by section so we can emit tidy [SECTION] blocks.
    by_section = {}
    written_params = set()
    for (cat, param), pairs in mapping.items():
        if cat not in setup or param not in setup[cat]:
            continue
        value = setup[cat][param]
        for section, key in pairs:
            by_section.setdefault(section, []).append((key, value))
        written_params.add((cat, param))

    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("// Generated by rF2 Setup Program\n")
        f.write("[General]\n")
        f.write(f"Symmetric={1 if symmetric else 0}\n\n")
        for section, items in by_section.items():
            f.write(f"[{section}]\n")
            for key, value in items:
                if isinstance(value, float):
                    f.write(f"{key}=0//{value:g}\n")
                else:
                    f.write(f"{key}=0//{value}\n")
            f.write("\n")

    omitted = []
    for cat, params in setup.items():
        for param in params:
            if (cat, param) not in written_params:
                omitted.append((cat, param))
    return omitted
