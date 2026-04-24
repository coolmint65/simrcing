"""Handling problem diagnosis — maps symptoms to recommended parameter changes."""

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
