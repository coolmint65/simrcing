"""rFactor 2 track database — real tracks with layout characteristics that
drive setup recommendations."""

# Each track has: type, length_km, surface quality (1-5, 5=glass smooth),
# top_speed_importance (1-5), slow_corner_count, elevation_change,
# and specific setup notes.

TRACKS = {
    # ---- High-Speed Circuits ----
    "Spa-Francorchamps": {
        "type": "High-Speed Circuit", "length_km": 7.0, "surface": 3,
        "top_speed": 5, "slow_corners": 2, "elevation": "high",
        "notes": "Very fast with big elevation changes. Eau Rouge/Raidillon is flat in high-downforce "
                 "cars. Long Kemmel straight needs good top speed. Bumpy in places (Bus Stop). "
                 "Weather changes constantly — be ready for rain setup.",
        "bias": {"Aero": {"Rear Wing Angle": -2}, "Gearing": {"Final Drive": -0.10}},
    },
    "Monza": {
        "type": "High-Speed Circuit", "length_km": 5.8, "surface": 4,
        "top_speed": 5, "slow_corners": 3, "elevation": "flat",
        "notes": "Temple of speed. Minimum downforce, maximum straight-line speed. "
                 "Heavy kerb usage at chicanes. Brake cooling important due to heavy braking zones. "
                 "Two Lesmo corners need good mid-speed aero balance.",
        "bias": {
            "Aero": {"Front Wing Angle": -4, "Rear Wing Angle": -5,
                     "Brake Ducts Front": 10, "Brake Ducts Rear": 5},
            "Gearing": {"Final Drive": -0.25},
        },
    },
    "Le Mans (Circuit de la Sarthe)": {
        "type": "High-Speed Circuit", "length_km": 13.6, "surface": 3,
        "top_speed": 5, "slow_corners": 4, "elevation": "low",
        "notes": "Longest circuit. Mulsanne straight (with chicanes) demands low drag. "
                 "Porsche curves are medium-speed. Public road sections are bumpy. "
                 "Night driving — setup must be stable and confidence-inspiring. "
                 "Fuel strategy is critical for endurance.",
        "bias": {
            "Aero": {"Front Wing Angle": -3, "Rear Wing Angle": -4},
            "Suspension": {"Front Ride Height": 3, "Rear Ride Height": 3},
            "Gearing": {"Final Drive": -0.20},
        },
    },
    "Silverstone": {
        "type": "High-Speed Circuit", "length_km": 5.9, "surface": 4,
        "top_speed": 4, "slow_corners": 3, "elevation": "flat",
        "notes": "Fast flowing circuit. Maggots-Becketts-Chapel is a high-speed complex that "
                 "demands excellent aero balance. Copse and Stowe are fast corners. "
                 "Good surface quality. Wind can be a factor.",
        "bias": {"Aero": {"Rear Wing Angle": -1}},
    },

    # ---- Technical / Tight Circuits ----
    "Monaco": {
        "type": "Technical / Tight Circuit", "length_km": 3.3, "surface": 3,
        "top_speed": 1, "slow_corners": 8, "elevation": "medium",
        "notes": "Ultimate street circuit. No run-off — walls everywhere. "
                 "Maximum downforce, short gearing. Mechanical grip is everything. "
                 "Bump absorption at Mirabeau and Swimming Pool critical. "
                 "Qualify well — overtaking is nearly impossible.",
        "bias": {
            "Aero": {"Front Wing Angle": 5, "Rear Wing Angle": 6},
            "Gearing": {"Final Drive": 0.30},
            "Suspension": {"Front Ride Height": 5, "Rear Ride Height": 5},
        },
    },
    "Zandvoort": {
        "type": "Technical / Tight Circuit", "length_km": 4.3, "surface": 4,
        "top_speed": 2, "slow_corners": 5, "elevation": "medium",
        "notes": "Banked final corner is unique. Lots of elevation change for a short track. "
                 "Several blind crests. Higher downforce works well here. "
                 "The banking loads the tires differently — watch tire temps on the banked turn.",
        "bias": {
            "Aero": {"Front Wing Angle": 3, "Rear Wing Angle": 4},
            "Gearing": {"Final Drive": 0.15},
        },
    },
    "Hungaroring": {
        "type": "Technical / Tight Circuit", "length_km": 4.4, "surface": 3,
        "top_speed": 2, "slow_corners": 6, "elevation": "medium",
        "notes": "Slow and twisty, like a big kart track. High downforce essential. "
                 "Overtaking very difficult. Tire degradation is high — surface is abrasive. "
                 "Good traction out of slow corners is critical for lap time.",
        "bias": {
            "Aero": {"Front Wing Angle": 4, "Rear Wing Angle": 5},
            "Gearing": {"Final Drive": 0.20},
        },
    },
    "Barcelona-Catalunya": {
        "type": "Technical / Tight Circuit", "length_km": 4.7, "surface": 4,
        "top_speed": 3, "slow_corners": 4, "elevation": "low",
        "notes": "The all-rounder test track. Good balance of fast and slow corners. "
                 "Sector 3 is very slow and technical. High tire wear, especially fronts. "
                 "If the car works here, it works most places.",
        "bias": {},
    },

    # ---- Street Circuits ----
    "Long Beach": {
        "type": "Street Circuit", "length_km": 3.2, "surface": 2,
        "top_speed": 2, "slow_corners": 5, "elevation": "flat",
        "notes": "Classic American street circuit. Very bumpy surface. "
                 "Fountain hairpin is very slow. Walls are close everywhere. "
                 "Need compliant suspension and forgiving setup.",
        "bias": {
            "Suspension": {"Front Ride Height": 5, "Rear Ride Height": 5,
                          "Front Spring Rate": -10, "Rear Spring Rate": -10},
        },
    },
    "Baku City Circuit": {
        "type": "Street Circuit", "length_km": 6.0, "surface": 2,
        "top_speed": 4, "slow_corners": 5, "elevation": "low",
        "notes": "Unique mix of very long straight and very tight old-town section. "
                 "Setup compromise between top speed and low-speed grip. "
                 "Castle section is extremely narrow. Bumpy surface throughout.",
        "bias": {
            "Aero": {"Rear Wing Angle": -2},
            "Suspension": {"Front Spring Rate": -5, "Rear Spring Rate": -5},
        },
    },
    "Singapore Marina Bay": {
        "type": "Street Circuit", "length_km": 5.1, "surface": 2,
        "top_speed": 2, "slow_corners": 8, "elevation": "flat",
        "notes": "Night race street circuit. Very long lap with many corners. "
                 "High physical demand. Bumpy surface, lots of 90-degree turns. "
                 "High downforce, focus on traction and braking stability.",
        "bias": {
            "Aero": {"Front Wing Angle": 4, "Rear Wing Angle": 5},
            "Gearing": {"Final Drive": 0.20},
        },
    },

    # ---- Bumpy / Old-School Circuits ----
    "Nurburgring Nordschleife": {
        "type": "Bumpy / Old-School Circuit", "length_km": 20.8, "surface": 2,
        "top_speed": 4, "slow_corners": 6, "elevation": "extreme",
        "notes": "The Green Hell. 20+ km of bumps, crests, blind corners, and elevation change. "
                 "Setup MUST be forgiving — you can't drive on the limit everywhere. "
                 "Compliant suspension is essential. Higher ride height than normal. "
                 "Gearing is a massive compromise — huge speed range. "
                 "If you can be fast here, you can drive anything.",
        "bias": {
            "Suspension": {"Front Ride Height": 8, "Rear Ride Height": 8,
                          "Front Spring Rate": -10, "Rear Spring Rate": -10,
                          "Front Anti-Roll Bar": -3, "Rear Anti-Roll Bar": -3},
            "Dampers": {"Front Fast Bump": -2, "Rear Fast Bump": -2,
                       "Front Fast Rebound": -2, "Rear Fast Rebound": -2},
        },
    },
    "Sebring": {
        "type": "Bumpy / Old-School Circuit", "length_km": 6.0, "surface": 1,
        "top_speed": 3, "slow_corners": 5, "elevation": "flat",
        "notes": "Built on an old airfield. Extremely bumpy concrete surface. "
                 "Destroys tires. Suspension compliance is everything. "
                 "Heavy braking zones. Endurance classic — setup for consistency not peak pace. "
                 "Tire pressures run away quickly on this surface.",
        "bias": {
            "Suspension": {"Front Spring Rate": -15, "Rear Spring Rate": -15},
            "Dampers": {"Front Fast Bump": -3, "Rear Fast Bump": -3},
            "Tires": {"Front Tire Pressure": -10, "Rear Tire Pressure": -10},
        },
    },
    "COTA (Circuit of the Americas)": {
        "type": "Bumpy / Old-School Circuit", "length_km": 5.5, "surface": 3,
        "top_speed": 4, "slow_corners": 4, "elevation": "medium",
        "notes": "Modern track but surface has developed bumps, especially sector 2. "
                 "Big elevation change at Turn 1. Long back straight. "
                 "Mix of high and low speed corners. Good all-round test.",
        "bias": {
            "Dampers": {"Front Fast Bump": -1, "Rear Fast Bump": -1},
            "Suspension": {"Front Ride Height": 3, "Rear Ride Height": 3},
        },
    },

    # ---- Classic / Historic Tracks ----
    "Goodwood": {
        "type": "Bumpy / Old-School Circuit", "length_km": 3.8, "surface": 3,
        "top_speed": 3, "slow_corners": 3, "elevation": "flat",
        "notes": "Classic British circuit. Mostly fast and flowing. "
                 "Perfect for historic cars. Chicane is the only slow section. "
                 "St Mary's is a high-speed commitment corner. Grass runoff only.",
        "bias": {},
    },
    "Brands Hatch (GP)": {
        "type": "Bumpy / Old-School Circuit", "length_km": 3.9, "surface": 3,
        "top_speed": 3, "slow_corners": 4, "elevation": "high",
        "notes": "Dramatic elevation changes, especially Paddock Hill Bend. "
                 "Narrow with little runoff. Clearways is very fast. "
                 "Druids hairpin needs good low-speed traction.",
        "bias": {
            "Suspension": {"Front Ride Height": 3, "Rear Ride Height": 3},
        },
    },

    # ---- Oval / Banked ----
    "Daytona International Speedway (Oval)": {
        "type": "Oval / Banked Circuit", "length_km": 4.0, "surface": 4,
        "top_speed": 5, "slow_corners": 0, "elevation": "flat",
        "notes": "High-speed superspeedway with steep banking. Full throttle most of the lap. "
                 "Aero is about drafting efficiency. Setup is about high-speed stability "
                 "and surviving pack racing. Very low drag needed.",
        "bias": {
            "Aero": {"Front Wing Angle": -5, "Rear Wing Angle": -5},
            "Gearing": {"Final Drive": -0.30},
        },
    },
    "Daytona (Road Course)": {
        "type": "Technical / Tight Circuit", "length_km": 5.7, "surface": 3,
        "top_speed": 4, "slow_corners": 4, "elevation": "flat",
        "notes": "Uses the oval banking plus an infield road course. Unique combination "
                 "of high-speed banking and technical infield. Setup is a compromise. "
                 "Bus stop chicane requires good low-speed grip.",
        "bias": {},
    },
    "Indianapolis Motor Speedway (Oval)": {
        "type": "Oval / Banked Circuit", "length_km": 4.0, "surface": 4,
        "top_speed": 5, "slow_corners": 0, "elevation": "flat",
        "notes": "The Brickyard. Moderate banking. Four left turns, all about corner speed. "
                 "Consistent setup — all four corners are similar. "
                 "Slight asymmetric setup benefits (stiffer right-side springs).",
        "bias": {
            "Aero": {"Rear Wing Angle": -3},
            "Suspension": {"Rear Spring Rate": 5},
        },
    },

    # ---- Modern Road Courses ----
    "Bathurst (Mount Panorama)": {
        "type": "Bumpy / Old-School Circuit", "length_km": 6.2, "surface": 3,
        "top_speed": 4, "slow_corners": 4, "elevation": "extreme",
        "notes": "Mountain circuit with extreme elevation change. Very narrow at the top. "
                 "Conrod straight is flat in high-downforce cars. The Chase is very fast. "
                 "Forrest Elbow is blind and critical. Setup must handle both the rough "
                 "mountain section and the fast lower section.",
        "bias": {
            "Suspension": {"Front Ride Height": 5, "Rear Ride Height": 5},
            "Dampers": {"Front Fast Bump": -1, "Rear Fast Bump": -1},
        },
    },
    "Suzuka": {
        "type": "High-Speed Circuit", "length_km": 5.8, "surface": 4,
        "top_speed": 4, "slow_corners": 3, "elevation": "medium",
        "notes": "Figure-8 layout. The Esses (S-curves) are legendary — need perfect balance. "
                 "130R is a high-speed commitment corner. Spoon curve rewards good rear stability. "
                 "Degner curves are tricky. One of the best driver's circuits.",
        "bias": {},
    },
    "Imola": {
        "type": "Technical / Tight Circuit", "length_km": 4.9, "surface": 3,
        "top_speed": 3, "slow_corners": 5, "elevation": "medium",
        "notes": "Classic Italian circuit. Variante Alta and Variante Bassa chicanes need "
                 "good kerb handling. Acque Minerali is bumpy on entry. "
                 "Rivazza is a great test of rear traction. Anti-clockwise.",
        "bias": {
            "Dampers": {"Front Fast Bump": -1, "Rear Fast Bump": -1},
        },
    },
    "Portimao (Algarve)": {
        "type": "Bumpy / Old-School Circuit", "length_km": 4.7, "surface": 4,
        "top_speed": 3, "slow_corners": 4, "elevation": "high",
        "notes": "Massive elevation changes, many blind crests. Modern surface but the "
                 "undulation makes it feel like an old-school track. Turn 1 is uphill and blind. "
                 "Turn 3 is a terrifying downhill braking zone. Ride height needs to handle compressions.",
        "bias": {
            "Suspension": {"Front Ride Height": 3, "Rear Ride Height": 3},
        },
    },
    "Watkins Glen": {
        "type": "High-Speed Circuit", "length_km": 5.4, "surface": 3,
        "top_speed": 4, "slow_corners": 2, "elevation": "medium",
        "notes": "Fast American road course. Lots of high-speed corners. "
                 "The Boot section is more technical. Good surface overall. "
                 "Inner Loop is the only really slow section. Great for prototypes.",
        "bias": {"Aero": {"Rear Wing Angle": -1}},
    },
    "Road America": {
        "type": "High-Speed Circuit", "length_km": 6.5, "surface": 3,
        "top_speed": 4, "slow_corners": 3, "elevation": "medium",
        "notes": "Long fast American circuit through Wisconsin woods. Big elevation changes. "
                 "Kink is flat for most cars. Canada Corner is a big braking zone. "
                 "Turn 5 is one of the best corners in motorsport. Natural terrain track.",
        "bias": {},
    },
    "Mugello": {
        "type": "High-Speed Circuit", "length_km": 5.2, "surface": 4,
        "top_speed": 4, "slow_corners": 2, "elevation": "medium",
        "notes": "Fast and flowing Tuscan circuit. Almost all medium-to-high speed corners. "
                 "Arrabbiata corners are a high-speed commitment. San Donato is a big braking zone. "
                 "Excellent surface. Rewards a well-balanced setup.",
        "bias": {},
    },
}


def find_track(query):
    """Fuzzy search for a track by name. Returns list of (name, data) tuples sorted by relevance."""
    query_lower = query.lower().strip()
    if not query_lower:
        return []

    exact = []
    starts = []
    contains = []
    word_match = []

    for name, data in TRACKS.items():
        name_lower = name.lower()
        if query_lower == name_lower:
            exact.append((name, data))
        elif name_lower.startswith(query_lower):
            starts.append((name, data))
        elif query_lower in name_lower:
            contains.append((name, data))
        else:
            query_words = query_lower.split()
            if all(w in name_lower or w in data.get("notes", "").lower()
                   or w in data.get("type", "").lower() for w in query_words):
                word_match.append((name, data))

    return exact + starts + contains + word_match
