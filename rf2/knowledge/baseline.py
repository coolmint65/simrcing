"""Baseline generators: combine car class + track type deltas + car/track specific bias
+ optional rF2 meta tweaks into a complete setup."""

from rf2.parameters import SETUP_CATEGORIES, get_default_setup
from rf2.knowledge.car_classes import CAR_CLASSES
from rf2.knowledge.track_types import TRACK_TYPES
from rf2.knowledge.problems import HANDLING_PROBLEMS


def _apply_delta(setup, cat, name, delta):
    """Add delta to setup[cat][name], clamped to bounds and snapped to step."""
    if cat not in setup or name not in setup[cat]:
        return
    info = SETUP_CATEGORIES.get(cat, {}).get(name)
    if not info:
        return
    vmin, vmax, step = info[:3]
    new_val = setup[cat][name] + delta
    new_val = max(vmin, min(vmax, new_val))
    if isinstance(step, float):
        decimals = len(str(step).split('.')[-1])
        new_val = round(round((new_val - vmin) / step) * step + vmin, decimals)
    else:
        new_val = int(round((new_val - vmin) / step) * step + vmin)
    setup[cat][name] = new_val


def generate_baseline(car_class_name, track_type_name):
    """Generate a baseline setup by combining car class defaults with track type deltas.

    Returns (setup_dict, tips_list, warnings_list).
    """
    car_class = CAR_CLASSES.get(car_class_name)
    track_type = TRACK_TYPES.get(track_type_name)

    if not car_class:
        return None, [], [f"Unknown car class: {car_class_name}"]

    setup = get_default_setup()

    for cat, params in car_class["defaults"].items():
        for name, val in params.items():
            if cat in setup and name in setup[cat]:
                setup[cat][name] = val

    tips = []
    warnings = []

    if track_type:
        tips.extend(track_type["tips"])
        for cat, params in track_type.get("deltas", {}).items():
            for name, delta in params.items():
                _apply_delta(setup, cat, name, delta)

    traits = car_class.get("traits", [])
    if "no_abs" in traits:
        warnings.append("This car has NO ABS. Use moderate brake pressure and forward "
                        "brake bias. Threshold braking technique is essential.")
    if "no_tc" in traits:
        warnings.append("This car has NO traction control. Be smooth on throttle application, "
                        "especially on corner exit. Use a smoother throttle map.")
    if "minimal_aero" in traits:
        warnings.append("This car has MINIMAL aerodynamic downforce. All grip comes from "
                        "mechanical sources (tires, suspension). Focus on springs, dampers, and tire pressures.")
    if "aero_sensitive" in traits:
        warnings.append("This car is AERO SENSITIVE. Small changes to ride height and wing angles "
                        "have large effects. Make small adjustments (1-2 units at a time).")
    if "extreme_power_to_grip_ratio" in traits or "high_power_to_grip_ratio" in traits:
        warnings.append("HIGH POWER-TO-GRIP RATIO. This car will bite if you're aggressive "
                        "with throttle. Smooth inputs are critical for survival.")

    return setup, tips, warnings


def generate_smart_baseline(car_data, track_data=None, apply_meta=True):
    """Generate a baseline from specific car + track data (from rf2.cars/rf2.tracks).

    Returns (setup_dict, tips_list, warnings_list, meta_changes_list).
    """
    car_class_name = car_data.get("class", "GT3")
    car_class = CAR_CLASSES.get(car_class_name)
    if not car_class:
        for cls_name in CAR_CLASSES:
            if car_class_name.lower() in cls_name.lower():
                car_class = CAR_CLASSES[cls_name]
                break
        if not car_class:
            car_class = list(CAR_CLASSES.values())[0]

    setup = get_default_setup()
    tips = []
    warnings = []

    for cat, params in car_class["defaults"].items():
        for name, val in params.items():
            if cat in setup and name in setup[cat]:
                setup[cat][name] = val

    for cat, params in car_data.get("bias", {}).items():
        for name, delta in params.items():
            _apply_delta(setup, cat, name, delta)

    if track_data:
        track_type_name = track_data.get("type", "")
        track_type = TRACK_TYPES.get(track_type_name)
        if track_type:
            tips.extend(track_type["tips"])
            for cat, params in track_type.get("deltas", {}).items():
                for name, delta in params.items():
                    _apply_delta(setup, cat, name, delta)

        for cat, params in track_data.get("bias", {}).items():
            for name, delta in params.items():
                _apply_delta(setup, cat, name, delta)

        if track_data.get("notes"):
            tips.insert(0, f"TRACK NOTE: {track_data['notes']}")

    meta_changes = []
    if apply_meta:
        from rf2.meta import apply_meta_to_setup
        meta_changes = apply_meta_to_setup(setup, car_data)

    if not car_data.get("has_abs", True):
        warnings.append("This car has NO ABS. Use moderate brake pressure and forward "
                        "brake bias. Threshold braking technique is essential.")
    if not car_data.get("has_tc", True):
        warnings.append("This car has NO traction control. Be smooth on throttle application, "
                        "especially on corner exit.")
    if car_data.get("aero") == "none":
        warnings.append("This car has NO aerodynamic downforce. All grip comes from "
                        "mechanical sources. Focus on springs, dampers, and tire pressures.")
    elif car_data.get("aero") in ("very_high", "extreme"):
        warnings.append("This car is AERO SENSITIVE. Small ride height changes have large effects.")
    if car_data.get("notes"):
        warnings.insert(0, f"CAR: {car_data['notes']}")

    return setup, tips, warnings, meta_changes


def get_problem_recommendations(problem_name):
    """Return the diagnosis info and list of recommended changes for a handling problem."""
    return HANDLING_PROBLEMS.get(problem_name)
