"""Fuel and gearing calculators.

Fuel: laps * consumption_per_lap + safety_margin.
Gearing: pick a final drive that hits the target top speed at or just below
the rev limiter, assuming the 6th-gear ratio from the loaded setup.
"""

import math


SAFETY_LAP_DEFAULT = 1.0   # extra laps of fuel as a buffer


def fuel_needed(laps, consumption_per_lap, safety_laps=SAFETY_LAP_DEFAULT):
    """Return liters needed for the stint. Rounds up to the nearest 0.5 L.

    Raises ValueError on negative inputs.
    """
    if laps < 0 or consumption_per_lap < 0 or safety_laps < 0:
        raise ValueError("fuel inputs must be non-negative")
    raw = (laps + safety_laps) * consumption_per_lap
    return math.ceil(raw * 2) / 2


def final_drive_for_top_speed(target_kph, rev_limit_rpm, top_gear_ratio,
                              tire_radius_m=0.33):
    """Compute the final drive ratio that produces `target_kph` at `rev_limit_rpm`
    in top gear.

    target_kph: desired top speed at rev limit, km/h
    rev_limit_rpm: engine rev limit
    top_gear_ratio: the highest gear ratio (e.g. 6th gear in the setup)
    tire_radius_m: rear tire rolling radius in meters (default ~GT3 slick)

    speed (m/s) = (rpm / 60) * (2*pi*r) / (top_gear * final_drive)
    Solve for final_drive.
    """
    if target_kph <= 0 or rev_limit_rpm <= 0 or top_gear_ratio <= 0 or tire_radius_m <= 0:
        raise ValueError("gearing inputs must be positive")
    target_ms = target_kph / 3.6
    circumference = 2 * math.pi * tire_radius_m
    wheel_rpm_at_limit = target_ms * 60 / circumference
    engine_rpm_per_wheel_rpm = rev_limit_rpm / wheel_rpm_at_limit
    # engine_rpm_per_wheel_rpm = top_gear_ratio * final_drive
    final_drive = engine_rpm_per_wheel_rpm / top_gear_ratio
    return round(final_drive, 2)


def top_speed_for_final_drive(final_drive, rev_limit_rpm, top_gear_ratio,
                              tire_radius_m=0.33):
    """Inverse of `final_drive_for_top_speed`. Returns km/h."""
    if final_drive <= 0 or rev_limit_rpm <= 0 or top_gear_ratio <= 0 or tire_radius_m <= 0:
        raise ValueError("gearing inputs must be positive")
    circumference = 2 * math.pi * tire_radius_m
    wheel_rpm_at_limit = rev_limit_rpm / (top_gear_ratio * final_drive)
    ms = wheel_rpm_at_limit * circumference / 60
    return round(ms * 3.6, 1)
