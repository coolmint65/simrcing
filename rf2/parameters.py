"""Setup parameter definitions.

Each parameter: (label, min, max, step, default, unit, tip).
This is the single source of truth for the 48 tunable parameters — the UI
reads it to build sliders, the knowledge base reads it to clamp values,
the .svm I/O reads it to map keys, etc.
"""


SETUP_CATEGORIES = {
    "Suspension": {
        "Front Ride Height": (20, 80, 1, 40, "mm",
            "Lower ride height reduces center of gravity and improves aero efficiency, "
            "but too low risks bottoming out. Start mid-range and lower gradually."),
        "Rear Ride Height": (20, 80, 1, 45, "mm",
            "Raising the rear relative to the front increases front downforce via rake angle. "
            "Keep within 5-15mm of front ride height for balance."),
        "Front Spring Rate": (20, 200, 5, 80, "N/mm",
            "Stiffer springs reduce body roll and improve responsiveness but can reduce grip "
            "on bumpy tracks. Softer springs improve mechanical grip."),
        "Rear Spring Rate": (20, 200, 5, 85, "N/mm",
            "Stiffer rear springs reduce traction under acceleration. A slightly stiffer rear "
            "vs front can reduce oversteer on turn entry."),
        "Front Anti-Roll Bar": (0, 50, 1, 15, "N/mm",
            "Stiffer front ARB reduces understeer mid-corner but can cause inside wheel lift. "
            "Softer improves mechanical grip on bumpy surfaces."),
        "Rear Anti-Roll Bar": (0, 50, 1, 12, "N/mm",
            "Stiffer rear ARB helps rotate the car but reduces rear traction. "
            "Balance front/rear ARBs to tune mid-corner behavior."),
        "Front Toe": (-2.0, 2.0, 0.05, 0.1, "deg",
            "Toe-out improves turn-in response but increases tire wear. "
            "Toe-in improves straight-line stability. Keep values small (0-0.3 deg)."),
        "Rear Toe": (-2.0, 2.0, 0.05, 0.2, "deg",
            "Slight toe-in at the rear improves stability under braking and corner entry. "
            "Too much toe-in causes drag and overheating."),
        "Front Camber": (-5.0, 0.0, 0.1, -3.0, "deg",
            "More negative camber improves cornering grip but reduces braking/acceleration grip. "
            "Check tire temps: inside should be ~5C hotter than outside."),
        "Rear Camber": (-5.0, 0.0, 0.1, -2.0, "deg",
            "Less negative camber than front is typical. Too much negative camber reduces "
            "rear traction under acceleration."),
    },
    "Dampers": {
        "Front Slow Bump": (1, 20, 1, 8, "clicks",
            "Controls compression at low shaft speeds (weight transfer). Higher values resist "
            "body roll but reduce grip over gentle undulations."),
        "Rear Slow Bump": (1, 20, 1, 8, "clicks",
            "Higher rear slow bump reduces squat under acceleration. "
            "Lower values improve rear traction on corner exit."),
        "Front Fast Bump": (1, 20, 1, 5, "clicks",
            "Controls compression over sharp bumps/kerbs. Lower values let the suspension "
            "absorb impacts better, keeping tire contact."),
        "Rear Fast Bump": (1, 20, 1, 5, "clicks",
            "Lower values improve rear grip over bumps. Too low can cause oscillation. "
            "Typically set 2-4 clicks below slow bump."),
        "Front Slow Rebound": (1, 20, 1, 10, "clicks",
            "Controls how quickly the suspension extends. Higher values improve stability "
            "during weight transfer but can cause jacking on bumpy tracks."),
        "Rear Slow Rebound": (1, 20, 1, 10, "clicks",
            "Higher rear rebound slows weight transfer to the front on turn-in, "
            "reducing oversteer. Lower values improve rotation."),
        "Front Fast Rebound": (1, 20, 1, 6, "clicks",
            "Controls extension speed over sharp bumps. Lower values help tires "
            "stay planted after hitting kerbs."),
        "Rear Fast Rebound": (1, 20, 1, 6, "clicks",
            "Similar to front — lower values keep rear tires in contact over bumps. "
            "Balance with fast bump for optimal control."),
    },
    "Aero": {
        "Front Wing Angle": (0, 40, 1, 15, "deg",
            "More front wing increases front downforce and reduces understeer. "
            "Increases drag. Balance with rear wing for neutral handling."),
        "Rear Wing Angle": (0, 40, 1, 20, "deg",
            "More rear wing increases rear grip and stability at high speed. "
            "Increases drag, reducing top speed. Lower for faster tracks."),
        "Front Splitter": (0, 10, 1, 5, "mm",
            "Extending the splitter increases front downforce. Very sensitive to ride height — "
            "lower ride height amplifies splitter effect."),
        "Rear Diffuser": (0, 10, 1, 5, "mm",
            "Larger diffuser setting generates more rear downforce with less drag penalty "
            "than the wing. Sensitive to rear ride height."),
        "Brake Ducts Front": (0, 100, 5, 50, "%",
            "More open ducts cool brakes faster but reduce front downforce. "
            "Open more for endurance, close for sprint qualifying."),
        "Brake Ducts Rear": (0, 100, 5, 50, "%",
            "Same trade-off as front ducts. Rear brakes typically run cooler "
            "so can often be more closed than fronts."),
    },
    "Tires": {
        "Front Tire Pressure": (100, 200, 5, 145, "kPa",
            "Higher pressure reduces rolling resistance but shrinks contact patch. "
            "Target 5-10 kPa increase from cold to hot. Check tire temps for even wear."),
        "Rear Tire Pressure": (100, 200, 5, 140, "kPa",
            "Slightly lower rear pressure than front improves rear traction. "
            "Monitor hot pressures — they should be 150-170 kPa typically."),
        "Front Tire Compound": (1, 5, 1, 3, "type",
            "1=Hardest, 5=Softest. Softer compounds grip better but wear faster. "
            "Consider stint length and track temperature."),
        "Rear Tire Compound": (1, 5, 1, 3, "type",
            "Usually matches front compound. In rare cases a harder rear compound "
            "can help with rear tire overheating issues."),
    },
    "Brakes": {
        "Brake Bias": (45.0, 70.0, 0.5, 57.0, "%",
            "Percentage of braking force on the front axle. Higher values improve stability "
            "but can cause front lock-ups. Lower values help rotation but risk rear lock-ups."),
        "Brake Pressure": (50, 100, 1, 90, "%",
            "Maximum braking force. Lower if you're locking up frequently. "
            "Higher values allow shorter braking zones with good pedal control."),
        "Front Brake Disc": (20, 40, 2, 28, "mm",
            "Thicker discs absorb more heat and resist fade but add unsprung weight. "
            "Use thicker discs for heavy braking circuits."),
        "Rear Brake Disc": (20, 40, 2, 24, "mm",
            "Rear discs can usually be thinner since less braking force goes to the rear. "
            "Saves weight without significant performance loss."),
    },
    "Differential": {
        "Preload": (10, 200, 5, 50, "Nm",
            "Higher preload creates a more locked differential at low torque. "
            "Improves traction exiting slow corners but reduces turn-in."),
        "Power (Accel) Lock": (0, 100, 5, 40, "%",
            "Controls locking under acceleration. Higher values put more power down "
            "but reduce corner-exit rotation. Lower values improve turn-in."),
        "Coast (Decel) Lock": (0, 100, 5, 20, "%",
            "Controls locking on deceleration/engine braking. Higher values stabilize "
            "the rear on turn-in. Lower values improve rotation."),
        "Viscous Lock": (0, 100, 5, 30, "%",
            "Speed-sensitive locking that smooths the differential behavior. "
            "Higher values provide more progressive locking characteristics."),
    },
    "Gearing": {
        "Final Drive": (2.0, 5.5, 0.01, 3.50, "ratio",
            "Lower ratio = higher top speed, less acceleration. Higher ratio = more acceleration, "
            "lower top speed. Start with a value that hits max RPM at the end of the longest straight."),
        "1st Gear": (2.5, 4.5, 0.01, 3.60, "ratio",
            "Set for the slowest corner on track. Should provide good acceleration "
            "out of hairpins without excessive wheelspin."),
        "2nd Gear": (1.8, 3.5, 0.01, 2.50, "ratio",
            "Bridge between 1st and 3rd. Aim for smooth RPM transitions "
            "between gears for consistent power delivery."),
        "3rd Gear": (1.3, 2.8, 0.01, 1.90, "ratio",
            "Often used in medium-speed corners. Set so you don't need to shift "
            "mid-corner in critical sections."),
        "4th Gear": (1.0, 2.3, 0.01, 1.55, "ratio",
            "Common gear for fast sweeping corners. Space evenly between 3rd and 5th "
            "for smooth power band usage."),
        "5th Gear": (0.8, 1.8, 0.01, 1.28, "ratio",
            "High-speed gear. Ensure you're in the power band on the main straights. "
            "Adjust spacing with 4th and 6th."),
        "6th Gear": (0.6, 1.5, 0.01, 1.08, "ratio",
            "Top gear. Set so the car just reaches or slightly exceeds the rev limiter "
            "at the end of the longest straight."),
    },
    "Engine": {
        "Engine Braking": (0, 100, 5, 50, "%",
            "Higher engine braking slows the car on lift-off, helping corner entry stability. "
            "Lower values reduce rear instability on deceleration."),
        "Throttle Map": (1, 5, 1, 3, "map",
            "1=Aggressive (full response), 5=Smooth (gradual). Lower maps give more immediate "
            "power but risk wheelspin. Higher maps improve traction control."),
        "Rev Limit": (8000, 15000, 100, 12000, "RPM",
            "Lower rev limits can improve fuel economy and engine life in endurance. "
            "Max RPM for qualifying and sprint races."),
        "Fuel Load": (10, 120, 1, 60, "liters",
            "More fuel adds weight, reducing grip and increasing tire wear. "
            "Calculate fuel needed for your stint and add a small buffer."),
    },
}


def get_default_setup():
    """Build a setup dict with every parameter at its default value."""
    setup = {}
    for cat, params in SETUP_CATEGORIES.items():
        setup[cat] = {}
        for name, (_vmin, _vmax, _step, default, _unit, _tip) in params.items():
            setup[cat][name] = default
    return setup


def setup_to_flat(setup):
    """Flatten nested setup dict to a list of (category, name, value) tuples."""
    items = []
    for cat in SETUP_CATEGORIES:
        if cat in setup:
            for name in SETUP_CATEGORIES[cat]:
                if name in setup[cat]:
                    items.append((cat, name, setup[cat][name]))
    return items


def clamp_param(cat, name, value):
    """Clamp a value to the (vmin, vmax) range for a parameter, preserving type."""
    info = SETUP_CATEGORIES.get(cat, {}).get(name)
    if not info:
        return value
    vmin, vmax, step = info[0], info[1], info[2]
    clamped = max(vmin, min(vmax, value))
    if isinstance(step, float):
        decimals = len(str(step).split('.')[-1])
        return round(clamped, decimals)
    return int(round(clamped))


def param_decimals(step):
    """Number of decimal places implied by a step."""
    if isinstance(step, float):
        return len(str(step).split('.')[-1])
    return 0
