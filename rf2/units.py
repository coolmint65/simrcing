"""Unit conversion — metric is always the canonical storage; this module
provides display-only conversion to imperial. Stored values never change."""


# Conversion factors: metric -> imperial
_FACTOR = {
    "mm": ("in", 1 / 25.4, 2),            # mm -> inches
    "kPa": ("psi", 0.145038, 1),          # kilopascals -> psi
    "N/mm": ("lbf/in", 5.71015, 0),       # N/mm -> lbf/in
    "Nm": ("lbf-ft", 0.737562, 1),        # newton-metre -> pound-foot
    "liters": ("gal", 0.264172, 1),       # litres -> US gallons
    # units with no conversion needed:
    "deg": ("deg", 1, 2),
    "clicks": ("clicks", 1, 0),
    "%": ("%", 1, 1),
    "type": ("type", 1, 0),
    "RPM": ("RPM", 1, 0),
    "ratio": ("ratio", 1, 2),
    "map": ("map", 1, 0),
}


def convert(value, unit, system="metric"):
    """Convert a stored (metric) value to the target system for display.

    Returns (converted_value, display_unit).
    """
    if system == "metric" or unit not in _FACTOR:
        return value, unit
    display_unit, factor, _decimals = _FACTOR[unit]
    return value * factor, display_unit


def format_value(value, unit, system="metric"):
    """Pretty-print a stored (metric) value for the requested unit system."""
    conv_value, display_unit = convert(value, unit, system)
    if unit in _FACTOR:
        _display, _factor, decimals = _FACTOR[unit]
        if system == "imperial" and decimals > 0:
            return f"{conv_value:.{decimals}f} {display_unit}"
    if isinstance(conv_value, float):
        return f"{conv_value:g} {display_unit}"
    return f"{conv_value} {display_unit}"


def supported_systems():
    return ("metric", "imperial")
