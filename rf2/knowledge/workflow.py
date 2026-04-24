"""Step-by-step setup workflow — the correct order of operations for building a setup."""

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
