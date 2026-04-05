"""rFactor 2 setup knowledge base — car classes, track types, handling problems,
baseline presets, and step-by-step workflow guidance."""


# ---------------------------------------------------------------------------
# Car class definitions — physics characteristics & typical parameter ranges
# ---------------------------------------------------------------------------

CAR_CLASSES = {
    "GT3": {
        "description": "Modern GT3 race cars (e.g. BMW M4 GT3, Porsche 911 GT3 R, McLaren 720S GT3). "
                       "Mid-high downforce, ABS, traction control available. ~500-600 HP, ~1300 kg.",
        "traits": ["high_power", "medium_downforce", "abs_available", "tc_available", "rear_engine_bias"],
        "defaults": {
            "Suspension": {
                "Front Ride Height": 50, "Rear Ride Height": 55,
                "Front Spring Rate": 90, "Rear Spring Rate": 95,
                "Front Anti-Roll Bar": 12, "Rear Anti-Roll Bar": 10,
                "Front Toe": 0.05, "Rear Toe": 0.20,
                "Front Camber": -3.5, "Rear Camber": -2.5,
            },
            "Dampers": {
                "Front Slow Bump": 8, "Rear Slow Bump": 7,
                "Front Fast Bump": 4, "Rear Fast Bump": 4,
                "Front Slow Rebound": 10, "Rear Slow Rebound": 9,
                "Front Fast Rebound": 5, "Rear Fast Rebound": 5,
            },
            "Aero": {
                "Front Wing Angle": 8, "Rear Wing Angle": 12,
                "Front Splitter": 4, "Rear Diffuser": 6,
                "Brake Ducts Front": 40, "Brake Ducts Rear": 30,
            },
            "Tires": {
                "Front Tire Pressure": 150, "Rear Tire Pressure": 145,
                "Front Tire Compound": 3, "Rear Tire Compound": 3,
            },
            "Brakes": {
                "Brake Bias": 57.0, "Brake Pressure": 90,
                "Front Brake Disc": 30, "Rear Brake Disc": 26,
            },
            "Differential": {
                "Preload": 60, "Power (Accel) Lock": 45,
                "Coast (Decel) Lock": 15, "Viscous Lock": 30,
            },
            "Gearing": {
                "Final Drive": 3.40, "1st Gear": 3.50, "2nd Gear": 2.40,
                "3rd Gear": 1.82, "4th Gear": 1.48, "5th Gear": 1.24, "6th Gear": 1.06,
            },
            "Engine": {
                "Engine Braking": 55, "Throttle Map": 3,
                "Rev Limit": 12500, "Fuel Load": 60,
            },
        },
    },
    "GTE / GT2": {
        "description": "Factory GTE / GT2 cars (e.g. Porsche 911 RSR, Ferrari 488 GTE, Corvette C8.R). "
                       "Higher downforce than GT3, more factory-tuned, ~500 HP, ~1250 kg.",
        "traits": ["high_power", "high_downforce", "abs_available", "tc_available"],
        "defaults": {
            "Suspension": {
                "Front Ride Height": 45, "Rear Ride Height": 52,
                "Front Spring Rate": 100, "Rear Spring Rate": 105,
                "Front Anti-Roll Bar": 14, "Rear Anti-Roll Bar": 12,
                "Front Toe": 0.05, "Rear Toe": 0.15,
                "Front Camber": -3.8, "Rear Camber": -2.8,
            },
            "Dampers": {
                "Front Slow Bump": 9, "Rear Slow Bump": 8,
                "Front Fast Bump": 5, "Rear Fast Bump": 4,
                "Front Slow Rebound": 11, "Rear Slow Rebound": 10,
                "Front Fast Rebound": 6, "Rear Fast Rebound": 5,
            },
            "Aero": {
                "Front Wing Angle": 12, "Rear Wing Angle": 16,
                "Front Splitter": 5, "Rear Diffuser": 7,
                "Brake Ducts Front": 35, "Brake Ducts Rear": 25,
            },
            "Tires": {
                "Front Tire Pressure": 148, "Rear Tire Pressure": 143,
                "Front Tire Compound": 3, "Rear Tire Compound": 3,
            },
            "Brakes": {
                "Brake Bias": 58.0, "Brake Pressure": 92,
                "Front Brake Disc": 32, "Rear Brake Disc": 28,
            },
            "Differential": {
                "Preload": 70, "Power (Accel) Lock": 50,
                "Coast (Decel) Lock": 20, "Viscous Lock": 35,
            },
            "Gearing": {
                "Final Drive": 3.30, "1st Gear": 3.40, "2nd Gear": 2.35,
                "3rd Gear": 1.78, "4th Gear": 1.45, "5th Gear": 1.20, "6th Gear": 1.02,
            },
            "Engine": {
                "Engine Braking": 50, "Throttle Map": 3,
                "Rev Limit": 12000, "Fuel Load": 55,
            },
        },
    },
    "LMP2 / Prototype": {
        "description": "Le Mans Prototype 2 and similar closed-cockpit prototypes. "
                       "Very high downforce, ~600 HP, ~930 kg. Aero-dependent.",
        "traits": ["high_power", "very_high_downforce", "aero_sensitive", "lightweight"],
        "defaults": {
            "Suspension": {
                "Front Ride Height": 35, "Rear Ride Height": 45,
                "Front Spring Rate": 120, "Rear Spring Rate": 130,
                "Front Anti-Roll Bar": 18, "Rear Anti-Roll Bar": 14,
                "Front Toe": 0.0, "Rear Toe": 0.15,
                "Front Camber": -3.2, "Rear Camber": -2.2,
            },
            "Dampers": {
                "Front Slow Bump": 10, "Rear Slow Bump": 9,
                "Front Fast Bump": 5, "Rear Fast Bump": 5,
                "Front Slow Rebound": 12, "Rear Slow Rebound": 11,
                "Front Fast Rebound": 6, "Rear Fast Rebound": 6,
            },
            "Aero": {
                "Front Wing Angle": 18, "Rear Wing Angle": 24,
                "Front Splitter": 6, "Rear Diffuser": 8,
                "Brake Ducts Front": 30, "Brake Ducts Rear": 20,
            },
            "Tires": {
                "Front Tire Pressure": 155, "Rear Tire Pressure": 150,
                "Front Tire Compound": 3, "Rear Tire Compound": 3,
            },
            "Brakes": {
                "Brake Bias": 56.0, "Brake Pressure": 95,
                "Front Brake Disc": 32, "Rear Brake Disc": 28,
            },
            "Differential": {
                "Preload": 40, "Power (Accel) Lock": 35,
                "Coast (Decel) Lock": 15, "Viscous Lock": 25,
            },
            "Gearing": {
                "Final Drive": 3.10, "1st Gear": 3.20, "2nd Gear": 2.20,
                "3rd Gear": 1.70, "4th Gear": 1.38, "5th Gear": 1.15, "6th Gear": 0.98,
            },
            "Engine": {
                "Engine Braking": 45, "Throttle Map": 2,
                "Rev Limit": 13000, "Fuel Load": 50,
            },
        },
    },
    "Open-Wheel / Formula": {
        "description": "Single-seater open-wheel cars (F1-style, F3, Formula E, etc). "
                       "Extreme downforce, very light, very responsive to setup changes.",
        "traits": ["extreme_downforce", "very_lightweight", "aero_sensitive", "open_wheel", "no_abs"],
        "defaults": {
            "Suspension": {
                "Front Ride Height": 25, "Rear Ride Height": 40,
                "Front Spring Rate": 140, "Rear Spring Rate": 150,
                "Front Anti-Roll Bar": 20, "Rear Anti-Roll Bar": 16,
                "Front Toe": -0.05, "Rear Toe": 0.10,
                "Front Camber": -3.0, "Rear Camber": -1.8,
            },
            "Dampers": {
                "Front Slow Bump": 12, "Rear Slow Bump": 10,
                "Front Fast Bump": 6, "Rear Fast Bump": 5,
                "Front Slow Rebound": 14, "Rear Slow Rebound": 12,
                "Front Fast Rebound": 7, "Rear Fast Rebound": 6,
            },
            "Aero": {
                "Front Wing Angle": 22, "Rear Wing Angle": 28,
                "Front Splitter": 7, "Rear Diffuser": 9,
                "Brake Ducts Front": 25, "Brake Ducts Rear": 20,
            },
            "Tires": {
                "Front Tire Pressure": 155, "Rear Tire Pressure": 150,
                "Front Tire Compound": 3, "Rear Tire Compound": 3,
            },
            "Brakes": {
                "Brake Bias": 55.0, "Brake Pressure": 95,
                "Front Brake Disc": 28, "Rear Brake Disc": 24,
            },
            "Differential": {
                "Preload": 30, "Power (Accel) Lock": 50,
                "Coast (Decel) Lock": 10, "Viscous Lock": 20,
            },
            "Gearing": {
                "Final Drive": 2.80, "1st Gear": 3.80, "2nd Gear": 2.60,
                "3rd Gear": 1.95, "4th Gear": 1.55, "5th Gear": 1.28, "6th Gear": 1.08,
            },
            "Engine": {
                "Engine Braking": 60, "Throttle Map": 2,
                "Rev Limit": 14000, "Fuel Load": 50,
            },
        },
    },
    "Touring Car": {
        "description": "Touring cars (BTCC, DTM, TCR, V8 Supercars). Heavier, less downforce, "
                       "mechanical grip dependent. ~300-500 HP, ~1100-1400 kg.",
        "traits": ["medium_power", "low_downforce", "mechanical_grip", "heavy"],
        "defaults": {
            "Suspension": {
                "Front Ride Height": 50, "Rear Ride Height": 55,
                "Front Spring Rate": 70, "Rear Spring Rate": 75,
                "Front Anti-Roll Bar": 10, "Rear Anti-Roll Bar": 8,
                "Front Toe": 0.10, "Rear Toe": 0.25,
                "Front Camber": -2.8, "Rear Camber": -1.8,
            },
            "Dampers": {
                "Front Slow Bump": 7, "Rear Slow Bump": 6,
                "Front Fast Bump": 4, "Rear Fast Bump": 3,
                "Front Slow Rebound": 9, "Rear Slow Rebound": 8,
                "Front Fast Rebound": 5, "Rear Fast Rebound": 4,
            },
            "Aero": {
                "Front Wing Angle": 5, "Rear Wing Angle": 8,
                "Front Splitter": 3, "Rear Diffuser": 3,
                "Brake Ducts Front": 50, "Brake Ducts Rear": 40,
            },
            "Tires": {
                "Front Tire Pressure": 145, "Rear Tire Pressure": 140,
                "Front Tire Compound": 3, "Rear Tire Compound": 3,
            },
            "Brakes": {
                "Brake Bias": 58.0, "Brake Pressure": 85,
                "Front Brake Disc": 28, "Rear Brake Disc": 24,
            },
            "Differential": {
                "Preload": 50, "Power (Accel) Lock": 40,
                "Coast (Decel) Lock": 20, "Viscous Lock": 30,
            },
            "Gearing": {
                "Final Drive": 3.70, "1st Gear": 3.60, "2nd Gear": 2.50,
                "3rd Gear": 1.90, "4th Gear": 1.55, "5th Gear": 1.28, "6th Gear": 1.08,
            },
            "Engine": {
                "Engine Braking": 50, "Throttle Map": 3,
                "Rev Limit": 11000, "Fuel Load": 55,
            },
        },
    },
    "Historic GT / Sports Car": {
        "description": "Classic GT and sports racing cars (Shelby Cobra, Ferrari 250 GTO, Porsche 917, "
                       "Ford GT40, Jaguar E-Type). No driver aids, narrow tires, live axles possible, "
                       "minimal aero. Mechanical grip is everything.",
        "traits": ["no_abs", "no_tc", "narrow_tires", "minimal_aero", "mechanical_grip",
                   "high_power_to_grip_ratio"],
        "defaults": {
            "Suspension": {
                "Front Ride Height": 55, "Rear Ride Height": 60,
                "Front Spring Rate": 50, "Rear Spring Rate": 55,
                "Front Anti-Roll Bar": 6, "Rear Anti-Roll Bar": 5,
                "Front Toe": 0.10, "Rear Toe": 0.30,
                "Front Camber": -2.0, "Rear Camber": -1.5,
            },
            "Dampers": {
                "Front Slow Bump": 5, "Rear Slow Bump": 5,
                "Front Fast Bump": 3, "Rear Fast Bump": 3,
                "Front Slow Rebound": 7, "Rear Slow Rebound": 7,
                "Front Fast Rebound": 4, "Rear Fast Rebound": 4,
            },
            "Aero": {
                "Front Wing Angle": 0, "Rear Wing Angle": 0,
                "Front Splitter": 0, "Rear Diffuser": 0,
                "Brake Ducts Front": 60, "Brake Ducts Rear": 50,
            },
            "Tires": {
                "Front Tire Pressure": 140, "Rear Tire Pressure": 135,
                "Front Tire Compound": 3, "Rear Tire Compound": 3,
            },
            "Brakes": {
                "Brake Bias": 60.0, "Brake Pressure": 80,
                "Front Brake Disc": 26, "Rear Brake Disc": 22,
            },
            "Differential": {
                "Preload": 30, "Power (Accel) Lock": 25,
                "Coast (Decel) Lock": 10, "Viscous Lock": 15,
            },
            "Gearing": {
                "Final Drive": 3.80, "1st Gear": 3.20, "2nd Gear": 2.20,
                "3rd Gear": 1.70, "4th Gear": 1.40, "5th Gear": 1.15, "6th Gear": 0.95,
            },
            "Engine": {
                "Engine Braking": 40, "Throttle Map": 4,
                "Rev Limit": 9000, "Fuel Load": 70,
            },
        },
    },
    "Historic Formula / Open-Wheel": {
        "description": "Classic open-wheel racers (Lotus 49, Brabham BT20, March 701, etc). "
                       "High power, minimal to no wings (early), no aids, treacherous handling.",
        "traits": ["no_abs", "no_tc", "open_wheel", "minimal_aero", "very_lightweight",
                   "extreme_power_to_grip_ratio"],
        "defaults": {
            "Suspension": {
                "Front Ride Height": 40, "Rear Ride Height": 50,
                "Front Spring Rate": 60, "Rear Spring Rate": 65,
                "Front Anti-Roll Bar": 8, "Rear Anti-Roll Bar": 6,
                "Front Toe": -0.05, "Rear Toe": 0.20,
                "Front Camber": -2.5, "Rear Camber": -1.5,
            },
            "Dampers": {
                "Front Slow Bump": 6, "Rear Slow Bump": 5,
                "Front Fast Bump": 3, "Rear Fast Bump": 3,
                "Front Slow Rebound": 8, "Rear Slow Rebound": 7,
                "Front Fast Rebound": 4, "Rear Fast Rebound": 4,
            },
            "Aero": {
                "Front Wing Angle": 2, "Rear Wing Angle": 4,
                "Front Splitter": 0, "Rear Diffuser": 0,
                "Brake Ducts Front": 55, "Brake Ducts Rear": 45,
            },
            "Tires": {
                "Front Tire Pressure": 140, "Rear Tire Pressure": 135,
                "Front Tire Compound": 3, "Rear Tire Compound": 3,
            },
            "Brakes": {
                "Brake Bias": 56.0, "Brake Pressure": 78,
                "Front Brake Disc": 24, "Rear Brake Disc": 22,
            },
            "Differential": {
                "Preload": 25, "Power (Accel) Lock": 30,
                "Coast (Decel) Lock": 10, "Viscous Lock": 15,
            },
            "Gearing": {
                "Final Drive": 3.50, "1st Gear": 3.40, "2nd Gear": 2.30,
                "3rd Gear": 1.75, "4th Gear": 1.42, "5th Gear": 1.18, "6th Gear": 1.00,
            },
            "Engine": {
                "Engine Braking": 45, "Throttle Map": 4,
                "Rev Limit": 10000, "Fuel Load": 65,
            },
        },
    },
    "Group C / Can-Am / Historic Prototype": {
        "description": "Classic prototypes (Porsche 962, Jaguar XJR-9, Nissan R89C, Can-Am cars). "
                       "Very high power, developing aero, ground effect possible. Fast and dangerous.",
        "traits": ["very_high_power", "high_downforce", "aero_sensitive", "no_tc",
                   "ground_effect", "turbo_possible"],
        "defaults": {
            "Suspension": {
                "Front Ride Height": 35, "Rear Ride Height": 45,
                "Front Spring Rate": 100, "Rear Spring Rate": 110,
                "Front Anti-Roll Bar": 14, "Rear Anti-Roll Bar": 10,
                "Front Toe": 0.0, "Rear Toe": 0.15,
                "Front Camber": -3.0, "Rear Camber": -2.2,
            },
            "Dampers": {
                "Front Slow Bump": 8, "Rear Slow Bump": 7,
                "Front Fast Bump": 4, "Rear Fast Bump": 4,
                "Front Slow Rebound": 10, "Rear Slow Rebound": 9,
                "Front Fast Rebound": 5, "Rear Fast Rebound": 5,
            },
            "Aero": {
                "Front Wing Angle": 14, "Rear Wing Angle": 20,
                "Front Splitter": 5, "Rear Diffuser": 7,
                "Brake Ducts Front": 35, "Brake Ducts Rear": 25,
            },
            "Tires": {
                "Front Tire Pressure": 150, "Rear Tire Pressure": 145,
                "Front Tire Compound": 3, "Rear Tire Compound": 3,
            },
            "Brakes": {
                "Brake Bias": 57.0, "Brake Pressure": 88,
                "Front Brake Disc": 30, "Rear Brake Disc": 26,
            },
            "Differential": {
                "Preload": 45, "Power (Accel) Lock": 40,
                "Coast (Decel) Lock": 15, "Viscous Lock": 25,
            },
            "Gearing": {
                "Final Drive": 3.00, "1st Gear": 3.30, "2nd Gear": 2.25,
                "3rd Gear": 1.72, "4th Gear": 1.40, "5th Gear": 1.16, "6th Gear": 0.98,
            },
            "Engine": {
                "Engine Braking": 50, "Throttle Map": 3,
                "Rev Limit": 11000, "Fuel Load": 60,
            },
        },
    },
    "Stock Car / Oval": {
        "description": "NASCAR-style stock cars, V8 Supercars, or oval-racing machines. "
                       "Heavy, high power, minimal aero adjustability, setup is about mechanical balance.",
        "traits": ["high_power", "heavy", "low_downforce", "mechanical_grip", "no_abs", "no_tc"],
        "defaults": {
            "Suspension": {
                "Front Ride Height": 55, "Rear Ride Height": 60,
                "Front Spring Rate": 65, "Rear Spring Rate": 70,
                "Front Anti-Roll Bar": 12, "Rear Anti-Roll Bar": 8,
                "Front Toe": 0.05, "Rear Toe": 0.20,
                "Front Camber": -3.0, "Rear Camber": -1.5,
            },
            "Dampers": {
                "Front Slow Bump": 7, "Rear Slow Bump": 6,
                "Front Fast Bump": 4, "Rear Fast Bump": 3,
                "Front Slow Rebound": 9, "Rear Slow Rebound": 8,
                "Front Fast Rebound": 5, "Rear Fast Rebound": 4,
            },
            "Aero": {
                "Front Wing Angle": 6, "Rear Wing Angle": 10,
                "Front Splitter": 3, "Rear Diffuser": 3,
                "Brake Ducts Front": 55, "Brake Ducts Rear": 45,
            },
            "Tires": {
                "Front Tire Pressure": 140, "Rear Tire Pressure": 135,
                "Front Tire Compound": 3, "Rear Tire Compound": 3,
            },
            "Brakes": {
                "Brake Bias": 60.0, "Brake Pressure": 82,
                "Front Brake Disc": 28, "Rear Brake Disc": 24,
            },
            "Differential": {
                "Preload": 60, "Power (Accel) Lock": 50,
                "Coast (Decel) Lock": 25, "Viscous Lock": 35,
            },
            "Gearing": {
                "Final Drive": 3.90, "1st Gear": 3.50, "2nd Gear": 2.40,
                "3rd Gear": 1.85, "4th Gear": 1.50, "5th Gear": 1.25, "6th Gear": 1.05,
            },
            "Engine": {
                "Engine Braking": 45, "Throttle Map": 3,
                "Rev Limit": 9500, "Fuel Load": 65,
            },
        },
    },
}



# ---------------------------------------------------------------------------
# Track type modifiers — adjustments applied on top of a car class baseline
# Values are DELTAS (added to the baseline)
# ---------------------------------------------------------------------------

TRACK_TYPES = {
    "High-Speed Circuit": {
        "description": "Long straights, fast sweepers (Monza, Le Mans, Spa). "
                       "Prioritize low drag, top speed, high-speed stability.",
        "tips": [
            "Lower wing angles to reduce drag and improve top speed.",
            "Lower ride height for better aero efficiency on smooth surfaces.",
            "Stiffer springs/dampers — high-speed stability matters more than bump absorption.",
            "Longer gear ratios — you need top speed on the straights.",
            "Slightly more rear wing bias for stability in fast sweepers.",
        ],
        "deltas": {
            "Aero": {"Front Wing Angle": -4, "Rear Wing Angle": -5},
            "Suspension": {
                "Front Ride Height": -5, "Rear Ride Height": -5,
                "Front Spring Rate": 10, "Rear Spring Rate": 10,
            },
            "Gearing": {"Final Drive": -0.20},
            "Brakes": {"Brake Pressure": 3},
        },
    },
    "Technical / Tight Circuit": {
        "description": "Lots of slow corners, chicanes, hairpins (Monaco, Zandvoort, Bathurst). "
                       "Prioritize mechanical grip, rotation, traction out of slow corners.",
        "tips": [
            "Higher wing angles — drag penalty matters less with short straights.",
            "Softer springs for better mechanical grip over kerbs.",
            "Lower diff preload for sharper turn-in at low speeds.",
            "Shorter gear ratios — you spend more time accelerating than at top speed.",
            "More front camber for tight cornering grip.",
        ],
        "deltas": {
            "Aero": {"Front Wing Angle": 4, "Rear Wing Angle": 5},
            "Suspension": {
                "Front Spring Rate": -10, "Rear Spring Rate": -10,
                "Front Camber": -0.3,
            },
            "Differential": {"Preload": -15, "Power (Accel) Lock": -5},
            "Gearing": {"Final Drive": 0.20},
        },
    },
    "Street Circuit": {
        "description": "Bumpy surfaces, walls close, no runoff (Monaco, Baku, Long Beach). "
                       "Forgiving setup, compliant suspension, good low-speed grip.",
        "tips": [
            "Softer springs and dampers — the bumps will destroy your tires otherwise.",
            "Higher ride height to avoid bottoming on uneven surfaces.",
            "Lower brake pressure — locking up into a wall ends your race.",
            "More rear toe for stability — walls punish snap oversteer.",
            "Slightly softer ARBs for better bump compliance.",
        ],
        "deltas": {
            "Suspension": {
                "Front Ride Height": 5, "Rear Ride Height": 5,
                "Front Spring Rate": -15, "Rear Spring Rate": -15,
                "Front Anti-Roll Bar": -3, "Rear Anti-Roll Bar": -3,
                "Rear Toe": 0.05,
            },
            "Dampers": {
                "Front Slow Bump": -2, "Rear Slow Bump": -2,
                "Front Fast Bump": -2, "Rear Fast Bump": -2,
            },
            "Brakes": {"Brake Pressure": -5},
        },
    },
    "Bumpy / Old-School Circuit": {
        "description": "Rough surfaces, elevation changes, old tarmac (Nordschleife, Sebring, "
                       "COTA). Need compliant suspension without being too soft.",
        "tips": [
            "Softer fast bump damping — let the suspension absorb the jolts.",
            "Higher ride height to prevent bottoming over crests.",
            "Lower slow rebound to prevent the car 'jacking up' over repeated bumps.",
            "More tire pressure tolerance — expect pressure to build with rough surface.",
            "Consider a harder tire compound if pressures are spiking.",
        ],
        "deltas": {
            "Suspension": {
                "Front Ride Height": 5, "Rear Ride Height": 5,
                "Front Spring Rate": -5, "Rear Spring Rate": -5,
            },
            "Dampers": {
                "Front Fast Bump": -2, "Rear Fast Bump": -2,
                "Front Slow Rebound": -2, "Rear Slow Rebound": -2,
                "Front Fast Rebound": -2, "Rear Fast Rebound": -2,
            },
            "Tires": {"Front Tire Pressure": -5, "Rear Tire Pressure": -5},
        },
    },
    "Oval / Banked Circuit": {
        "description": "Banked turns, high sustained speeds, left-turn bias (Daytona, Indianapolis). "
                       "Asymmetric setup considerations.",
        "tips": [
            "Stiffen the right side (outside) springs for banking support.",
            "Lower left-side ride height if possible for turn-in.",
            "More rear wing for stability through the banking.",
            "Higher diff locking — you need consistent power through long turns.",
            "Brake bias slightly rearward — you're braking less but need rotation.",
        ],
        "deltas": {
            "Aero": {"Rear Wing Angle": 3},
            "Suspension": {"Rear Spring Rate": 10},
            "Differential": {"Power (Accel) Lock": 10, "Preload": 10},
            "Brakes": {"Brake Bias": -1.5},
            "Gearing": {"Final Drive": -0.15},
        },
    },
    "Wet / Damp Conditions": {
        "description": "Rain or damp track. Drastically different approach — "
                       "everything about mechanical grip and driver confidence.",
        "tips": [
            "Soften everything — springs, ARBs, dampers. Mechanical grip is king.",
            "More rear wing for stability. Drag doesn't matter as much at lower speeds.",
            "Higher ride height — aquaplaning risk decreases with more clearance.",
            "Lower brake pressure and more forward bias — rears lock very easily.",
            "Lower diff locking — the tires need freedom to find grip independently.",
            "Reduce engine braking — sudden deceleration breaks rear traction.",
            "Smoother throttle map — wheelspin is the biggest enemy.",
        ],
        "deltas": {
            "Suspension": {
                "Front Ride Height": 8, "Rear Ride Height": 8,
                "Front Spring Rate": -20, "Rear Spring Rate": -20,
                "Front Anti-Roll Bar": -5, "Rear Anti-Roll Bar": -5,
            },
            "Dampers": {
                "Front Slow Bump": -3, "Rear Slow Bump": -3,
                "Front Fast Bump": -2, "Rear Fast Bump": -2,
            },
            "Aero": {"Front Wing Angle": 3, "Rear Wing Angle": 6},
            "Differential": {
                "Preload": -20, "Power (Accel) Lock": -15,
                "Coast (Decel) Lock": -10,
            },
            "Brakes": {"Brake Bias": 2.0, "Brake Pressure": -10},
            "Engine": {"Engine Braking": -15, "Throttle Map": 2},
        },
    },
}



# ---------------------------------------------------------------------------
# Handling problem diagnosis — maps symptoms to recommended changes
# Each problem: description, list of (parameter_path, direction, amount, explanation)
# ---------------------------------------------------------------------------

HANDLING_PROBLEMS = {
    "Entry Understeer": {
        "description": "Car pushes wide (won't turn in) when you brake and turn into the corner.",
        "causes": "Front tires lack grip on turn-in, weight distribution too rearward, "
                  "or front suspension too stiff for the corner entry phase.",
        "recommendations": [
            ("Brakes", "Brake Bias", -1.0,
             "Move brake bias rearward to load the front tires less and let them grip laterally."),
            ("Differential", "Coast (Decel) Lock", -5,
             "Lower coast lock so the inside rear wheel slows independently, helping rotation."),
            ("Suspension", "Front Anti-Roll Bar", -2,
             "Softer front ARB lets the front end roll more, increasing front contact patch."),
            ("Suspension", "Rear Anti-Roll Bar", 2,
             "Stiffer rear ARB unloads the inside rear, helping the car rotate."),
            ("Suspension", "Front Spring Rate", -5,
             "Softer front springs allow more weight transfer to the front during braking."),
            ("Aero", "Front Wing Angle", 2,
             "More front downforce directly increases front-end grip."),
            ("Engine", "Engine Braking", -5,
             "Less engine braking reduces the rear's tendency to push the car straight."),
        ],
    },
    "Mid-Corner Understeer": {
        "description": "Car feels planted on entry but pushes wide at the apex, "
                       "won't hold the line through the middle of the corner.",
        "causes": "Overall mechanical balance favors the rear too much, or suspension "
                  "geometry doesn't maintain front grip under sustained lateral load.",
        "recommendations": [
            ("Suspension", "Front Anti-Roll Bar", -2,
             "Softer front ARB improves front grip at sustained lateral loads."),
            ("Suspension", "Rear Anti-Roll Bar", 2,
             "Stiffer rear ARB shifts mid-corner balance toward oversteer (more rotation)."),
            ("Suspension", "Front Camber", -0.3,
             "More negative camber keeps the front tires' contact patch optimal in corners."),
            ("Differential", "Preload", -10,
             "Lower preload allows more wheel speed difference, improving mid-corner rotation."),
            ("Aero", "Front Wing Angle", 2,
             "More front downforce at speed gives the front tires more to work with."),
            ("Aero", "Rear Wing Angle", -1,
             "Slightly less rear wing shifts aero balance forward."),
        ],
    },
    "Exit Understeer": {
        "description": "Car pushes wide when applying throttle on corner exit. "
                       "You can't get on the power early without running wide.",
        "causes": "Rear traction is so good that the front can't keep up, or the diff "
                  "is locking too aggressively and pushing the front wide.",
        "recommendations": [
            ("Differential", "Power (Accel) Lock", -10,
             "Lower power lock allows more wheel speed difference on exit, reducing push."),
            ("Differential", "Preload", -10,
             "Lower preload reduces the diff's tendency to lock under low torque."),
            ("Suspension", "Rear Spring Rate", 5,
             "Stiffer rear springs limit squat, keeping the rear slightly less planted."),
            ("Suspension", "Rear Anti-Roll Bar", 2,
             "Stiffer rear ARB transfers grip from rear to front on exit."),
            ("Aero", "Front Wing Angle", 1,
             "More front grip helps balance the strong rear traction."),
        ],
    },
    "Entry Oversteer": {
        "description": "Rear end steps out when braking into corners. Car snaps loose on turn-in.",
        "causes": "Too much weight transfer to the front under braking, rear too light, "
                  "or diff coast locking too low allowing the inside rear to slow too much.",
        "recommendations": [
            ("Brakes", "Brake Bias", 1.5,
             "More forward bias takes braking load off the rears, stabilizing the rear end."),
            ("Differential", "Coast (Decel) Lock", 5,
             "More coast lock keeps the rear axle connected, preventing one wheel from slowing too fast."),
            ("Suspension", "Rear Anti-Roll Bar", -2,
             "Softer rear ARB keeps the rear tires planted during weight transfer."),
            ("Suspension", "Rear Spring Rate", -5,
             "Softer rear springs allow more rear grip during the braking phase."),
            ("Engine", "Engine Braking", -10,
             "Less engine braking reduces the rear deceleration force that unsettles the car."),
            ("Suspension", "Rear Toe", 0.05,
             "More rear toe-in increases straight-line and braking stability."),
        ],
    },
    "Mid-Corner Oversteer": {
        "description": "Rear slides out at the apex of corners. Car rotates too much mid-corner.",
        "causes": "Rear mechanical grip insufficient for the lateral loads, "
                  "or suspension setup transfers too much load off the rear.",
        "recommendations": [
            ("Suspension", "Rear Anti-Roll Bar", -2,
             "Softer rear ARB keeps the rear tires planted."),
            ("Suspension", "Front Anti-Roll Bar", 2,
             "Stiffer front ARB reduces front grip, rebalancing toward understeer."),
            ("Suspension", "Rear Camber", 0.3,
             "Less negative camber gives the rear tires a bigger contact patch mid-corner."),
            ("Aero", "Rear Wing Angle", 2,
             "More rear downforce directly improves rear grip at speed."),
            ("Suspension", "Rear Spring Rate", -5,
             "Softer rear springs improve rear mechanical grip."),
        ],
    },
    "Exit Oversteer / Power Oversteer": {
        "description": "Rear steps out when applying throttle out of corners. Wheelspin or snap.",
        "causes": "Too much power for the available rear grip, diff too open on power, "
                  "or rear suspension too stiff allowing wheel hop.",
        "recommendations": [
            ("Differential", "Power (Accel) Lock", 10,
             "More power lock distributes torque more evenly, reducing single-wheel spin."),
            ("Engine", "Throttle Map", 1,
             "Smoother throttle response gives you more control at the limit."),
            ("Suspension", "Rear Spring Rate", -5,
             "Softer rear springs keep the tires planted on acceleration."),
            ("Suspension", "Rear Anti-Roll Bar", -2,
             "Softer rear ARB improves rear traction under load transfer."),
            ("Aero", "Rear Wing Angle", 2,
             "More rear downforce at speed helps with high-speed exit oversteer."),
            ("Tires", "Rear Tire Pressure", -5,
             "Lower pressure increases the contact patch for more traction."),
        ],
    },
    "High-Speed Instability": {
        "description": "Car feels nervous, twitchy, or darty at high speeds. Unsafe on straights.",
        "causes": "Insufficient rear downforce, too much rear toe-out, or dampers not controlling "
                  "high-speed movements. Could also be ride height causing aero stall.",
        "recommendations": [
            ("Aero", "Rear Wing Angle", 3,
             "More rear wing stabilizes the car at speed."),
            ("Suspension", "Rear Toe", 0.05,
             "More rear toe-in improves straight-line stability."),
            ("Suspension", "Front Ride Height", -3,
             "Lower front ride height improves aero stability."),
            ("Dampers", "Rear Slow Rebound", 2,
             "Higher rear rebound controls pitch changes that cause instability."),
            ("Suspension", "Rear Spring Rate", 5,
             "Stiffer rear springs reduce aero platform movement."),
        ],
    },
    "Excessive Tire Wear (Front)": {
        "description": "Front tires overheat or wear out much faster than rears.",
        "causes": "Too much front camber, too much front toe, excessive front loading from "
                  "aero or spring setup, or brake bias too forward.",
        "recommendations": [
            ("Suspension", "Front Camber", 0.3,
             "Less negative camber reduces inner edge wear."),
            ("Suspension", "Front Toe", -0.05,
             "Less toe reduces tire scrub and heat buildup."),
            ("Brakes", "Brake Bias", -1.0,
             "Less front bias reduces front tire stress under braking."),
            ("Tires", "Front Tire Pressure", 5,
             "Slightly higher pressure reduces the contact patch and heat generation."),
            ("Aero", "Front Wing Angle", -1,
             "Less front downforce reduces the load the front tires must manage."),
        ],
    },
    "Excessive Tire Wear (Rear)": {
        "description": "Rear tires overheat or wear out much faster than fronts.",
        "causes": "Too much wheelspin on exit, diff too open, too much rear camber, "
                  "or not enough rear downforce for the power output.",
        "recommendations": [
            ("Differential", "Power (Accel) Lock", 5,
             "More power lock distributes torque better, reducing single-tire abuse."),
            ("Suspension", "Rear Camber", 0.2,
             "Less negative camber gives a flatter contact patch under power."),
            ("Tires", "Rear Tire Pressure", 5,
             "Slightly higher pressure reduces heat buildup."),
            ("Aero", "Rear Wing Angle", 2,
             "More rear downforce reduces slip and therefore wear."),
            ("Engine", "Throttle Map", 1,
             "Smoother throttle response reduces wheelspin."),
        ],
    },
    "Braking Instability / Lockups": {
        "description": "Wheels lock up under braking, or the car pulls to one side. "
                       "Inconsistent braking performance.",
        "causes": "Brake pressure too high, bias wrong for the conditions, "
                  "or suspension setup causes excessive load transfer.",
        "recommendations": [
            ("Brakes", "Brake Pressure", -5,
             "Lower maximum pressure gives you more modulation range."),
            ("Brakes", "Brake Bias", 1.0,
             "If rears are locking: more forward bias. If fronts locking: less forward bias."),
            ("Suspension", "Front Spring Rate", -5,
             "Softer front springs improve weight transfer to the front under braking."),
            ("Suspension", "Rear Anti-Roll Bar", -1,
             "Softer rear ARB keeps the rears planted during braking."),
        ],
    },
    "Poor Traction (Low Speed)": {
        "description": "Can't put the power down out of slow corners. Excessive wheelspin "
                       "even with moderate throttle.",
        "causes": "Diff too open, rear suspension too stiff, tire pressures too high, "
                  "or not enough mechanical grip.",
        "recommendations": [
            ("Differential", "Power (Accel) Lock", 10,
             "More lock distributes power to both wheels."),
            ("Differential", "Preload", 10,
             "Higher preload engages the diff sooner at low speeds."),
            ("Suspension", "Rear Spring Rate", -5,
             "Softer rear keeps the tires on the ground."),
            ("Tires", "Rear Tire Pressure", -5,
             "Lower pressure increases contact patch for more grip."),
            ("Engine", "Throttle Map", 1,
             "Smoother throttle helps manage wheelspin."),
        ],
    },
    "Car Bottoming Out": {
        "description": "Car hits the ground over bumps or compressions. Sparks, loss of grip, "
                       "damage risk.",
        "causes": "Ride height too low, springs too soft allowing too much compression, "
                  "or bump damping too low.",
        "recommendations": [
            ("Suspension", "Front Ride Height", 5,
             "More clearance prevents contact."),
            ("Suspension", "Rear Ride Height", 5,
             "More clearance prevents contact."),
            ("Suspension", "Front Spring Rate", 10,
             "Stiffer springs resist compression that causes bottoming."),
            ("Suspension", "Rear Spring Rate", 10,
             "Stiffer springs resist compression that causes bottoming."),
            ("Dampers", "Front Slow Bump", 2,
             "Higher bump damping slows compression."),
            ("Dampers", "Rear Slow Bump", 2,
             "Higher bump damping slows compression."),
        ],
    },
}



# ---------------------------------------------------------------------------
# Step-by-step setup workflow
# ---------------------------------------------------------------------------

SETUP_WORKFLOW = [
    {
        "step": 1,
        "title": "Choose a Baseline",
        "action": "select_baseline",
        "description": (
            "Start by selecting your car class and track type from the Advisor tab. "
            "This generates an intelligent baseline that accounts for your car's physics "
            "characteristics and the track's demands. Never start from scratch — "
            "a good baseline saves dozens of laps."
        ),
        "what_to_check": (
            "The car should be driveable and predictable. You don't need it to be fast yet. "
            "If it's undriveable out of the box, the baseline is wrong for your car — "
            "try a different car class."
        ),
    },
    {
        "step": 2,
        "title": "Set Ride Height & Aero",
        "action": "adjust_aero",
        "description": (
            "Ride height and wing angles are the foundation of your setup. They affect "
            "everything downstream. Run 5-10 laps and assess: Is the car stable at high speed? "
            "Does it bottom out? Is there enough overall grip?\n\n"
            "LOWER RIDE HEIGHT = more downforce, less ground clearance\n"
            "MORE WING = more grip but more drag (lower top speed)\n"
            "MORE RAKE (rear higher than front) = more front downforce"
        ),
        "what_to_check": (
            "No bottoming out. Stable at top speed. Reasonable aero balance — "
            "if understeer at high speed, add front wing. If oversteer at high speed, add rear wing."
        ),
    },
    {
        "step": 3,
        "title": "Tune Springs & Anti-Roll Bars",
        "action": "adjust_springs",
        "description": (
            "Springs and ARBs control weight transfer and body roll. They determine "
            "how the car feels in transitions and mid-corner.\n\n"
            "STIFFER FRONT = less understeer mid-corner (but harsher ride)\n"
            "STIFFER REAR = more oversteer mid-corner\n"
            "STIFFER ARBs = less body roll, but reduce grip over bumps\n\n"
            "For HISTORIC CARS: start softer than you think. These cars rely on "
            "mechanical grip and soft suspension helps tires work."
        ),
        "what_to_check": (
            "Mid-corner balance should feel neutral or slightly understeery (safer). "
            "The car should handle bumps and kerbs without feeling harsh or bouncing."
        ),
    },
    {
        "step": 4,
        "title": "Dial In Dampers",
        "action": "adjust_dampers",
        "description": (
            "Dampers control HOW FAST weight transfers happen. They're the fine-tuning "
            "layer on top of springs.\n\n"
            "SLOW BUMP/REBOUND = controls weight transfer (roll, pitch)\n"
            "FAST BUMP/REBOUND = controls bump absorption (kerbs, rough surfaces)\n\n"
            "Start with slow bump ~60-70% of slow rebound.\n"
            "Start with fast bump ~50-60% of slow bump.\n"
            "Fast rebound similar to fast bump."
        ),
        "what_to_check": (
            "Smooth weight transitions. No oscillation (bouncing). Car settles quickly "
            "after hitting bumps. If the car feels like it's 'porpoising' — dampers are wrong."
        ),
    },
    {
        "step": 5,
        "title": "Set Differential",
        "action": "adjust_diff",
        "description": (
            "The differential controls how power is split between the rear wheels.\n\n"
            "MORE PRELOAD = more connected feel, better traction, worse turn-in\n"
            "MORE POWER LOCK = better traction on exit, less rotation on exit\n"
            "MORE COAST LOCK = more stable on turn-in, less rotation on entry\n\n"
            "For HISTORIC CARS without limited-slip diffs, the diff settings may "
            "be minimal — focus on throttle control instead."
        ),
        "what_to_check": (
            "Good traction out of slow corners. No excessive wheelspin. "
            "The car should still rotate enough to feel nimble."
        ),
    },
    {
        "step": 6,
        "title": "Optimize Brakes",
        "action": "adjust_brakes",
        "description": (
            "Brake bias determines which axle does more braking work.\n\n"
            "MORE FORWARD BIAS = stable under braking, risk of front lockup\n"
            "MORE REARWARD BIAS = better rotation into corners, risk of rear lockup/spin\n\n"
            "For cars WITHOUT ABS (especially historics): use less brake pressure "
            "and a more forward bias. Threshold braking is key."
        ),
        "what_to_check": (
            "No wheel lockups during normal braking. The car slows in a straight "
            "line without pulling to one side. Can trail-brake into corners without snapping."
        ),
    },
    {
        "step": 7,
        "title": "Set Gearing",
        "action": "adjust_gearing",
        "description": (
            "Gearing is track-specific. The goals:\n"
            "1. Top gear should reach (or just reach) the rev limiter at the end of "
            "the longest straight.\n"
            "2. 1st gear should be usable for the slowest corner exit without bogging.\n"
            "3. Gear spacing should keep you in the powerband throughout.\n\n"
            "FINAL DRIVE affects ALL gears proportionally. Adjust it first, "
            "then fine-tune individual gears."
        ),
        "what_to_check": (
            "Not hitting the rev limiter before the braking zone on any straight. "
            "Not bogging down in any corner. Smooth power delivery between shifts."
        ),
    },
    {
        "step": 8,
        "title": "Fine-Tune with Tire Pressures & Camber",
        "action": "adjust_tires",
        "description": (
            "Tire pressures and camber are your final fine-tuning tools.\n\n"
            "PRESSURES: Set cold pressures so hot pressures (after 3-4 laps) land "
            "in the optimal window. Usually 5-10 kPa rise from cold to hot.\n\n"
            "CAMBER: Check tire temperatures across the surface. "
            "Inside should be ~5-10C hotter than outside. If inside is much hotter, "
            "reduce negative camber. If outside is hotter, increase it."
        ),
        "what_to_check": (
            "Even tire temperatures across the surface. Hot pressures in the right range. "
            "No excessive tire wear on one edge."
        ),
    },
    {
        "step": 9,
        "title": "Use the Problem Solver",
        "action": "use_problem_solver",
        "description": (
            "Now do race-pace laps and note specific handling issues. "
            "Go to the Problem Solver tab and select the problem you're experiencing. "
            "Apply the recommended changes one at a time, testing 2-3 laps between each.\n\n"
            "IMPORTANT: Only change ONE thing at a time. If you change multiple parameters "
            "simultaneously, you won't know what helped (or hurt)."
        ),
        "what_to_check": (
            "Each change should make a noticeable difference. If it doesn't, revert it. "
            "When the car feels good everywhere, save the setup!"
        ),
    },
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def generate_baseline(car_class_name, track_type_name):
    """Generate a baseline setup by combining car class defaults with track type deltas.

    Returns (setup_dict, tips_list, warnings_list).
    """
    car_class = CAR_CLASSES.get(car_class_name)
    track_type = TRACK_TYPES.get(track_type_name)

    if not car_class:
        return None, [], [f"Unknown car class: {car_class_name}"]

    # Start from car class defaults
    from rf2_setup import SETUP_CATEGORIES, get_default_setup
    setup = get_default_setup()

    # Apply car class defaults
    for cat, params in car_class["defaults"].items():
        for name, val in params.items():
            if cat in setup and name in setup[cat]:
                setup[cat][name] = val

    tips = []
    warnings = []

    # Apply track type deltas if specified
    if track_type:
        tips.extend(track_type["tips"])
        for cat, params in track_type.get("deltas", {}).items():
            for name, delta in params.items():
                if cat in setup and name in setup[cat]:
                    # Get min/max from SETUP_CATEGORIES
                    if name in SETUP_CATEGORIES.get(cat, {}):
                        vmin, vmax, step = SETUP_CATEGORIES[cat][name][:3]
                        new_val = setup[cat][name] + delta
                        new_val = max(vmin, min(vmax, new_val))
                        # Snap to step
                        if isinstance(step, float):
                            decimals = len(str(step).split('.')[-1])
                            new_val = round(round((new_val - vmin) / step) * step + vmin, decimals)
                        else:
                            new_val = int(round((new_val - vmin) / step) * step + vmin)
                        setup[cat][name] = new_val

    # Generate car-specific warnings
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


def get_problem_recommendations(problem_name):
    """Return the diagnosis info and list of recommended changes for a handling problem."""
    problem = HANDLING_PROBLEMS.get(problem_name)
    if not problem:
        return None
    return problem
