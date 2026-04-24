"""Calculators tab — fuel needed for a stint, final drive for a target top speed."""

import tkinter as tk
from tkinter import ttk, messagebox

from rf2.calculators import (fuel_needed, final_drive_for_top_speed,
                              top_speed_for_final_drive)
from rf2.parameters import SETUP_CATEGORIES
from ui.scroll_helper import build_scrollable


class CalcMixin:
    def _build_calc_tab(self):
        outer, frame = build_scrollable(self.notebook)

        ttk.Label(frame, text="Calculators",
                  font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(frame, text=(
            "Practical race-engineering calculators. Results can be written back into "
            "the loaded setup."
        ), wraplength=800).pack(anchor="w", pady=(0, 15))

        self._build_fuel_calc(frame)
        self._build_gear_calc(frame)

        return outer

    # ---- Fuel ---------------------------------------------------------------

    def _build_fuel_calc(self, parent):
        fuel_frame = ttk.LabelFrame(parent, text="Fuel Calculator", padding=10)
        fuel_frame.pack(fill=tk.X, pady=5)

        self.fuel_laps_var = tk.StringVar(value="30")
        self.fuel_consumption_var = tk.StringVar(value="2.4")
        self.fuel_safety_var = tk.StringVar(value="1.0")

        row = ttk.Frame(fuel_frame)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="Laps in stint:", width=25).pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.fuel_laps_var, width=10).pack(side=tk.LEFT)

        row = ttk.Frame(fuel_frame)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="Consumption (L / lap):", width=25).pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.fuel_consumption_var, width=10).pack(side=tk.LEFT)

        row = ttk.Frame(fuel_frame)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="Safety buffer (laps):", width=25).pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.fuel_safety_var, width=10).pack(side=tk.LEFT)

        btn_row = ttk.Frame(fuel_frame)
        btn_row.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(btn_row, text="Calculate", command=self._calc_fuel).pack(side=tk.LEFT)
        ttk.Button(btn_row, text="Apply to Setup (Fuel Load)",
                   command=self._apply_fuel).pack(side=tk.LEFT, padx=(10, 0))

        self.fuel_result_var = tk.StringVar(value="")
        ttk.Label(fuel_frame, textvariable=self.fuel_result_var,
                  foreground="dark blue",
                  font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(5, 0))

    def _calc_fuel(self):
        try:
            laps = float(self.fuel_laps_var.get())
            cons = float(self.fuel_consumption_var.get())
            safety = float(self.fuel_safety_var.get())
            liters = fuel_needed(laps, cons, safety)
        except ValueError as e:
            messagebox.showerror("Fuel Calculator", f"Invalid input: {e}")
            return
        self._fuel_liters = liters
        self.fuel_result_var.set(f"Fuel needed: {liters:.1f} L  "
                                  f"(including {self.fuel_safety_var.get()}-lap buffer)")

    def _apply_fuel(self):
        if not hasattr(self, "_fuel_liters"):
            self._calc_fuel()
            if not hasattr(self, "_fuel_liters"):
                return
        info = SETUP_CATEGORIES["Engine"]["Fuel Load"]
        vmin, vmax = info[0], info[1]
        liters = max(vmin, min(vmax, int(round(self._fuel_liters))))
        old = self.setup["Engine"]["Fuel Load"]
        self.setup["Engine"]["Fuel Load"] = liters
        self._apply_setup_to_ui()
        self.journal_log("Engine", "Fuel Load", old, liters,
                         reason=f"Fuel calculator: {self.fuel_laps_var.get()} laps × "
                                f"{self.fuel_consumption_var.get()} L/lap")

    # ---- Gear ratio ---------------------------------------------------------

    def _build_gear_calc(self, parent):
        gear_frame = ttk.LabelFrame(parent, text="Gear Ratio Calculator (final drive)",
                                    padding=10)
        gear_frame.pack(fill=tk.X, pady=5)

        ttk.Label(gear_frame, text=(
            "Given a target top speed at the end of the longest straight, compute the "
            "final drive that hits the rev limiter in top gear. Pulls the current 6th "
            "gear ratio and rev limit from the loaded setup."
        ), wraplength=700, foreground="gray40").pack(anchor="w", pady=(0, 8))

        self.gear_topspeed_var = tk.StringVar(value="280")
        self.gear_tire_radius_var = tk.StringVar(value="0.33")

        row = ttk.Frame(gear_frame)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="Target top speed (km/h):", width=30).pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.gear_topspeed_var, width=10).pack(side=tk.LEFT)

        row = ttk.Frame(gear_frame)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="Tire radius (m):", width=30).pack(side=tk.LEFT)
        ttk.Entry(row, textvariable=self.gear_tire_radius_var, width=10).pack(side=tk.LEFT)

        btn_row = ttk.Frame(gear_frame)
        btn_row.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(btn_row, text="Compute Final Drive",
                   command=self._calc_gear).pack(side=tk.LEFT)
        ttk.Button(btn_row, text="Apply to Setup",
                   command=self._apply_gear).pack(side=tk.LEFT, padx=(10, 0))

        self.gear_result_var = tk.StringVar(value="")
        ttk.Label(gear_frame, textvariable=self.gear_result_var,
                  foreground="dark blue",
                  font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(5, 0))

    def _calc_gear(self):
        try:
            target = float(self.gear_topspeed_var.get())
            radius = float(self.gear_tire_radius_var.get())
            rev_limit = self.setup["Engine"]["Rev Limit"]
            top_gear = self.setup["Gearing"]["6th Gear"]
            fd = final_drive_for_top_speed(target, rev_limit, top_gear, radius)
            check_kph = top_speed_for_final_drive(fd, rev_limit, top_gear, radius)
        except (ValueError, KeyError) as e:
            messagebox.showerror("Gear Calculator", f"Could not compute: {e}")
            return
        self._final_drive = fd
        self.gear_result_var.set(
            f"Final Drive: {fd:.2f}   (verifies to {check_kph:.1f} km/h "
            f"at {rev_limit} RPM in 6th × {top_gear})")

    def _apply_gear(self):
        if not hasattr(self, "_final_drive"):
            self._calc_gear()
            if not hasattr(self, "_final_drive"):
                return
        info = SETUP_CATEGORIES["Gearing"]["Final Drive"]
        vmin, vmax = info[0], info[1]
        fd = max(vmin, min(vmax, self._final_drive))
        old = self.setup["Gearing"]["Final Drive"]
        self.setup["Gearing"]["Final Drive"] = fd
        self._apply_setup_to_ui()
        self.journal_log("Gearing", "Final Drive", old, fd,
                         reason=f"Gear calculator: target {self.gear_topspeed_var.get()} km/h")
