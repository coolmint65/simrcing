"""rFactor 2 car database — real cars with specific setup characteristics.
Each car has: class, engine layout, drivetrain, weight, power, aero level,
has_abs, has_tc, and setup bias hints that feed into baseline generation."""

# Engine layouts: front, mid, rear
# Drivetrains: RWD, FWD, AWD
# Aero levels: none, low, medium, high, very_high, extreme

CARS = {
    # ---- GT3 ----
    "BMW M4 GT3": {
        "class": "GT3", "engine": "front", "drivetrain": "RWD",
        "weight": 1310, "power": 590, "aero": "medium",
        "has_abs": True, "has_tc": True,
        "notes": "Front-engine GT3. More stable on the brakes than mid/rear-engine cars. "
                 "Can run slightly more rearward brake bias. Tends to understeer on entry.",
        "bias": {"Brakes": {"Brake Bias": -1.0}, "Suspension": {"Front Spring Rate": -5}},
    },
    "Porsche 911 GT3 R (991.2)": {
        "class": "GT3", "engine": "rear", "drivetrain": "RWD",
        "weight": 1300, "power": 550, "aero": "medium",
        "has_abs": True, "has_tc": True,
        "notes": "Rear-engine. Natural rear weight bias gives great traction but can snap "
                 "oversteer on lift-off. Needs more front downforce than most GT3s. "
                 "Run stiffer front springs to compensate for rear weight.",
        "bias": {
            "Aero": {"Front Wing Angle": 2, "Rear Wing Angle": -1},
            "Suspension": {"Front Spring Rate": 5, "Rear Spring Rate": -5},
            "Differential": {"Coast (Decel) Lock": 5},
        },
    },
    "Mercedes-AMG GT3": {
        "class": "GT3", "engine": "front", "drivetrain": "RWD",
        "weight": 1325, "power": 585, "aero": "medium",
        "has_abs": True, "has_tc": True,
        "notes": "Long wheelbase front-engine. Very stable platform, excellent on fast tracks. "
                 "Can struggle to rotate in tight corners. Benefits from aggressive diff settings.",
        "bias": {"Differential": {"Preload": -10, "Coast (Decel) Lock": -5}},
    },
    "McLaren 720S GT3": {
        "class": "GT3", "engine": "mid", "drivetrain": "RWD",
        "weight": 1290, "power": 570, "aero": "medium",
        "has_abs": True, "has_tc": True,
        "notes": "Mid-engine, well balanced. Good all-rounder. Slightly more aero-efficient "
                 "than rivals. Can run slightly less wing for same downforce.",
        "bias": {"Aero": {"Front Wing Angle": -1, "Rear Wing Angle": -1}},
    },
    "Ferrari 296 GT3": {
        "class": "GT3", "engine": "mid", "drivetrain": "RWD",
        "weight": 1295, "power": 600, "aero": "medium",
        "has_abs": True, "has_tc": True,
        "notes": "V6 turbo mid-engine. Strong power delivery, good aero platform. "
                 "Turbo lag at low RPM means smoother throttle maps help corner exit.",
        "bias": {"Engine": {"Throttle Map": 1}},
    },
    "Audi R8 LMS GT3 Evo II": {
        "class": "GT3", "engine": "mid", "drivetrain": "RWD",
        "weight": 1310, "power": 585, "aero": "medium",
        "has_abs": True, "has_tc": True,
        "notes": "Mid-engine V10 naturally aspirated. Linear power delivery, predictable handling. "
                 "Slightly heavier than rivals. Good on brakes due to V10 engine braking.",
        "bias": {"Engine": {"Engine Braking": 5}},
    },
    "Lamborghini Huracan GT3 EVO2": {
        "class": "GT3", "engine": "mid", "drivetrain": "RWD",
        "weight": 1310, "power": 580, "aero": "medium",
        "has_abs": True, "has_tc": True,
        "notes": "Similar platform to Audi R8 GT3. Mid-engine V10. "
                 "Slightly more aggressive aero. Good mechanical grip.",
        "bias": {"Aero": {"Rear Diffuser": 1}},
    },
    "Aston Martin Vantage GT3": {
        "class": "GT3", "engine": "front", "drivetrain": "RWD",
        "weight": 1315, "power": 575, "aero": "medium",
        "has_abs": True, "has_tc": True,
        "notes": "Front-engine V8 turbo. Good straight-line speed, stable on brakes. "
                 "Can struggle in very tight sections. Turbo delivery needs smooth inputs.",
        "bias": {"Engine": {"Throttle Map": 1}, "Brakes": {"Brake Bias": -0.5}},
    },

    # ---- GTE / GT2 ----
    "Porsche 911 RSR (2017)": {
        "class": "GTE / GT2", "engine": "rear", "drivetrain": "RWD",
        "weight": 1245, "power": 510, "aero": "high",
        "has_abs": True, "has_tc": True,
        "notes": "Rear-engine GTE. Incredible rear traction, notorious for entry understeer. "
                 "Needs aggressive front aero and soft front springs. Run minimum rear wing possible.",
        "bias": {
            "Aero": {"Front Wing Angle": 3, "Rear Wing Angle": -2},
            "Suspension": {"Front Spring Rate": -10},
        },
    },
    "Ferrari 488 GTE": {
        "class": "GTE / GT2", "engine": "mid", "drivetrain": "RWD",
        "weight": 1260, "power": 500, "aero": "high",
        "has_abs": True, "has_tc": True,
        "notes": "Mid-engine turbo V8 GTE. Well balanced, strong in medium-speed corners. "
                 "Turbo needs smooth throttle application.",
        "bias": {"Engine": {"Throttle Map": 1}},
    },
    "Corvette C8.R": {
        "class": "GTE / GT2", "engine": "mid", "drivetrain": "RWD",
        "weight": 1270, "power": 500, "aero": "high",
        "has_abs": True, "has_tc": True,
        "notes": "Mid-engine flat-plane V8. Excellent power delivery, strong on the brakes. "
                 "Good top speed. Slightly heavier than European rivals.",
        "bias": {"Brakes": {"Brake Pressure": 3}},
    },

    # ---- LMP2 / Prototype ----
    "Oreca 07 LMP2": {
        "class": "LMP2 / Prototype", "engine": "mid", "drivetrain": "RWD",
        "weight": 930, "power": 600, "aero": "very_high",
        "has_abs": False, "has_tc": True,
        "notes": "The dominant LMP2 chassis. Very aero dependent — ride height is critical. "
                 "Small changes to ride height have massive effects. No ABS, so brake modulation matters.",
        "bias": {},
    },
    "Dallara P217 LMP2": {
        "class": "LMP2 / Prototype", "engine": "mid", "drivetrain": "RWD",
        "weight": 930, "power": 600, "aero": "very_high",
        "has_abs": False, "has_tc": True,
        "notes": "Alternative LMP2 chassis. Slightly different aero characteristics to Oreca. "
                 "More forgiving at the limit but slightly less peak downforce.",
        "bias": {"Aero": {"Front Wing Angle": 1, "Rear Wing Angle": 1}},
    },

    # ---- Open-Wheel / Formula ----
    "Dallara F3": {
        "class": "Open-Wheel / Formula", "engine": "mid", "drivetrain": "RWD",
        "weight": 680, "power": 380, "aero": "high",
        "has_abs": False, "has_tc": False,
        "notes": "Formula 3 car. No driver aids. Great car to learn open-wheel racing. "
                 "Aero matters a lot but power is moderate so traction is manageable.",
        "bias": {
            "Suspension": {"Front Spring Rate": -10, "Rear Spring Rate": -10},
            "Engine": {"Throttle Map": 1},
        },
    },
    "Dallara IR-18 (IndyCar)": {
        "class": "Open-Wheel / Formula", "engine": "mid", "drivetrain": "RWD",
        "weight": 725, "power": 700, "aero": "very_high",
        "has_abs": False, "has_tc": False,
        "notes": "IndyCar. Massive power, big downforce. Very different road course vs oval setup. "
                 "No aids at all — demands respect. Push-to-pass system means power spikes.",
        "bias": {"Engine": {"Throttle Map": 1}},
    },

    # ---- Touring ----
    "BMW 320 TC (WTCC)": {
        "class": "Touring Car", "engine": "front", "drivetrain": "FWD",
        "weight": 1170, "power": 350, "aero": "low",
        "has_abs": True, "has_tc": False,
        "notes": "Front-wheel drive touring car. Completely different driving style — "
                 "trail braking rotates the car, throttle straightens it. "
                 "Needs very different diff approach. Brake bias more rearward than RWD.",
        "bias": {
            "Brakes": {"Brake Bias": -3.0},
            "Differential": {"Power (Accel) Lock": -15, "Coast (Decel) Lock": 10},
        },
    },
    "Chevrolet Cruze TC1 (WTCC)": {
        "class": "Touring Car", "engine": "front", "drivetrain": "FWD",
        "weight": 1170, "power": 360, "aero": "low",
        "has_abs": True, "has_tc": False,
        "notes": "Front-wheel drive touring car. Similar characteristics to BMW 320 TC. "
                 "Slightly more power means more torque steer to manage.",
        "bias": {
            "Brakes": {"Brake Bias": -3.0},
            "Differential": {"Power (Accel) Lock": -15, "Coast (Decel) Lock": 10},
            "Engine": {"Throttle Map": 1},
        },
    },

    # ---- Historic GT / Sports Car ----
    "Shelby Cobra 427": {
        "class": "Historic GT / Sports Car", "engine": "front", "drivetrain": "RWD",
        "weight": 1050, "power": 485, "aero": "none",
        "has_abs": False, "has_tc": False,
        "notes": "Massive V8 in a tiny body. Brutal power-to-weight. Will kill you if you're "
                 "not careful. Very soft suspension by modern standards. Needs smooth throttle "
                 "and conservative diff. The rear WILL step out on you.",
        "bias": {
            "Differential": {"Power (Accel) Lock": -10, "Preload": -10},
            "Engine": {"Throttle Map": 2},
            "Suspension": {"Rear Spring Rate": -5, "Rear Anti-Roll Bar": -2},
        },
    },
    "Ferrari 250 GTO": {
        "class": "Historic GT / Sports Car", "engine": "front", "drivetrain": "RWD",
        "weight": 1000, "power": 300, "aero": "none",
        "has_abs": False, "has_tc": False,
        "notes": "Front-engine V12. More refined than the Cobra but still no aids. "
                 "Better weight distribution. Drum brakes (if modeled) fade quickly. "
                 "Beautiful to drive when you respect it.",
        "bias": {
            "Brakes": {"Brake Pressure": -5},
            "Suspension": {"Front Spring Rate": -5, "Rear Spring Rate": -5},
        },
    },
    "Ford GT40 Mk I": {
        "class": "Historic GT / Sports Car", "engine": "mid", "drivetrain": "RWD",
        "weight": 1015, "power": 380, "aero": "none",
        "has_abs": False, "has_tc": False,
        "notes": "Mid-engine Le Mans winner. Better balanced than front-engine historics. "
                 "Low roofline means poor visibility. Surprisingly good brakes for the era. "
                 "Gearing is critical — original only had 4-speed.",
        "bias": {"Suspension": {"Front Ride Height": -3, "Rear Ride Height": -3}},
    },
    "Porsche 917K": {
        "class": "Historic GT / Sports Car", "engine": "rear", "drivetrain": "RWD",
        "weight": 820, "power": 600, "aero": "low",
        "has_abs": False, "has_tc": False,
        "notes": "Rear-engine flat-12 monster. Terrifying power-to-weight. Early aero was sketchy — "
                 "high-speed stability is the #1 concern. Legendary tail-happy handling. "
                 "Short wheelbase + rear engine + 600hp = constant attention required.",
        "bias": {
            "Aero": {"Rear Wing Angle": 3},
            "Suspension": {"Rear Toe": 0.10, "Rear Spring Rate": 5},
            "Differential": {"Power (Accel) Lock": -10},
            "Engine": {"Throttle Map": 2},
        },
    },
    "Jaguar E-Type Lightweight": {
        "class": "Historic GT / Sports Car", "engine": "front", "drivetrain": "RWD",
        "weight": 1000, "power": 300, "aero": "none",
        "has_abs": False, "has_tc": False,
        "notes": "Front-engine inline-6. Graceful and well balanced for its era. "
                 "Long nose means weight is forward — good on brakes, can understeer mid-corner.",
        "bias": {"Suspension": {"Front Anti-Roll Bar": -2}},
    },

    # ---- Historic Formula / Open-Wheel ----
    "Lotus 49": {
        "class": "Historic Formula / Open-Wheel", "engine": "rear", "drivetrain": "RWD",
        "weight": 530, "power": 410, "aero": "none",
        "has_abs": False, "has_tc": False,
        "notes": "DFV-powered, no wings in original spec. One of the most dangerous cars ever built. "
                 "The engine IS the chassis (stressed member). Zero aero grip, all mechanical. "
                 "Will spin without warning. Needs very conservative setup.",
        "bias": {
            "Suspension": {"Rear Toe": 0.10},
            "Differential": {"Power (Accel) Lock": -10},
            "Engine": {"Throttle Map": 2},
        },
    },
    "Lotus 79": {
        "class": "Historic Formula / Open-Wheel", "engine": "rear", "drivetrain": "RWD",
        "weight": 575, "power": 480, "aero": "high",
        "has_abs": False, "has_tc": False,
        "notes": "First ground-effect F1 car. MASSIVE downforce from the underbody tunnels. "
                 "Ride height is CRITICAL — too high and you lose all ground effect. "
                 "Very planted until the aero stalls, then snap oversteer.",
        "bias": {
            "Suspension": {"Front Ride Height": -8, "Rear Ride Height": -5},
            "Aero": {"Front Wing Angle": 4, "Rear Wing Angle": 6},
        },
    },
    "Brabham BT20": {
        "class": "Historic Formula / Open-Wheel", "engine": "rear", "drivetrain": "RWD",
        "weight": 510, "power": 310, "aero": "none",
        "has_abs": False, "has_tc": False,
        "notes": "1960s F1 car. No wings, pure mechanical grip. Less powerful than the Lotus 49 "
                 "but more forgiving. Good car to learn historic open-wheel racing.",
        "bias": {"Engine": {"Throttle Map": 1}},
    },
    "March 701": {
        "class": "Historic Formula / Open-Wheel", "engine": "rear", "drivetrain": "RWD",
        "weight": 545, "power": 430, "aero": "low",
        "has_abs": False, "has_tc": False,
        "notes": "Early wings era F1 car. Some downforce but crude aero. Better than no-wing cars "
                 "at high speed but still needs respect. Wings add some setup options.",
        "bias": {"Aero": {"Front Wing Angle": 2, "Rear Wing Angle": 3}},
    },

    # ---- Group C / Can-Am / Historic Prototype ----
    "Porsche 962C": {
        "class": "Group C / Can-Am / Historic Prototype", "engine": "rear", "drivetrain": "RWD",
        "weight": 850, "power": 700, "aero": "high",
        "has_abs": False, "has_tc": False,
        "notes": "Turbo flat-6 Group C car. Ground effect + turbo power = very fast but demanding. "
                 "Turbo lag is significant — need smooth throttle. Ride height critical for ground effect.",
        "bias": {
            "Suspension": {"Front Ride Height": -3, "Rear Ride Height": -3},
            "Engine": {"Throttle Map": 1},
        },
    },
    "Jaguar XJR-9": {
        "class": "Group C / Can-Am / Historic Prototype", "engine": "mid", "drivetrain": "RWD",
        "weight": 880, "power": 720, "aero": "high",
        "has_abs": False, "has_tc": False,
        "notes": "V12 Group C car. Massive naturally aspirated power — instant throttle response "
                 "unlike turbo rivals. More predictable power delivery but still brutal.",
        "bias": {"Engine": {"Engine Braking": 5}},
    },
    "Nissan R89C": {
        "class": "Group C / Can-Am / Historic Prototype", "engine": "mid", "drivetrain": "RWD",
        "weight": 870, "power": 680, "aero": "high",
        "has_abs": False, "has_tc": False,
        "notes": "Twin-turbo V8 Group C car. Good aero platform. Turbo delivery needs management. "
                 "Slightly heavier than Porsche but more stable.",
        "bias": {"Engine": {"Throttle Map": 1}},
    },

    # ---- Stock Car / Oval ----
    "Chevrolet Camaro ZL1 (NASCAR)": {
        "class": "Stock Car / Oval", "engine": "front", "drivetrain": "RWD",
        "weight": 1450, "power": 670, "aero": "low",
        "has_abs": False, "has_tc": False,
        "notes": "NASCAR Cup car. V8 pushrod engine. Heavy, powerful, crude. "
                 "Setup is completely different for road course vs oval. "
                 "On ovals: stagger (different tire sizes L/R) is key. On road courses: brake bias matters most.",
        "bias": {},
    },
    "Ford Mustang (NASCAR)": {
        "class": "Stock Car / Oval", "engine": "front", "drivetrain": "RWD",
        "weight": 1450, "power": 670, "aero": "low",
        "has_abs": False, "has_tc": False,
        "notes": "NASCAR Cup car. Similar to Camaro but slightly different aero profile. "
                 "Marginally better top speed, slightly less downforce.",
        "bias": {"Aero": {"Front Wing Angle": -1}},
    },
}


def find_car(query):
    """Fuzzy search for a car by name. Returns list of (name, data) tuples sorted by relevance."""
    query_lower = query.lower().strip()
    if not query_lower:
        return []

    exact = []
    starts = []
    contains = []
    word_match = []

    for name, data in CARS.items():
        name_lower = name.lower()
        if query_lower == name_lower:
            exact.append((name, data))
        elif name_lower.startswith(query_lower):
            starts.append((name, data))
        elif query_lower in name_lower:
            contains.append((name, data))
        else:
            # Check if all query words appear somewhere
            query_words = query_lower.split()
            if all(w in name_lower or w in data.get("class", "").lower()
                   or w in data.get("notes", "").lower() for w in query_words):
                word_match.append((name, data))

    return exact + starts + contains + word_match
