#!/usr/bin/env python3
"""rFactor 2 Car Setup Program - A comprehensive setup editor with save/load,
comparison, and tuning tips for all major car setup categories."""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from copy import deepcopy
from setup_knowledge import (CAR_CLASSES, TRACK_TYPES, HANDLING_PROBLEMS,
                             SETUP_WORKFLOW, generate_baseline,
                             get_problem_recommendations)

# ---------------------------------------------------------------------------
# Setup parameter definitions
# Each parameter: (label, min, max, step, default, unit, tip)
# ---------------------------------------------------------------------------

SETUP_CATEGORIES = {
    "Suspension": {
        "Front Ride Height": (20, 80, 1, 40, "mm",
            "Lower ride height reduces center of gravity and improves aero efficiency, "
            "but too low risks bottoming out. Start mid-range and lower gradually."),
        "Rear Ride Height": (20, 80, 1, 45, "mm",
            "Raising the rear relative to the front increases front downforce via rake angle. "
            "Keep within 5-15mm of front ride height for balance."),
        "Front Spring Rate": (20, 200, 5, 80, "N/mm",
            "Stiffer springs reduce body roll and improve responsiveness but can reduce grip "
            "on bumpy tracks. Softer springs improve mechanical grip."),
        "Rear Spring Rate": (20, 200, 5, 85, "N/mm",
            "Stiffer rear springs reduce traction under acceleration. A slightly stiffer rear "
            "vs front can reduce oversteer on turn entry."),
        "Front Anti-Roll Bar": (0, 50, 1, 15, "N/mm",
            "Stiffer front ARB reduces understeer mid-corner but can cause inside wheel lift. "
            "Softer improves mechanical grip on bumpy surfaces."),
        "Rear Anti-Roll Bar": (0, 50, 1, 12, "N/mm",
            "Stiffer rear ARB helps rotate the car but reduces rear traction. "
            "Balance front/rear ARBs to tune mid-corner behavior."),
        "Front Toe": (-2.0, 2.0, 0.05, 0.1, "deg",
            "Toe-out improves turn-in response but increases tire wear. "
            "Toe-in improves straight-line stability. Keep values small (0-0.3 deg)."),
        "Rear Toe": (-2.0, 2.0, 0.05, 0.2, "deg",
            "Slight toe-in at the rear improves stability under braking and corner entry. "
            "Too much toe-in causes drag and overheating."),
        "Front Camber": (-5.0, 0.0, 0.1, -3.0, "deg",
            "More negative camber improves cornering grip but reduces braking/acceleration grip. "
            "Check tire temps: inside should be ~5C hotter than outside."),
        "Rear Camber": (-5.0, 0.0, 0.1, -2.0, "deg",
            "Less negative camber than front is typical. Too much negative camber reduces "
            "rear traction under acceleration."),
    },
    "Dampers": {
        "Front Slow Bump": (1, 20, 1, 8, "clicks",
            "Controls compression at low shaft speeds (weight transfer). Higher values resist "
            "body roll but reduce grip over gentle undulations."),
        "Rear Slow Bump": (1, 20, 1, 8, "clicks",
            "Higher rear slow bump reduces squat under acceleration. "
            "Lower values improve rear traction on corner exit."),
        "Front Fast Bump": (1, 20, 1, 5, "clicks",
            "Controls compression over sharp bumps/kerbs. Lower values let the suspension "
            "absorb impacts better, keeping tire contact."),
        "Rear Fast Bump": (1, 20, 1, 5, "clicks",
            "Lower values improve rear grip over bumps. Too low can cause oscillation. "
            "Typically set 2-4 clicks below slow bump."),
        "Front Slow Rebound": (1, 20, 1, 10, "clicks",
            "Controls how quickly the suspension extends. Higher values improve stability "
            "during weight transfer but can cause jacking on bumpy tracks."),
        "Rear Slow Rebound": (1, 20, 1, 10, "clicks",
            "Higher rear rebound slows weight transfer to the front on turn-in, "
            "reducing oversteer. Lower values improve rotation."),
        "Front Fast Rebound": (1, 20, 1, 6, "clicks",
            "Controls extension speed over sharp bumps. Lower values help tires "
            "stay planted after hitting kerbs."),
        "Rear Fast Rebound": (1, 20, 1, 6, "clicks",
            "Similar to front — lower values keep rear tires in contact over bumps. "
            "Balance with fast bump for optimal control."),
    },
    "Aero": {
        "Front Wing Angle": (0, 40, 1, 15, "deg",
            "More front wing increases front downforce and reduces understeer. "
            "Increases drag. Balance with rear wing for neutral handling."),
        "Rear Wing Angle": (0, 40, 1, 20, "deg",
            "More rear wing increases rear grip and stability at high speed. "
            "Increases drag, reducing top speed. Lower for faster tracks."),
        "Front Splitter": (0, 10, 1, 5, "mm",
            "Extending the splitter increases front downforce. Very sensitive to ride height — "
            "lower ride height amplifies splitter effect."),
        "Rear Diffuser": (0, 10, 1, 5, "mm",
            "Larger diffuser setting generates more rear downforce with less drag penalty "
            "than the wing. Sensitive to rear ride height."),
        "Brake Ducts Front": (0, 100, 5, 50, "%",
            "More open ducts cool brakes faster but reduce front downforce. "
            "Open more for endurance, close for sprint qualifying."),
        "Brake Ducts Rear": (0, 100, 5, 50, "%",
            "Same trade-off as front ducts. Rear brakes typically run cooler "
            "so can often be more closed than fronts."),
    },
    "Tires": {
        "Front Tire Pressure": (100, 200, 5, 145, "kPa",
            "Higher pressure reduces rolling resistance but shrinks contact patch. "
            "Target 5-10 kPa increase from cold to hot. Check tire temps for even wear."),
        "Rear Tire Pressure": (100, 200, 5, 140, "kPa",
            "Slightly lower rear pressure than front improves rear traction. "
            "Monitor hot pressures — they should be 150-170 kPa typically."),
        "Front Tire Compound": (1, 5, 1, 3, "type",
            "1=Hardest, 5=Softest. Softer compounds grip better but wear faster. "
            "Consider stint length and track temperature."),
        "Rear Tire Compound": (1, 5, 1, 3, "type",
            "Usually matches front compound. In rare cases a harder rear compound "
            "can help with rear tire overheating issues."),
    },
    "Brakes": {
        "Brake Bias": (45.0, 70.0, 0.5, 57.0, "%",
            "Percentage of braking force on the front axle. Higher values improve stability "
            "but can cause front lock-ups. Lower values help rotation but risk rear lock-ups."),
        "Brake Pressure": (50, 100, 1, 90, "%",
            "Maximum braking force. Lower if you're locking up frequently. "
            "Higher values allow shorter braking zones with good pedal control."),
        "Front Brake Disc": (20, 40, 2, 28, "mm",
            "Thicker discs absorb more heat and resist fade but add unsprung weight. "
            "Use thicker discs for heavy braking circuits."),
        "Rear Brake Disc": (20, 40, 2, 24, "mm",
            "Rear discs can usually be thinner since less braking force goes to the rear. "
            "Saves weight without significant performance loss."),
    },
    "Differential": {
        "Preload": (10, 200, 5, 50, "Nm",
            "Higher preload creates a more locked differential at low torque. "
            "Improves traction exiting slow corners but reduces turn-in."),
        "Power (Accel) Lock": (0, 100, 5, 40, "%",
            "Controls locking under acceleration. Higher values put more power down "
            "but reduce corner-exit rotation. Lower values improve turn-in."),
        "Coast (Decel) Lock": (0, 100, 5, 20, "%",
            "Controls locking on deceleration/engine braking. Higher values stabilize "
            "the rear on turn-in. Lower values improve rotation."),
        "Viscous Lock": (0, 100, 5, 30, "%",
            "Speed-sensitive locking that smooths the differential behavior. "
            "Higher values provide more progressive locking characteristics."),
    },
    "Gearing": {
        "Final Drive": (2.0, 5.5, 0.01, 3.50, "ratio",
            "Lower ratio = higher top speed, less acceleration. Higher ratio = more acceleration, "
            "lower top speed. Start with a value that hits max RPM at the end of the longest straight."),
        "1st Gear": (2.5, 4.5, 0.01, 3.60, "ratio",
            "Set for the slowest corner on track. Should provide good acceleration "
            "out of hairpins without excessive wheelspin."),
        "2nd Gear": (1.8, 3.5, 0.01, 2.50, "ratio",
            "Bridge between 1st and 3rd. Aim for smooth RPM transitions "
            "between gears for consistent power delivery."),
        "3rd Gear": (1.3, 2.8, 0.01, 1.90, "ratio",
            "Often used in medium-speed corners. Set so you don't need to shift "
            "mid-corner in critical sections."),
        "4th Gear": (1.0, 2.3, 0.01, 1.55, "ratio",
            "Common gear for fast sweeping corners. Space evenly between 3rd and 5th "
            "for smooth power band usage."),
        "5th Gear": (0.8, 1.8, 0.01, 1.28, "ratio",
            "High-speed gear. Ensure you're in the power band on the main straights. "
            "Adjust spacing with 4th and 6th."),
        "6th Gear": (0.6, 1.5, 0.01, 1.08, "ratio",
            "Top gear. Set so the car just reaches or slightly exceeds the rev limiter "
            "at the end of the longest straight."),
    },
    "Engine": {
        "Engine Braking": (0, 100, 5, 50, "%",
            "Higher engine braking slows the car on lift-off, helping corner entry stability. "
            "Lower values reduce rear instability on deceleration."),
        "Throttle Map": (1, 5, 1, 3, "map",
            "1=Aggressive (full response), 5=Smooth (gradual). Lower maps give more immediate "
            "power but risk wheelspin. Higher maps improve traction control."),
        "Rev Limit": (8000, 15000, 100, 12000, "RPM",
            "Lower rev limits can improve fuel economy and engine life in endurance. "
            "Max RPM for qualifying and sprint races."),
        "Fuel Load": (10, 120, 1, 60, "liters",
            "More fuel adds weight, reducing grip and increasing tire wear. "
            "Calculate fuel needed for your stint and add a small buffer."),
    },
}


def get_default_setup():
    """Create a setup dict with all default values."""
    setup = {}
    for cat, params in SETUP_CATEGORIES.items():
        setup[cat] = {}
        for name, (vmin, vmax, step, default, unit, tip) in params.items():
            setup[cat][name] = default
    return setup


def setup_to_flat(setup):
    """Flatten a nested setup dict to a list of (category, name, value) tuples."""
    items = []
    for cat in SETUP_CATEGORIES:
        if cat in setup:
            for name in SETUP_CATEGORIES[cat]:
                if name in setup[cat]:
                    items.append((cat, name, setup[cat][name]))
    return items


# ---------------------------------------------------------------------------
# Main Application
# ---------------------------------------------------------------------------

class RF2SetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("rFactor 2 Car Setup Program")
        self.root.geometry("960x720")
        self.root.minsize(800, 600)

        self.setup = get_default_setup()
        self.compare_setup = None
        self.compare_name = ""
        self.widgets = {}  # cat -> name -> (var, scale, value_label)

        self._build_menu()
        self._build_ui()

    # ---- Menu Bar ----
    def _build_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Setup", command=self.new_setup)
        file_menu.add_command(label="Open Setup...", command=self.load_setup)
        file_menu.add_command(label="Save Setup...", command=self.save_setup)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        compare_menu = tk.Menu(menubar, tearoff=0)
        compare_menu.add_command(label="Load Setup to Compare...", command=self.load_compare)
        compare_menu.add_command(label="Clear Comparison", command=self.clear_compare)
        menubar.add_cascade(label="Compare", menu=compare_menu)

    # ---- Main UI ----
    def _build_ui(self):
        # Top info bar
        info_frame = ttk.Frame(self.root, padding=5)
        info_frame.pack(fill=tk.X)
        self.status_var = tk.StringVar(value="rFactor 2 Setup Editor — New Setup")
        ttk.Label(info_frame, textvariable=self.status_var,
                  font=("TkDefaultFont", 11, "bold")).pack(side=tk.LEFT)

        self.compare_var = tk.StringVar(value="")
        ttk.Label(info_frame, textvariable=self.compare_var,
                  foreground="blue").pack(side=tk.RIGHT)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Advisor tab (first!) — baseline generator
        advisor_tab = self._build_advisor_tab()
        self.notebook.add(advisor_tab, text=">> Advisor")

        # Problem Solver tab
        problem_tab = self._build_problem_solver_tab()
        self.notebook.add(problem_tab, text=">> Problem Solver")

        # Workflow tab
        workflow_tab = self._build_workflow_tab()
        self.notebook.add(workflow_tab, text=">> Workflow Guide")

        # Separator
        sep_frame = ttk.Frame(self.notebook)
        self.notebook.add(sep_frame, text="---", state="disabled")

        # Setup category tabs
        for cat, params in SETUP_CATEGORIES.items():
            tab = self._build_category_tab(cat, params)
            self.notebook.add(tab, text=cat)

    # ---- Advisor Tab ----
    def _build_advisor_tab(self):
        outer = ttk.Frame(self.notebook)
        canvas = tk.Canvas(outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient=tk.VERTICAL, command=canvas.yview)
        frame = ttk.Frame(canvas, padding=15)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        for evt in ("<MouseWheel>",):
            canvas.bind(evt, lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        for evt, d in (("<Button-4>", -1), ("<Button-5>", 1)):
            canvas.bind(evt, lambda e, delta=d: canvas.yview_scroll(delta, "units"))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Setup Advisor — Generate an Intelligent Baseline",
                  font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 10))
        ttk.Label(frame, text=(
            "Select your car class and track type below. The advisor will generate a "
            "physics-informed baseline setup tailored to your combination, with specific "
            "warnings and tips for your car type."
        ), wraplength=800).pack(anchor="w", pady=(0, 15))

        # Car class selector
        car_frame = ttk.LabelFrame(frame, text="Car Class", padding=10)
        car_frame.pack(fill=tk.X, pady=5)
        self.car_class_var = tk.StringVar()
        car_names = list(CAR_CLASSES.keys())
        self.car_class_combo = ttk.Combobox(car_frame, textvariable=self.car_class_var,
                                            values=car_names, state="readonly", width=40)
        self.car_class_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.car_class_combo.bind("<<ComboboxSelected>>", self._on_car_class_selected)
        self.car_desc_var = tk.StringVar(value="Select a car class to see its description.")
        ttk.Label(car_frame, textvariable=self.car_desc_var,
                  wraplength=500, foreground="gray30").pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Track type selector
        track_frame = ttk.LabelFrame(frame, text="Track Type", padding=10)
        track_frame.pack(fill=tk.X, pady=5)
        self.track_type_var = tk.StringVar()
        track_names = list(TRACK_TYPES.keys())
        self.track_type_combo = ttk.Combobox(track_frame, textvariable=self.track_type_var,
                                             values=track_names, state="readonly", width=40)
        self.track_type_combo.pack(side=tk.LEFT, padx=(0, 10))
        self.track_type_combo.bind("<<ComboboxSelected>>", self._on_track_type_selected)
        self.track_desc_var = tk.StringVar(value="Select a track type to see its description.")
        ttk.Label(track_frame, textvariable=self.track_desc_var,
                  wraplength=500, foreground="gray30").pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Generate button
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=15)
        ttk.Button(btn_frame, text="Generate Baseline Setup",
                   command=self._generate_baseline).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(btn_frame, text="This will overwrite your current setup!",
                  foreground="red").pack(side=tk.LEFT)

        # Results area
        self.advisor_results = tk.Text(frame, height=20, wrap=tk.WORD, state=tk.DISABLED,
                                       font=("TkDefaultFont", 9))
        self.advisor_results.pack(fill=tk.BOTH, expand=True, pady=5)
        self.advisor_results.tag_configure("heading", font=("TkDefaultFont", 11, "bold"))
        self.advisor_results.tag_configure("warning", foreground="dark red",
                                           font=("TkDefaultFont", 9, "bold"))
        self.advisor_results.tag_configure("tip", foreground="dark green")

        return outer

    def _on_car_class_selected(self, event=None):
        name = self.car_class_var.get()
        if name in CAR_CLASSES:
            self.car_desc_var.set(CAR_CLASSES[name]["description"])

    def _on_track_type_selected(self, event=None):
        name = self.track_type_var.get()
        if name in TRACK_TYPES:
            self.track_desc_var.set(TRACK_TYPES[name]["description"])

    def _generate_baseline(self):
        car_class = self.car_class_var.get()
        track_type = self.track_type_var.get()
        if not car_class:
            messagebox.showwarning("Select Car Class",
                                   "Please select a car class before generating a baseline.")
            return

        setup, tips, warnings = generate_baseline(car_class, track_type or None)
        if setup is None:
            messagebox.showerror("Error", "\n".join(warnings))
            return

        self.setup = setup
        self._apply_setup_to_ui()
        label = f"{car_class}"
        if track_type:
            label += f" @ {track_type}"
        self.status_var.set(f"rFactor 2 Setup Editor — {label}")

        # Show results
        t = self.advisor_results
        t.config(state=tk.NORMAL)
        t.delete("1.0", tk.END)
        t.insert(tk.END, f"Baseline Generated: {label}\n\n", "heading")

        if warnings:
            t.insert(tk.END, "IMPORTANT WARNINGS:\n", "heading")
            for w in warnings:
                t.insert(tk.END, f"  * {w}\n", "warning")
            t.insert(tk.END, "\n")

        if tips:
            t.insert(tk.END, "TRACK-SPECIFIC TIPS:\n", "heading")
            for tip in tips:
                t.insert(tk.END, f"  * {tip}\n", "tip")
            t.insert(tk.END, "\n")

        t.insert(tk.END, "NEXT STEPS:\n", "heading")
        t.insert(tk.END, (
            "  1. Save this baseline (File > Save Setup) before making changes.\n"
            "  2. Go to the Workflow Guide tab for step-by-step tuning instructions.\n"
            "  3. Run 5-10 laps, then use the Problem Solver tab to fix handling issues.\n"
            "  4. Use Compare to see your changes vs the baseline.\n"
        ))
        t.config(state=tk.DISABLED)

    # ---- Problem Solver Tab ----
    def _build_problem_solver_tab(self):
        outer = ttk.Frame(self.notebook)
        canvas = tk.Canvas(outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient=tk.VERTICAL, command=canvas.yview)
        frame = ttk.Frame(canvas, padding=15)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        for evt in ("<MouseWheel>",):
            canvas.bind(evt, lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        for evt, d in (("<Button-4>", -1), ("<Button-5>", 1)):
            canvas.bind(evt, lambda e, delta=d: canvas.yview_scroll(delta, "units"))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Handling Problem Solver",
                  font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(frame, text=(
            "Select the handling problem you're experiencing. The solver will diagnose "
            "the likely causes and recommend specific parameter changes to fix it. "
            "Apply changes one at a time and test 2-3 laps between each."
        ), wraplength=800).pack(anchor="w", pady=(0, 15))

        # Problem selector
        sel_frame = ttk.LabelFrame(frame, text="What problem are you experiencing?", padding=10)
        sel_frame.pack(fill=tk.X, pady=5)
        self.problem_var = tk.StringVar()
        problem_names = list(HANDLING_PROBLEMS.keys())
        self.problem_combo = ttk.Combobox(sel_frame, textvariable=self.problem_var,
                                          values=problem_names, state="readonly", width=50)
        self.problem_combo.pack(side=tk.LEFT, padx=(0, 10))

        ttk.Button(sel_frame, text="Diagnose & Recommend",
                   command=self._diagnose_problem).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(sel_frame, text="Apply Top Fix",
                   command=self._apply_top_fix).pack(side=tk.LEFT)

        # Results
        self.problem_results = tk.Text(frame, height=25, wrap=tk.WORD, state=tk.DISABLED,
                                        font=("TkDefaultFont", 9))
        self.problem_results.pack(fill=tk.BOTH, expand=True, pady=5)
        self.problem_results.tag_configure("heading", font=("TkDefaultFont", 11, "bold"))
        self.problem_results.tag_configure("cause", foreground="dark red")
        self.problem_results.tag_configure("fix", foreground="dark blue",
                                            font=("TkDefaultFont", 9, "bold"))
        self.problem_results.tag_configure("explain", foreground="gray30")
        self.problem_results.tag_configure("current", foreground="gray50")

        self._current_recommendations = []
        return outer

    def _diagnose_problem(self):
        name = self.problem_var.get()
        if not name:
            messagebox.showwarning("Select Problem", "Please select a handling problem first.")
            return
        problem = get_problem_recommendations(name)
        if not problem:
            return

        t = self.problem_results
        t.config(state=tk.NORMAL)
        t.delete("1.0", tk.END)

        t.insert(tk.END, f"DIAGNOSIS: {name}\n\n", "heading")
        t.insert(tk.END, f"{problem['description']}\n\n")
        t.insert(tk.END, "Likely causes: ", "heading")
        t.insert(tk.END, f"{problem['causes']}\n\n", "cause")

        t.insert(tk.END, "RECOMMENDED CHANGES (in priority order):\n\n", "heading")

        self._current_recommendations = problem["recommendations"]
        for i, (cat, param, delta, explanation) in enumerate(problem["recommendations"], 1):
            current = self.setup.get(cat, {}).get(param, "?")
            info = SETUP_CATEGORIES.get(cat, {}).get(param)
            if info:
                vmin, vmax, step = info[:3]
                new_val = current + delta if current != "?" else delta
                new_val = max(vmin, min(vmax, new_val))
                if isinstance(step, float):
                    decimals = len(str(step).split('.')[-1])
                    new_val = round(new_val, decimals)
                    curr_str = f"{current:.{decimals}f}" if current != "?" else "?"
                    new_str = f"{new_val:.{decimals}f}"
                else:
                    new_val = int(round(new_val))
                    curr_str = str(current)
                    new_str = str(new_val)
                sign = "+" if delta > 0 else ""
                t.insert(tk.END, f"  {i}. [{cat}] {param}: {curr_str} -> {new_str} ({sign}{delta})\n", "fix")
            else:
                t.insert(tk.END, f"  {i}. [{cat}] {param}: change by {delta}\n", "fix")
            t.insert(tk.END, f"     {explanation}\n\n", "explain")

        t.insert(tk.END, "\nTIP: ", "heading")
        t.insert(tk.END, (
            "Click 'Apply Top Fix' to apply the #1 recommendation automatically. "
            "Test for 2-3 laps, then come back and diagnose again if needed.\n"
        ))
        t.config(state=tk.DISABLED)

    def _apply_top_fix(self):
        if not self._current_recommendations:
            messagebox.showinfo("No Recommendations", "Diagnose a problem first.")
            return
        cat, param, delta, explanation = self._current_recommendations[0]
        current = self.setup.get(cat, {}).get(param)
        if current is None:
            return
        info = SETUP_CATEGORIES.get(cat, {}).get(param)
        if not info:
            return
        vmin, vmax, step = info[:3]
        new_val = current + delta
        new_val = max(vmin, min(vmax, new_val))
        if isinstance(step, float):
            decimals = len(str(step).split('.')[-1])
            new_val = round(new_val, decimals)
        else:
            new_val = int(round(new_val))

        self.setup[cat][param] = new_val
        self._apply_setup_to_ui()
        messagebox.showinfo("Applied",
                            f"Changed [{cat}] {param} from {current} to {new_val}.\n\n"
                            f"Reason: {explanation}")
        # Remove applied recommendation
        self._current_recommendations = self._current_recommendations[1:]

    # ---- Workflow Guide Tab ----
    def _build_workflow_tab(self):
        outer = ttk.Frame(self.notebook)
        canvas = tk.Canvas(outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient=tk.VERTICAL, command=canvas.yview)
        frame = ttk.Frame(canvas, padding=15)
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        for evt in ("<MouseWheel>",):
            canvas.bind(evt, lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        for evt, d in (("<Button-4>", -1), ("<Button-5>", 1)):
            canvas.bind(evt, lambda e, delta=d: canvas.yview_scroll(delta, "units"))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Step-by-Step Setup Workflow",
                  font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(frame, text=(
            "Follow these steps in order to build a proper setup from the ground up. "
            "This is the correct order of operations used by professional race engineers. "
            "Don't skip steps — each one depends on the previous being reasonably dialed in."
        ), wraplength=800).pack(anchor="w", pady=(0, 15))

        for step_info in SETUP_WORKFLOW:
            step_frame = ttk.LabelFrame(
                frame,
                text=f"Step {step_info['step']}: {step_info['title']}",
                padding=10
            )
            step_frame.pack(fill=tk.X, pady=5)

            # Description
            desc = step_info["description"]
            ttk.Label(step_frame, text=desc, wraplength=800,
                      font=("TkDefaultFont", 9)).pack(anchor="w", fill=tk.X)

            # What to check
            check_frame = ttk.Frame(step_frame)
            check_frame.pack(fill=tk.X, pady=(8, 0))
            ttk.Label(check_frame, text="What to verify: ",
                      font=("TkDefaultFont", 9, "bold")).pack(side=tk.LEFT, anchor="n")
            ttk.Label(check_frame, text=step_info["what_to_check"],
                      wraplength=700, foreground="dark green",
                      font=("TkDefaultFont", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        return outer

    def _build_category_tab(self, cat, params):
        outer = ttk.Frame(self.notebook)
        canvas = tk.Canvas(outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient=tk.VERTICAL, command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind("<Configure>",
                          lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_mousewheel_linux(event):
            if event.num == 4:
                canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                canvas.yview_scroll(1, "units")

        canvas.bind("<MouseWheel>", _on_mousewheel)
        canvas.bind("<Button-4>", _on_mousewheel_linux)
        canvas.bind("<Button-5>", _on_mousewheel_linux)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.widgets[cat] = {}
        row = 0
        for name, (vmin, vmax, step, default, unit, tip) in params.items():
            self._build_param_row(scroll_frame, cat, name, vmin, vmax, step, default, unit, tip, row)
            row += 1

        return outer

    def _build_param_row(self, parent, cat, name, vmin, vmax, step, default, unit, tip, row):
        is_float = isinstance(step, float)
        resolution = step

        frame = ttk.LabelFrame(parent, text=f"{name} ({unit})", padding=(10, 5))
        frame.grid(row=row, column=0, sticky="ew", padx=10, pady=4)
        parent.columnconfigure(0, weight=1)

        # Variable
        if is_float:
            var = tk.DoubleVar(value=default)
        else:
            var = tk.IntVar(value=default)

        # Top row: slider + value
        slider_frame = ttk.Frame(frame)
        slider_frame.pack(fill=tk.X)

        ttk.Label(slider_frame, text=str(vmin), width=6, anchor="e").pack(side=tk.LEFT)

        scale = ttk.Scale(slider_frame, from_=vmin, to=vmax, variable=var,
                          orient=tk.HORIZONTAL,
                          command=lambda val, c=cat, n=name, s=step, f=is_float:
                              self._on_scale_change(val, c, n, s, f))
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Label(slider_frame, text=str(vmax), width=6).pack(side=tk.LEFT)

        fmt = f"{{:.{len(str(step).split('.')[-1])}f}}" if is_float else "{}"
        value_label = ttk.Label(slider_frame, text=fmt.format(default),
                                width=8, anchor="center",
                                font=("TkDefaultFont", 10, "bold"))
        value_label.pack(side=tk.LEFT, padx=(5, 0))

        # Compare indicator
        compare_label = ttk.Label(slider_frame, text="", width=12, foreground="red")
        compare_label.pack(side=tk.LEFT, padx=(5, 0))

        # Tip row
        tip_label = ttk.Label(frame, text=tip, wraplength=700,
                              foreground="gray40", font=("TkDefaultFont", 8))
        tip_label.pack(fill=tk.X, pady=(2, 0))

        self.widgets[cat][name] = (var, scale, value_label, compare_label, step, is_float, vmin, vmax)

    def _on_scale_change(self, val, cat, name, step, is_float):
        """Snap value to step increments and update display."""
        raw = float(val)
        info = self.widgets[cat][name]
        var, scale, value_label, compare_label, st, fl, vmin, vmax = info

        # Snap to step
        snapped = round(round((raw - vmin) / step) * step + vmin, 10)
        snapped = max(vmin, min(vmax, snapped))

        if is_float:
            decimals = len(str(step).split('.')[-1])
            snapped = round(snapped, decimals)
            var.set(snapped)
            value_label.config(text=f"{snapped:.{decimals}f}")
        else:
            snapped = int(snapped)
            var.set(snapped)
            value_label.config(text=str(snapped))

        self.setup[cat][name] = snapped
        self._update_compare_label(cat, name)

    def _update_compare_label(self, cat, name):
        """Update comparison indicator for a single parameter."""
        info = self.widgets[cat][name]
        compare_label = info[3]
        if self.compare_setup and cat in self.compare_setup and name in self.compare_setup[cat]:
            comp_val = self.compare_setup[cat][name]
            cur_val = self.setup[cat][name]
            diff = cur_val - comp_val
            if abs(diff) < 1e-9:
                compare_label.config(text="= same", foreground="green")
            else:
                sign = "+" if diff > 0 else ""
                is_float = info[5]
                if is_float:
                    decimals = len(str(info[4]).split('.')[-1])
                    compare_label.config(text=f"{sign}{diff:.{decimals}f}", foreground="red")
                else:
                    compare_label.config(text=f"{sign}{int(diff)}", foreground="red")
        else:
            compare_label.config(text="")

    def _update_all_compare_labels(self):
        for cat in self.widgets:
            for name in self.widgets[cat]:
                self._update_compare_label(cat, name)

    def _apply_setup_to_ui(self):
        """Push self.setup values into all widgets."""
        for cat, params in self.widgets.items():
            for name, (var, scale, value_label, compare_label, step, is_float, vmin, vmax) in params.items():
                val = self.setup.get(cat, {}).get(name, var.get())
                var.set(val)
                if is_float:
                    decimals = len(str(step).split('.')[-1])
                    value_label.config(text=f"{val:.{decimals}f}")
                else:
                    value_label.config(text=str(val))
        self._update_all_compare_labels()

    # ---- File Operations ----
    def new_setup(self):
        self.setup = get_default_setup()
        self._apply_setup_to_ui()
        self.status_var.set("rFactor 2 Setup Editor — New Setup")

    def save_setup(self):
        path = filedialog.asksaveasfilename(
            title="Save Setup",
            defaultextension=".json",
            filetypes=[("JSON Setup Files", "*.json"), ("All Files", "*.*")],
            initialdir=os.path.join(os.path.dirname(__file__), "setups"))
        if path:
            with open(path, "w") as f:
                json.dump(self.setup, f, indent=2)
            basename = os.path.basename(path)
            self.status_var.set(f"rFactor 2 Setup Editor — {basename}")
            messagebox.showinfo("Saved", f"Setup saved to:\n{path}")

    def load_setup(self):
        path = filedialog.askopenfilename(
            title="Open Setup",
            filetypes=[("JSON Setup Files", "*.json"), ("All Files", "*.*")],
            initialdir=os.path.join(os.path.dirname(__file__), "setups"))
        if path:
            try:
                with open(path) as f:
                    data = json.load(f)
                # Merge loaded data with defaults (handles missing keys)
                merged = get_default_setup()
                for cat in merged:
                    if cat in data:
                        for name in merged[cat]:
                            if name in data[cat]:
                                merged[cat][name] = data[cat][name]
                self.setup = merged
                self._apply_setup_to_ui()
                basename = os.path.basename(path)
                self.status_var.set(f"rFactor 2 Setup Editor — {basename}")
            except (json.JSONDecodeError, KeyError) as e:
                messagebox.showerror("Error", f"Failed to load setup:\n{e}")

    # ---- Compare ----
    def load_compare(self):
        path = filedialog.askopenfilename(
            title="Load Setup to Compare",
            filetypes=[("JSON Setup Files", "*.json"), ("All Files", "*.*")],
            initialdir=os.path.join(os.path.dirname(__file__), "setups"))
        if path:
            try:
                with open(path) as f:
                    data = json.load(f)
                merged = get_default_setup()
                for cat in merged:
                    if cat in data:
                        for name in merged[cat]:
                            if name in data[cat]:
                                merged[cat][name] = data[cat][name]
                self.compare_setup = merged
                self.compare_name = os.path.basename(path)
                self.compare_var.set(f"Comparing with: {self.compare_name}")
                self._update_all_compare_labels()
            except (json.JSONDecodeError, KeyError) as e:
                messagebox.showerror("Error", f"Failed to load compare setup:\n{e}")

    def clear_compare(self):
        self.compare_setup = None
        self.compare_name = ""
        self.compare_var.set("")
        self._update_all_compare_labels()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    root = tk.Tk()

    # Apply a nicer theme if available
    style = ttk.Style()
    available_themes = style.theme_names()
    for preferred in ("clam", "alt", "default"):
        if preferred in available_themes:
            style.theme_use(preferred)
            break

    app = RF2SetupApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
