"""Car class definitions — physics characteristics & default parameter values for each class."""


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
