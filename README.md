# rFactor 2 Car Setup Program

An intelligent desktop GUI application for building the *right* setup for any car/track combination in rFactor 2. Covers modern race cars, historics, prototypes, and everything in between.

## Features

### Intelligent Setup Advisor
- **9 car classes**: GT3, GTE/GT2, LMP2/Prototype, Open-Wheel/Formula, Touring Car, Historic GT, Historic Formula, Group C/Can-Am, Stock Car/Oval
- **6 track types**: High-Speed, Technical, Street Circuit, Bumpy/Old-School, Oval/Banked, Wet/Damp
- Generates a physics-informed baseline by combining car characteristics with track demands
- Car-specific warnings (no ABS, no TC, minimal aero, aero-sensitive, high power-to-grip)

### Handling Problem Solver
- Select from 12 common handling problems (understeer, oversteer, tire wear, instability, etc.)
- Get a diagnosis of likely causes
- Prioritized list of specific parameter changes with explanations
- "Apply Top Fix" button to make changes one at a time

### Step-by-Step Workflow Guide
- 9-step professional setup workflow from baseline through fine-tuning
- Correct order of operations (ride height/aero first, tires/camber last)
- "What to verify" checklist for each step
- Special notes for historic cars

### Full Setup Editor
- **All Major Categories**: Suspension, Dampers, Aero, Tires, Brakes, Differential, Gearing, Engine
- **48 tunable parameters** with sliders, step snapping, and units
- **Contextual tuning tips** on every parameter

### Save/Load & Compare
- Save/load setups as JSON files
- Side-by-side comparison with inline diff indicators

## Requirements

- Python 3.6+
- Tkinter (included with most Python installations)

## Usage

```bash
python3 rf2_setup.py
```

### Recommended Workflow

1. **Advisor tab** — Select your car class + track type, hit "Generate Baseline"
2. **Save the baseline** (File > Save Setup) — you'll compare against this later
3. **Workflow Guide tab** — Follow the steps in order to refine the setup
4. **Run laps** — test on track
5. **Problem Solver tab** — describe what's wrong, apply fixes one at a time
6. **Compare** — load your baseline to see what you changed
7. **Save your final setup**

### Car Classes

| Class | Examples | Key Traits |
|-------|----------|------------|
| GT3 | BMW M4 GT3, Porsche 911 GT3 R | Mid-high downforce, ABS/TC available |
| GTE / GT2 | Porsche 911 RSR, Ferrari 488 GTE | Higher downforce than GT3 |
| LMP2 / Prototype | Oreca 07, Dallara P217 | Very high downforce, aero-sensitive |
| Open-Wheel / Formula | F1, F3, Formula E | Extreme downforce, very light |
| Touring Car | BTCC, DTM, TCR | Low downforce, mechanical grip |
| Historic GT | Shelby Cobra, Ferrari 250 GTO | No aids, narrow tires, no aero |
| Historic Formula | Lotus 49, Brabham BT20 | No aids, minimal wings, dangerous |
| Group C / Can-Am | Porsche 962, Jaguar XJR-9 | Very high power, ground effect |
| Stock Car / Oval | NASCAR-style | Heavy, low downforce, mechanical grip |
