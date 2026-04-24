"""rFactor 2 simulation meta-knowledge.

These are rF2-specific optimizations that differ from real life. The sim has
quirks in its tire model, aero model, and physics that mean certain settings
are almost always optimal regardless of car/track. This module encodes that
meta knowledge so the program can apply it automatically."""


# ---------------------------------------------------------------------------
# rF2 Meta Rules — applied AFTER baseline generation
# Each rule: condition function, modifications, explanation
# ---------------------------------------------------------------------------

RF2_META = {
    "tire_pressure_meta": {
        "description": "Minimum tire pressures are almost always fastest in rF2",
        "explanation": (
            "rF2's tire model doesn't penalize low pressures as harshly as real life. "
            "Lower pressures = bigger contact patch = more grip, with minimal rolling "
            "resistance penalty. The optimal hot pressure is usually the minimum allowed. "
            "Set cold pressures so they rise to just above minimum when hot (after 3-4 laps). "
            "This is the single biggest 'free' performance gain in rF2."
        ),
        "always_apply": True,
        "apply": {
            "Tires": {
                "Front Tire Pressure": 110,  # Near minimum
                "Rear Tire Pressure": 105,   # Near minimum
            },
        },
    },
    "camber_meta": {
        "description": "rF2 rewards more aggressive camber than real life",
        "explanation": (
            "rF2's tire model responds well to aggressive negative camber. "
            "In real life, too much camber overheats the inner edge, but in rF2 "
            "the crossover point is much further negative. Front camber of -3.5 to -4.0 "
            "and rear camber of -2.5 to -3.0 is typical meta for modern race cars. "
            "Historic cars with crossply tires should use less (around -2.0 front)."
        ),
        "always_apply": False,
        "modern_car_apply": {
            "Suspension": {
                "Front Camber": -3.8,
                "Rear Camber": -2.8,
            },
        },
        "historic_car_apply": {
            "Suspension": {
                "Front Camber": -2.0,
                "Rear Camber": -1.5,
            },
        },
    },
    "damper_meta": {
        "description": "rF2 dampers are less sensitive than real life — run stiffer",
        "explanation": (
            "rF2's damper model is somewhat simplified. In real life, damper tuning is "
            "extremely nuanced with lots of sensitivity. In rF2, the effects are more "
            "broad-brush. You can generally run stiffer dampers than you'd expect without "
            "losing mechanical grip. Focus on slow bump/rebound for weight transfer control "
            "and keep fast bump/rebound moderate. The ratio of slow rebound to slow bump "
            "should be about 1.2-1.4x."
        ),
        "always_apply": False,
    },
    "ride_height_meta": {
        "description": "rF2's aero model rewards very low ride heights",
        "explanation": (
            "rF2 has a well-modeled ground effect and underbody aero system. Running the "
            "car as low as possible without bottoming out gives significant aero gains. "
            "The key is maximum rake angle (rear higher than front) for diffuser performance. "
            "For aero-dependent cars, every mm of ride height matters. "
            "Aim for 5-15mm of rake (rear minus front ride height)."
        ),
        "always_apply": False,
        "aero_car_tips": [
            "Run the front as low as you can without bottoming out.",
            "Rear should be 5-15mm higher than front (rake angle).",
            "Every mm lower = measurable aero gain on aero-dependent cars.",
            "Use stiffer springs to prevent bottoming rather than raising ride height.",
        ],
    },
    "brake_meta": {
        "description": "rF2 brake temps and wear are more forgiving than real life",
        "explanation": (
            "rF2's brake model is relatively forgiving. You can usually run smaller "
            "brake ducts (more closed) than real life without overheating. This gives "
            "a small aero benefit. Only open ducts further if you see brake temps "
            "consistently above 700C. For sprint races, you can often close them to 20-30%."
        ),
        "always_apply": True,
        "apply": {
            "Aero": {
                "Brake Ducts Front": 25,
                "Brake Ducts Rear": 20,
            },
        },
    },
    "diff_meta": {
        "description": "rF2's diff model responds well to moderate preload",
        "explanation": (
            "rF2's limited-slip differential model is generally well-modeled. "
            "However, the game tends to reward moderate preload values (40-70 Nm for most cars) "
            "and moderate power lock (35-55%). Coast lock is often best kept low (10-25%) "
            "to preserve turn-in. Very high or very low diff settings tend to hurt more than help."
        ),
        "always_apply": False,
    },
    "fuel_effect_meta": {
        "description": "Fuel weight has a bigger effect on handling in rF2 than you'd expect",
        "explanation": (
            "In rF2, fuel weight significantly affects handling balance. A full tank "
            "can shift the balance noticeably toward understeer. If you're tuning with "
            "low fuel, the car will handle differently with a full race load. "
            "Always do your final setup tuning at RACE fuel level, not qualifying fuel. "
            "For endurance, consider that the car will improve as fuel burns off."
        ),
        "always_apply": False,
    },
    "toe_meta": {
        "description": "Minimal toe settings are generally fastest in rF2",
        "explanation": (
            "rF2 models tire scrub from toe angles well. Excessive toe creates drag "
            "and heat. The meta is to run near-zero front toe (0.00 to 0.05 toe-out) "
            "and minimal rear toe-in (0.10 to 0.15). Only increase rear toe if you're "
            "struggling with high-speed instability."
        ),
        "always_apply": True,
        "apply": {
            "Suspension": {
                "Front Toe": 0.0,
                "Rear Toe": 0.10,
            },
        },
    },
}


def get_meta_tips():
    """Return all meta tips as a formatted list."""
    tips = []
    for key, meta in RF2_META.items():
        tips.append({
            "title": meta["description"],
            "explanation": meta["explanation"],
            "always_apply": meta.get("always_apply", False),
        })
    return tips


def apply_meta_to_setup(setup, car_data=None):
    """Apply rF2 meta knowledge to a setup dict. Modifies in place and returns
    a list of (description, explanation) for what was changed."""
    from rf2.parameters import SETUP_CATEGORIES

    changes = []

    for key, meta in RF2_META.items():
        # Always-apply rules
        if meta.get("always_apply") and "apply" in meta:
            for cat, params in meta["apply"].items():
                for param, value in params.items():
                    if cat in setup and param in setup[cat]:
                        info = SETUP_CATEGORIES.get(cat, {}).get(param)
                        if info:
                            vmin, vmax = info[0], info[1]
                            value = max(vmin, min(vmax, value))
                        setup[cat][param] = value
            changes.append((meta["description"], meta["explanation"]))

        # Camber meta — depends on car type
        if key == "camber_meta" and car_data:
            is_historic = "historic" in car_data.get("class", "").lower()
            apply_key = "historic_car_apply" if is_historic else "modern_car_apply"
            if apply_key in meta:
                for cat, params in meta[apply_key].items():
                    for param, value in params.items():
                        if cat in setup and param in setup[cat]:
                            info = SETUP_CATEGORIES.get(cat, {}).get(param)
                            if info:
                                vmin, vmax = info[0], info[1]
                                value = max(vmin, min(vmax, value))
                            setup[cat][param] = value
                changes.append((meta["description"], meta["explanation"]))

    return changes
