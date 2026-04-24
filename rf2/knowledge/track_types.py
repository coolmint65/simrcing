"""Track type definitions — setup deltas applied on top of a car class baseline."""

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
