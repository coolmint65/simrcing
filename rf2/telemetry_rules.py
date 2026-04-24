"""Rules that turn telemetry readings into setup suggestions.

The rules engine is pure — takes a TelemetryReading dict, returns a
list of Suggestion named tuples. This makes it testable without rF2
running, and lets the UI use it on manually-entered readings too.

Field glossary:
  tire_temp_inner/middle/outer: tire surface temperature (°C) across
    the width of the tire. Racing slicks should show inner ~5-10°C
    hotter than outer; wet tires more uniform.
  tire_pressure_cold/hot: kPa. Hot pressure should land in the car's
    optimal window after 3-4 laps.
  brake_temp: disc temperature (°C). Too hot = fading, too cold = no bite.
  wheel index: 0=FL, 1=FR, 2=RL, 3=RR throughout.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# Temperature targets (°C)
TIRE_INNER_VS_OUTER_TARGET = 8          # inner should be ~8°C hotter than outer
TIRE_INNER_VS_OUTER_TOLERANCE = 3
TIRE_LEFT_VS_RIGHT_TOLERANCE = 10
TIRE_FRONT_VS_REAR_TOLERANCE = 15
BRAKE_TEMP_HOT_THRESHOLD = 700
BRAKE_TEMP_COLD_THRESHOLD = 300
TIRE_PRESSURE_RISE_TARGET = 10          # kPa rise cold-to-hot
TIRE_PRESSURE_RISE_TOLERANCE = 5


WHEEL_NAMES = ("FL", "FR", "RL", "RR")


@dataclass
class WheelTelemetry:
    tire_temp_inner: Optional[float] = None
    tire_temp_middle: Optional[float] = None
    tire_temp_outer: Optional[float] = None
    tire_pressure_cold: Optional[float] = None
    tire_pressure_hot: Optional[float] = None
    brake_temp: Optional[float] = None


@dataclass
class TelemetryReading:
    wheels: Dict[str, WheelTelemetry] = field(default_factory=dict)
    source: str = "manual"                 # "manual" or "live"

    @classmethod
    def empty(cls):
        return cls(wheels={name: WheelTelemetry() for name in WHEEL_NAMES})


@dataclass
class Suggestion:
    priority: int                          # 1 (most important) to 10
    category: str                          # setup param category
    param: str                             # setup param name
    direction: str                         # "increase" or "decrease"
    reason: str                            # human-readable explanation


def analyze(reading: TelemetryReading) -> List[Suggestion]:
    """Run all rules against the reading and return sorted suggestions."""
    suggestions = []
    for rule in (_camber_rule,
                  _tire_pressure_rule,
                  _brake_duct_rule,
                  _left_right_balance_rule,
                  _front_rear_balance_rule):
        suggestions.extend(rule(reading))
    suggestions.sort(key=lambda s: s.priority)
    return suggestions


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------

def _camber_rule(reading):
    out = []
    for wheel_name, w in reading.wheels.items():
        if w.tire_temp_inner is None or w.tire_temp_outer is None:
            continue
        diff = w.tire_temp_inner - w.tire_temp_outer
        side = "Front" if wheel_name.startswith("F") else "Rear"
        target = TIRE_INNER_VS_OUTER_TARGET
        if diff > target + TIRE_INNER_VS_OUTER_TOLERANCE:
            out.append(Suggestion(
                priority=2,
                category="Suspension",
                param=f"{side} Camber",
                direction="increase",   # towards zero = less negative camber
                reason=(f"{wheel_name}: inner tire {diff:.1f}°C hotter than outer "
                         f"(target ~{target}°C). Reduce negative camber.")))
        elif diff < target - TIRE_INNER_VS_OUTER_TOLERANCE:
            out.append(Suggestion(
                priority=3,
                category="Suspension",
                param=f"{side} Camber",
                direction="decrease",   # more negative
                reason=(f"{wheel_name}: inner-outer delta only {diff:.1f}°C "
                         f"(target ~{target}°C). Increase negative camber.")))
    return out


def _tire_pressure_rule(reading):
    out = []
    for wheel_name, w in reading.wheels.items():
        if w.tire_pressure_cold is None or w.tire_pressure_hot is None:
            continue
        rise = w.tire_pressure_hot - w.tire_pressure_cold
        side = "Front" if wheel_name.startswith("F") else "Rear"
        if rise > TIRE_PRESSURE_RISE_TARGET + TIRE_PRESSURE_RISE_TOLERANCE:
            out.append(Suggestion(
                priority=2,
                category="Tires",
                param=f"{side} Tire Pressure",
                direction="increase",
                reason=(f"{wheel_name}: pressure rose {rise:.0f} kPa cold→hot "
                         f"(target ~{TIRE_PRESSURE_RISE_TARGET}). "
                         "Tire overworking — raise cold pressure to reduce rise, "
                         "or check camber/alignment.")))
        elif rise < TIRE_PRESSURE_RISE_TARGET - TIRE_PRESSURE_RISE_TOLERANCE:
            out.append(Suggestion(
                priority=4,
                category="Tires",
                param=f"{side} Tire Pressure",
                direction="decrease",
                reason=(f"{wheel_name}: pressure only rose {rise:.0f} kPa cold→hot "
                         f"(target ~{TIRE_PRESSURE_RISE_TARGET}). "
                         "Tire underworking — lower cold pressure.")))
    return out


def _brake_duct_rule(reading):
    out = []
    front_brakes = [reading.wheels["FL"].brake_temp, reading.wheels["FR"].brake_temp]
    rear_brakes = [reading.wheels["RL"].brake_temp, reading.wheels["RR"].brake_temp]
    front_valid = [t for t in front_brakes if t is not None]
    rear_valid = [t for t in rear_brakes if t is not None]

    if front_valid:
        avg_f = sum(front_valid) / len(front_valid)
        if avg_f > BRAKE_TEMP_HOT_THRESHOLD:
            out.append(Suggestion(
                priority=1,
                category="Aero",
                param="Brake Ducts Front",
                direction="increase",
                reason=(f"Front brake avg {avg_f:.0f}°C — risk of fade. "
                         "Open front ducts.")))
        elif avg_f < BRAKE_TEMP_COLD_THRESHOLD:
            out.append(Suggestion(
                priority=4,
                category="Aero",
                param="Brake Ducts Front",
                direction="decrease",
                reason=(f"Front brake avg {avg_f:.0f}°C — too cold for best bite. "
                         "Close front ducts.")))

    if rear_valid:
        avg_r = sum(rear_valid) / len(rear_valid)
        if avg_r > BRAKE_TEMP_HOT_THRESHOLD:
            out.append(Suggestion(
                priority=1,
                category="Aero",
                param="Brake Ducts Rear",
                direction="increase",
                reason=(f"Rear brake avg {avg_r:.0f}°C — risk of fade. "
                         "Open rear ducts.")))
        elif avg_r < BRAKE_TEMP_COLD_THRESHOLD:
            out.append(Suggestion(
                priority=4,
                category="Aero",
                param="Brake Ducts Rear",
                direction="decrease",
                reason=(f"Rear brake avg {avg_r:.0f}°C — too cold for best bite. "
                         "Close rear ducts.")))
    return out


def _left_right_balance_rule(reading):
    """If left-side tires are consistently hotter than right (or vice versa),
    weight distribution or alignment may be off."""
    out = []
    for (a, b, label) in (("FL", "FR", "Front"), ("RL", "RR", "Rear")):
        temps_a = _middle_or_avg(reading.wheels[a])
        temps_b = _middle_or_avg(reading.wheels[b])
        if temps_a is None or temps_b is None:
            continue
        diff = abs(temps_a - temps_b)
        if diff > TIRE_LEFT_VS_RIGHT_TOLERANCE:
            hotter = a if temps_a > temps_b else b
            out.append(Suggestion(
                priority=3,
                category="Suspension",
                param="Weight Distribution",
                direction="adjust",
                reason=(f"{label}: {hotter} is {diff:.1f}°C hotter than its pair. "
                         "Left-right imbalance — check weight distribution, "
                         "alignment, or setup symmetry.")))
    return out


def _front_rear_balance_rule(reading):
    """Front overheating vs rear suggests aero or brake bias issues."""
    out = []
    front = [_middle_or_avg(reading.wheels[w]) for w in ("FL", "FR")]
    rear = [_middle_or_avg(reading.wheels[w]) for w in ("RL", "RR")]
    front = [t for t in front if t is not None]
    rear = [t for t in rear if t is not None]
    if not front or not rear:
        return out
    avg_f = sum(front) / len(front)
    avg_r = sum(rear) / len(rear)
    diff = avg_f - avg_r
    if diff > TIRE_FRONT_VS_REAR_TOLERANCE:
        out.append(Suggestion(
            priority=2,
            category="Brakes",
            param="Brake Bias",
            direction="decrease",
            reason=(f"Front tires avg {diff:.1f}°C hotter than rear. "
                     "Consider less front brake bias, more rear wing, or "
                     "softer front ARB.")))
    elif diff < -TIRE_FRONT_VS_REAR_TOLERANCE:
        out.append(Suggestion(
            priority=2,
            category="Brakes",
            param="Brake Bias",
            direction="increase",
            reason=(f"Rear tires avg {-diff:.1f}°C hotter than front. "
                     "Consider more front brake bias or more front wing.")))
    return out


def _middle_or_avg(w):
    if w.tire_temp_middle is not None:
        return w.tire_temp_middle
    parts = [x for x in (w.tire_temp_inner, w.tire_temp_outer) if x is not None]
    if not parts:
        return None
    return sum(parts) / len(parts)
