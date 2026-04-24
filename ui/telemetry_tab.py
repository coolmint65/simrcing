"""Telemetry-driven setup suggestions.

Enter tire temps (inner/middle/outer per wheel), tire pressures (cold/hot),
and brake temps — the rules engine produces prioritized setup changes.

Separate from Problem Solver because the inputs are measurements (what
the car did on track) rather than symptoms (what the car felt like).
"""

import tkinter as tk
from tkinter import ttk, messagebox

from rf2 import telemetry_rules
from ui.scroll_helper import build_scrollable


class TelemetryMixin:
    def _build_telemetry_tab(self):
        outer, frame = build_scrollable(self.notebook)

        ttk.Label(frame, text="Telemetry-Driven Analysis",
                  font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(frame, text=(
            "Enter measured values from your last run (or try 'Populate from Live' "
            "if the rF2 Shared Memory plugin is available). The rules engine turns "
            "measurements into prioritized setup suggestions."
        ), wraplength=800).pack(anchor="w", pady=(0, 10))

        # ---- Tire temps grid -----------------------------------------------
        temps_frame = ttk.LabelFrame(frame, text="Tire Temperatures (°C)",
                                      padding=10)
        temps_frame.pack(fill=tk.X, pady=5)

        self._temp_vars = {}
        headers = ("Inner", "Middle", "Outer")
        ttk.Label(temps_frame, text="", width=6).grid(row=0, column=0)
        for col, h in enumerate(headers, start=1):
            ttk.Label(temps_frame, text=h,
                      font=("TkDefaultFont", 9, "bold")).grid(row=0, column=col, padx=4)
        for row, wheel in enumerate(telemetry_rules.WHEEL_NAMES, start=1):
            ttk.Label(temps_frame, text=wheel, width=6).grid(row=row, column=0, sticky="w")
            for col, key in enumerate(("inner", "middle", "outer"), start=1):
                var = tk.StringVar()
                ttk.Entry(temps_frame, textvariable=var, width=8).grid(row=row, column=col, padx=4)
                self._temp_vars[(wheel, key)] = var

        # ---- Pressures + brakes --------------------------------------------
        prs_frame = ttk.LabelFrame(frame, text="Tire Pressures (kPa) & Brake Temps (°C)",
                                    padding=10)
        prs_frame.pack(fill=tk.X, pady=5)

        self._pressure_cold_vars = {}
        self._pressure_hot_vars = {}
        self._brake_vars = {}

        ttk.Label(prs_frame, text="Wheel", width=6).grid(row=0, column=0)
        for col, h in enumerate(("Cold", "Hot", "Brake"), start=1):
            ttk.Label(prs_frame, text=h,
                      font=("TkDefaultFont", 9, "bold")).grid(row=0, column=col, padx=4)
        for row, wheel in enumerate(telemetry_rules.WHEEL_NAMES, start=1):
            ttk.Label(prs_frame, text=wheel, width=6).grid(row=row, column=0, sticky="w")
            cold = tk.StringVar(); hot = tk.StringVar(); brake = tk.StringVar()
            ttk.Entry(prs_frame, textvariable=cold, width=8).grid(row=row, column=1, padx=4)
            ttk.Entry(prs_frame, textvariable=hot, width=8).grid(row=row, column=2, padx=4)
            ttk.Entry(prs_frame, textvariable=brake, width=8).grid(row=row, column=3, padx=4)
            self._pressure_cold_vars[wheel] = cold
            self._pressure_hot_vars[wheel] = hot
            self._brake_vars[wheel] = brake

        # ---- Action buttons -------------------------------------------------
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(5, 10))
        ttk.Button(btn_frame, text="Analyze",
                   command=self._telemetry_analyze).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Populate from Live (rF2 SMMP)",
                   command=self._telemetry_populate_live).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Clear",
                   command=self._telemetry_clear).pack(side=tk.LEFT)

        # ---- Results --------------------------------------------------------
        self.telemetry_results = tk.Text(frame, height=16, wrap=tk.WORD, state=tk.DISABLED,
                                          font=("TkDefaultFont", 9))
        self.telemetry_results.pack(fill=tk.BOTH, expand=True, pady=5)
        self.telemetry_results.tag_configure("heading",
                                               font=("TkDefaultFont", 11, "bold"))
        self.telemetry_results.tag_configure("high", foreground="dark red",
                                               font=("TkDefaultFont", 9, "bold"))
        self.telemetry_results.tag_configure("med", foreground="dark orange")
        self.telemetry_results.tag_configure("low", foreground="gray30")
        return outer

    # ---- Actions ------------------------------------------------------------

    def _telemetry_clear(self):
        for var_map in (self._temp_vars,):
            for var in var_map.values():
                var.set("")
        for var_map in (self._pressure_cold_vars, self._pressure_hot_vars,
                         self._brake_vars):
            for var in var_map.values():
                var.set("")
        self._telemetry_set_result("")

    def _telemetry_collect(self):
        reading = telemetry_rules.TelemetryReading.empty()
        for wheel in telemetry_rules.WHEEL_NAMES:
            w = reading.wheels[wheel]
            w.tire_temp_inner = _parse_float(self._temp_vars[(wheel, "inner")].get())
            w.tire_temp_middle = _parse_float(self._temp_vars[(wheel, "middle")].get())
            w.tire_temp_outer = _parse_float(self._temp_vars[(wheel, "outer")].get())
            w.tire_pressure_cold = _parse_float(self._pressure_cold_vars[wheel].get())
            w.tire_pressure_hot = _parse_float(self._pressure_hot_vars[wheel].get())
            w.brake_temp = _parse_float(self._brake_vars[wheel].get())
        return reading

    def _telemetry_analyze(self):
        reading = self._telemetry_collect()
        suggestions = telemetry_rules.analyze(reading)
        if not suggestions:
            self._telemetry_set_result(
                "No issues detected in the readings you entered. Either the "
                "car is well-tuned or there isn't enough data — fill in more "
                "fields for a more complete analysis.")
            return
        lines = [f"Found {len(suggestions)} suggestion(s), highest priority first:\n"]
        for s in suggestions:
            arrow = "↑" if s.direction == "increase" else ("↓" if s.direction == "decrease" else "?")
            lines.append(f"[P{s.priority}] {s.category} / {s.param}  {arrow}")
            lines.append(f"    {s.reason}\n")
        self._telemetry_set_result("\n".join(lines), suggestions=suggestions)

    def _telemetry_set_result(self, text, suggestions=None):
        t = self.telemetry_results
        t.config(state=tk.NORMAL)
        t.delete("1.0", tk.END)
        if suggestions:
            for line in text.split("\n"):
                tag = "low"
                if line.startswith("[P1]") or line.startswith("[P2]"):
                    tag = "high"
                elif line.startswith("[P3]") or line.startswith("[P4]"):
                    tag = "med"
                t.insert(tk.END, line + "\n", tag)
        else:
            t.insert(tk.END, text)
        t.config(state=tk.DISABLED)

    def _telemetry_populate_live(self):
        from rf2 import telemetry as live
        try:
            with live.connect() as t:
                temps = t.tire_temps()
                brakes = t.brake_temps()
        except live.TelemetryUnavailable as e:
            messagebox.showwarning(
                "Live Telemetry",
                f"{e}\n\nYou can still analyze manually-entered readings below.")
            return
        if temps is None and brakes is None:
            messagebox.showinfo("Live Telemetry",
                                 "Connected, but the plugin's struct layout didn't "
                                 "match what this app expects. Fall back to manual entry.")
            return
        if temps:
            for wheel, val in temps.items():
                # We only have a single 'middle' from the current stub; fill it.
                self._temp_vars[(wheel, "middle")].set(f"{val:.1f}")
        if brakes:
            for wheel, val in brakes.items():
                self._brake_vars[wheel].set(f"{val:.0f}")
        messagebox.showinfo("Live Telemetry",
                             "Populated from live buffer. Run Analyze to get "
                             "suggestions.")


def _parse_float(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None
