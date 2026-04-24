"""Physics calculations for setup work.

Real equations (not heuristics) for weight transfer, natural frequency,
and aero balance. Car-specific constants (mass, wheelbase, CoG, track
width, tire radius) come from cars.json where available, falling back to
class-level defaults defined here.

Units: meters and kilograms internally; most inputs accept the units the
user naturally types (mm for geometry, N/mm for springs) and convert.
"""

import math


G = 9.80665  # m/s²


# ---------------------------------------------------------------------------
# Class-level physics defaults
# ---------------------------------------------------------------------------

# Each entry: mass_kg, wheelbase_mm, cog_height_mm, track_width_mm,
#             tire_radius_mm, front_weight_pct
PHYSICS_DEFAULTS_BY_CLASS = {
    "GT3":                                 (1300, 2700, 450, 1600, 330, 47),
    "GTE / GT2":                           (1245, 2700, 430, 1600, 330, 47),
    "LMP2 / Prototype":                    (930,  2950, 350, 1680, 330, 45),
    "Open-Wheel / Formula":                (700,  3150, 300, 1500, 330, 45),
    "Touring Car":                         (1250, 2700, 500, 1600, 320, 60),
    "Historic GT / Sports Car":            (1100, 2500, 500, 1500, 330, 50),
    "Historic Formula / Open-Wheel":       (560,  2400, 350, 1500, 310, 48),
    "Group C / Can-Am / Historic Prototype": (870, 2700, 360, 1650, 330, 46),
    "Stock Car / Oval":                    (1500, 2800, 520, 1650, 360, 52),
}


def physics_for_car(car_data):
    """Return a dict with mass_kg, wheelbase_mm, cog_height_mm,
    track_width_mm, tire_radius_mm, front_weight_pct.

    Per-car overrides from cars.json take precedence over class defaults.
    """
    cls = car_data.get("class") if car_data else None
    mass, wb, cog, trk, tr, fwp = PHYSICS_DEFAULTS_BY_CLASS.get(
        cls, PHYSICS_DEFAULTS_BY_CLASS["GT3"])
    if car_data and "weight" in car_data:
        mass = car_data["weight"]
    out = {
        "mass_kg": mass,
        "wheelbase_mm": car_data.get("wheelbase_mm", wb) if car_data else wb,
        "cog_height_mm": car_data.get("cog_height_mm", cog) if car_data else cog,
        "track_width_mm": car_data.get("track_width_mm", trk) if car_data else trk,
        "tire_radius_mm": car_data.get("tire_radius_mm", tr) if car_data else tr,
        "front_weight_pct": car_data.get("front_weight_pct", fwp) if car_data else fwp,
    }
    return out


# ---------------------------------------------------------------------------
# Weight transfer
# ---------------------------------------------------------------------------

def longitudinal_weight_transfer(mass_kg, cog_height_mm, wheelbase_mm, decel_g):
    """Longitudinal load transfer under braking (or acceleration).

    ΔW = m · g · (h / L) · a_g

    Returns delta load (N). Positive = load moving to the front axle
    (braking); negative under acceleration.
    """
    return mass_kg * G * (cog_height_mm / wheelbase_mm) * decel_g


def lateral_weight_transfer_axle(axle_mass_kg, cog_height_mm, track_width_mm,
                                  lateral_g):
    """Per-axle lateral load transfer in a steady-state corner.

    Assumes the roll center is at ground level for simplicity (good enough
    for first-order intuition). For full accuracy you'd split the transfer
    between the sprung and unsprung components, but that needs roll-
    center-height data we don't have.
    """
    return axle_mass_kg * G * (cog_height_mm / track_width_mm) * lateral_g


def static_corner_loads(mass_kg, front_weight_pct):
    """Static vertical load (N) on each corner assuming left-right symmetry."""
    front_total = mass_kg * G * (front_weight_pct / 100.0)
    rear_total = mass_kg * G * (1 - front_weight_pct / 100.0)
    return {
        "FL": front_total / 2, "FR": front_total / 2,
        "RL": rear_total / 2,  "RR": rear_total / 2,
    }


def dynamic_corner_loads(mass_kg, front_weight_pct, cog_height_mm,
                          wheelbase_mm, track_width_mm,
                          long_g=0.0, lat_g=0.0):
    """Corner loads under combined longitudinal + lateral accel.

    Positive long_g = braking (forward transfer). Positive lat_g =
    cornering with right-side loaded (equivalent to a left-hand turn).
    """
    static = static_corner_loads(mass_kg, front_weight_pct)
    long_delta = longitudinal_weight_transfer(mass_kg, cog_height_mm, wheelbase_mm, long_g)
    per_front = long_delta / 2
    per_rear = long_delta / 2

    front_total = (static["FL"] + static["FR"]) + long_delta
    rear_total = (static["RL"] + static["RR"]) - long_delta
    front_axle_mass = front_total / G
    rear_axle_mass = rear_total / G

    front_lat = lateral_weight_transfer_axle(front_axle_mass, cog_height_mm,
                                              track_width_mm, lat_g)
    rear_lat = lateral_weight_transfer_axle(rear_axle_mass, cog_height_mm,
                                              track_width_mm, lat_g)

    return {
        "FL": static["FL"] + per_front - front_lat,
        "FR": static["FR"] + per_front + front_lat,
        "RL": static["RL"] - per_rear - rear_lat,
        "RR": static["RR"] - per_rear + rear_lat,
    }


# ---------------------------------------------------------------------------
# Suspension frequency
# ---------------------------------------------------------------------------

def natural_frequency(spring_rate_n_per_mm, corner_mass_kg,
                      motion_ratio=1.0):
    """Undamped natural frequency of a quarter-car oscillator.

    f = (1/2π) · sqrt(k_wheel / m_corner)

    `motion_ratio` lets the caller account for the ratio between spring
    travel and wheel travel. Wheel rate = spring rate × (motion ratio)².
    For most modern race cars the motion ratio is ~1.0; for some double-
    wishbone setups it's ~0.7-0.9.
    """
    k_wheel_n_per_m = spring_rate_n_per_mm * 1000 * motion_ratio ** 2
    if corner_mass_kg <= 0 or k_wheel_n_per_m <= 0:
        raise ValueError("mass and spring rate must be positive")
    return math.sqrt(k_wheel_n_per_m / corner_mass_kg) / (2 * math.pi)


def target_spring_rate(target_hz, corner_mass_kg, motion_ratio=1.0):
    """Inverse of `natural_frequency`: given a target frequency in Hz,
    what spring rate (N/mm) do you need?

    Typical race-car targets: GT3 ~2.5-3.5 Hz, LMP2 ~4-5 Hz, F1 ~5-7 Hz,
    road car ~1-1.5 Hz. Higher Hz = stiffer/more responsive but less
    mechanical grip over bumps.
    """
    if target_hz <= 0 or corner_mass_kg <= 0:
        raise ValueError("frequency and mass must be positive")
    omega = 2 * math.pi * target_hz
    k_wheel = omega ** 2 * corner_mass_kg
    k_spring = k_wheel / (motion_ratio ** 2 * 1000)
    return round(k_spring, 1)


# ---------------------------------------------------------------------------
# Aero
# ---------------------------------------------------------------------------

def aero_balance(front_downforce_n, rear_downforce_n):
    """Front aero balance as % of total downforce."""
    total = front_downforce_n + rear_downforce_n
    if total <= 0:
        return 50.0
    return 100.0 * front_downforce_n / total


def estimate_downforce(front_wing_deg, rear_wing_deg,
                        front_splitter_mm, rear_diffuser_mm,
                        speed_kph, aero_level="medium"):
    """Very rough downforce estimate in newtons. Real aero maps are
    non-linear and car-specific; this returns first-order deltas useful
    for seeing which direction a change moves balance, NOT a physical
    prediction of actual downforce.

    aero_level scales the base coefficients:
      none (1960s GT)    -> x0.2
      low (touring/oval) -> x0.6
      medium (GT3)       -> x1.0
      high (GTE)         -> x1.4
      very_high (LMP)    -> x2.0
      extreme (F1)       -> x3.0
    """
    level_scale = {
        "none": 0.2, "low": 0.6, "medium": 1.0,
        "high": 1.4, "very_high": 2.0, "extreme": 3.0,
    }.get((aero_level or "medium").lower(), 1.0)

    speed_ms = speed_kph / 3.6
    q = 0.5 * 1.225 * speed_ms ** 2       # dynamic pressure (Pa) at sea level

    # Coefficient × reference area (Cl·A) per unit of setting.
    # These constants are calibrated so a "medium" car with typical
    # settings produces realistic downforce in the hundreds-of-kg range
    # at 200 km/h.
    front_cla = (front_wing_deg * 0.015 + front_splitter_mm * 0.010) * level_scale
    rear_cla = (rear_wing_deg * 0.020 + rear_diffuser_mm * 0.012) * level_scale

    return front_cla * q, rear_cla * q
