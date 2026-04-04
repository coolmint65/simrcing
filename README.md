# rFactor 2 Car Setup Program

A desktop GUI application for creating, editing, comparing, and managing rFactor 2 car setups.

## Features

- **All Major Setup Categories**: Suspension, Dampers, Aero, Tires, Brakes, Differential, Gearing, Engine
- **Save/Load Setups**: Save configurations as JSON files and load them later
- **Compare Setups**: Load a second setup for side-by-side comparison with diff indicators
- **Tuning Guide Tips**: Contextual tips for every parameter explaining what it does and how to tune it
- **Tabbed Interface**: Clean tabbed layout organized by category with scrollable parameter lists

## Requirements

- Python 3.6+
- Tkinter (included with most Python installations)

## Usage

```bash
python3 rf2_setup.py
```

### Menu Options

- **File > New Setup** — Reset all parameters to defaults
- **File > Open Setup** — Load a previously saved setup (.json)
- **File > Save Setup** — Save the current setup to a .json file
- **Compare > Load Setup to Compare** — Load a second setup; differences are shown inline
- **Compare > Clear Comparison** — Remove comparison indicators

### Tuning Workflow

1. Start with the default setup or load an existing one
2. Adjust parameters using the sliders — each has min/max ranges and tuning tips
3. Save your setup before heading to the track
4. After testing, load your baseline and compare it with your new setup to see what changed

## Setup File Format

Setups are saved as JSON files in the `setups/` directory (or any location you choose):

```json
{
  "Suspension": {
    "Front Ride Height": 40,
    "Rear Ride Height": 45,
    ...
  },
  "Aero": { ... },
  ...
}
```
