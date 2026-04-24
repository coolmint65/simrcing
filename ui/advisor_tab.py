"""Advisor tab — resolve car + track from user text, generate a baseline setup."""

import tkinter as tk
from tkinter import ttk, messagebox

from rf2.cars import CARS, find_car
from rf2.tracks import TRACKS, find_track
from rf2.knowledge import CAR_CLASSES, TRACK_TYPES, generate_smart_baseline
from rf2.inference import (infer_car, infer_track, remember_car, remember_track,
                            get_learned_car, get_learned_track, load_learned)
from ui.scroll_helper import build_scrollable
from ui.wizard import run_wizard


class AdvisorMixin:
    def _build_advisor_tab(self):
        outer, frame = build_scrollable(self.notebook)

        ttk.Label(frame, text="Setup Advisor — Just Type Your Car and Track",
                  font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 10))
        ttk.Label(frame, text=(
            "Type the name of your car and track below. The advisor knows specific cars "
            "and tracks, their physics characteristics, and rF2's simulation meta. "
            "It will generate the right baseline setup automatically.\n\n"
            "If your car isn't in the database, select a car class as a fallback."
        ), wraplength=800).pack(anchor="w", pady=(0, 15))

        car_frame = ttk.LabelFrame(frame, text="Car (type to search)", padding=10)
        car_frame.pack(fill=tk.X, pady=5)

        car_entry_frame = ttk.Frame(car_frame)
        car_entry_frame.pack(fill=tk.X)

        self.car_entry_var = tk.StringVar()
        self.car_entry = ttk.Entry(car_entry_frame, textvariable=self.car_entry_var, width=45)
        self.car_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.car_entry.bind("<KeyRelease>", self._on_car_search)

        ttk.Label(car_entry_frame, text="or class:").pack(side=tk.LEFT, padx=(10, 5))
        self.car_class_var = tk.StringVar()
        self.car_class_combo = ttk.Combobox(car_entry_frame, textvariable=self.car_class_var,
                                            values=list(CAR_CLASSES.keys()),
                                            state="readonly", width=30)
        self.car_class_combo.pack(side=tk.LEFT)

        self.car_results_frame = ttk.Frame(car_frame)
        self.car_results_frame.pack(fill=tk.X, pady=(5, 0))
        self.car_listbox = tk.Listbox(self.car_results_frame, height=4,
                                       font=("TkDefaultFont", 9))
        self.car_listbox.pack(fill=tk.X)
        self.car_listbox.bind("<<ListboxSelect>>", self._on_car_selected)
        self._car_search_results = []

        self.car_desc_var = tk.StringVar(
            value="Type a car name (e.g. 'Porsche 911', 'Lotus 49', 'BMW GT3')...")
        ttk.Label(car_frame, textvariable=self.car_desc_var,
                  wraplength=800, foreground="gray30").pack(anchor="w", pady=(5, 0))

        track_frame = ttk.LabelFrame(frame, text="Track (type to search)", padding=10)
        track_frame.pack(fill=tk.X, pady=5)

        track_entry_frame = ttk.Frame(track_frame)
        track_entry_frame.pack(fill=tk.X)

        self.track_entry_var = tk.StringVar()
        self.track_entry = ttk.Entry(track_entry_frame, textvariable=self.track_entry_var, width=45)
        self.track_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.track_entry.bind("<KeyRelease>", self._on_track_search)

        ttk.Label(track_entry_frame, text="or type:").pack(side=tk.LEFT, padx=(10, 5))
        self.track_type_var = tk.StringVar()
        self.track_type_combo = ttk.Combobox(track_entry_frame, textvariable=self.track_type_var,
                                             values=list(TRACK_TYPES.keys()),
                                             state="readonly", width=30)
        self.track_type_combo.pack(side=tk.LEFT)

        self.track_results_frame = ttk.Frame(track_frame)
        self.track_results_frame.pack(fill=tk.X, pady=(5, 0))
        self.track_listbox = tk.Listbox(self.track_results_frame, height=4,
                                         font=("TkDefaultFont", 9))
        self.track_listbox.pack(fill=tk.X)
        self.track_listbox.bind("<<ListboxSelect>>", self._on_track_selected)
        self._track_search_results = []

        self.track_desc_var = tk.StringVar(
            value="Type a track name (e.g. 'Spa', 'Nordschleife', 'Monaco')...")
        ttk.Label(track_frame, textvariable=self.track_desc_var,
                  wraplength=800, foreground="gray30").pack(anchor="w", pady=(5, 0))

        meta_frame = ttk.Frame(frame)
        meta_frame.pack(fill=tk.X, pady=5)
        self.apply_meta_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(meta_frame,
                        text="Apply rF2 meta optimizations (min pressures, camber, brake ducts, toe)",
                        variable=self.apply_meta_var).pack(side=tk.LEFT)

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=10)
        ttk.Button(btn_frame, text="Generate Baseline Setup",
                   command=self._generate_baseline).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(btn_frame, text="This will overwrite your current setup!",
                  foreground="red").pack(side=tk.LEFT)

        self.advisor_results = tk.Text(frame, height=20, wrap=tk.WORD, state=tk.DISABLED,
                                       font=("TkDefaultFont", 9))
        self.advisor_results.pack(fill=tk.BOTH, expand=True, pady=5)
        self.advisor_results.tag_configure("heading", font=("TkDefaultFont", 11, "bold"))
        self.advisor_results.tag_configure("warning", foreground="dark red",
                                           font=("TkDefaultFont", 9, "bold"))
        self.advisor_results.tag_configure("tip", foreground="dark green")
        self.advisor_results.tag_configure("meta", foreground="purple",
                                           font=("TkDefaultFont", 9, "italic"))

        self._selected_car_data = None
        self._selected_car_name = None
        self._selected_track_data = None
        self._selected_track_name = None

        return outer

    def loaded_car(self):
        """Return the currently resolved car data, or None."""
        return self._selected_car_data

    def loaded_track(self):
        """Return the currently resolved track data, or None."""
        return self._selected_track_data

    def _on_car_search(self, event=None):
        query = self.car_entry_var.get()
        self.car_listbox.delete(0, tk.END)
        self._car_search_results = []
        self._selected_car_data = None
        self._selected_car_name = None
        if len(query) < 2:
            self.car_desc_var.set("Type a car name — I know 30+ cars, and can learn any new one...")
            return

        db_results = find_car(query)[:6]
        learned = load_learned()
        learned_results = [(n, d) for n, d in learned.get("cars", {}).items()
                           if query.lower() in n.lower()]

        for name, data in db_results:
            self._car_search_results.append((name, data, "db"))
            self.car_listbox.insert(tk.END, f"{name}  [{data['class']}]")
        for name, data in learned_results[:4]:
            self._car_search_results.append((name, data, "learned"))
            cls = data.get('class', '?')
            self.car_listbox.insert(tk.END, f"{name}  [{cls}] (remembered)")

        if self._car_search_results:
            self.car_desc_var.set(f"Found {len(self._car_search_results)} car(s). "
                                  "Click to select, or just hit Generate to auto-detect.")
        else:
            result = infer_car(query)
            if result["confidence"] > 0.2:
                cls = result["inferred"].get("class", "Unknown class")
                self.car_desc_var.set(
                    f"Not in database — detected as: {cls}. "
                    f"Hit Generate and I'll figure it out (or ask you a few questions).")
            else:
                self.car_desc_var.set(
                    "Unknown car — hit Generate and I'll ask you a few quick questions "
                    "to build a profile. I'll remember it for next time.")

    def _on_car_selected(self, event=None):
        sel = self.car_listbox.curselection()
        if not sel or sel[0] >= len(self._car_search_results):
            return
        name, data, source = self._car_search_results[sel[0]]
        self._selected_car_name = name
        self._selected_car_data = data
        self.car_entry_var.set(name)
        desc = (f"{name} — {data.get('class', '?')} | "
                f"{data.get('engine', '?')}-engine {data.get('drivetrain', '?')} | "
                f"{data.get('power', '?')}HP / {data.get('weight', '?')}kg | "
                f"Aero: {data.get('aero', '?')}")
        if not data.get('has_abs', True):
            desc += " | NO ABS"
        if not data.get('has_tc', True):
            desc += " | NO TC"
        if source == "learned":
            desc += " | (remembered)"
        self.car_desc_var.set(desc)

    def _on_track_search(self, event=None):
        query = self.track_entry_var.get()
        self.track_listbox.delete(0, tk.END)
        self._track_search_results = []
        self._selected_track_data = None
        self._selected_track_name = None
        if len(query) < 2:
            self.track_desc_var.set("Type a track name — I know 25+ tracks, and can learn any new one...")
            return

        db_results = find_track(query)[:6]
        learned = load_learned()
        learned_results = [(n, d) for n, d in learned.get("tracks", {}).items()
                           if query.lower() in n.lower()]

        for name, data in db_results:
            self._track_search_results.append((name, data, "db"))
            self.track_listbox.insert(tk.END, f"{name}  [{data['type']}]")
        for name, data in learned_results[:4]:
            self._track_search_results.append((name, data, "learned"))
            self.track_listbox.insert(tk.END, f"{name}  [{data.get('type', '?')}] (remembered)")

        if self._track_search_results:
            self.track_desc_var.set(f"Found {len(self._track_search_results)} track(s). "
                                     "Click to select, or just hit Generate.")
        else:
            result = infer_track(query)
            if result["confidence"] > 0.2:
                ttype = result["inferred"].get("type", "Unknown type")
                self.track_desc_var.set(
                    f"Not in database — detected as: {ttype}. "
                    f"Hit Generate to confirm or I'll ask a quick question.")
            else:
                self.track_desc_var.set(
                    "Unknown track — hit Generate and I'll ask a quick question. "
                    "I'll remember it for next time.")

    def _on_track_selected(self, event=None):
        sel = self.track_listbox.curselection()
        if not sel or sel[0] >= len(self._track_search_results):
            return
        name, data, source = self._track_search_results[sel[0]]
        self._selected_track_name = name
        self._selected_track_data = data
        self.track_entry_var.set(name)
        desc = (f"{name} — {data.get('type', '?')} | {data.get('length_km', '?')}km | "
                f"Surface: {data.get('surface', '?')}/5 | "
                f"Top speed: {data.get('top_speed', '?')}/5")
        if source == "learned":
            desc += " | (remembered)"
        self.track_desc_var.set(desc)

    def _resolve_car(self):
        """Resolve car input to (name, car_data) through DB -> learned -> infer -> wizard."""
        if self._selected_car_data:
            return self._selected_car_name, self._selected_car_data

        car_text = self.car_entry_var.get().strip()
        if not car_text and not self.car_class_var.get():
            return None, None

        if car_text:
            results = find_car(car_text)
            if results:
                return results[0]

            learned = get_learned_car(car_text)
            if learned:
                return car_text, learned

            inference = infer_car(car_text)
            profile = inference["inferred"]

            if inference["questions"]:
                answers = run_wizard(self.root,
                                     f"Tell me about: {car_text}", inference["questions"])
                if answers is None:
                    return None, None
                for key, val in answers.items():
                    if key == "class":
                        for cls_name in CAR_CLASSES:
                            if cls_name.lower() in val.lower() or val.lower().startswith(cls_name.lower()[:10]):
                                profile["class"] = cls_name
                                break
                        else:
                            profile["class"] = val.split("(")[0].strip()
                    elif key == "engine":
                        profile["engine"] = val.lower()
                    elif key == "has_abs":
                        profile["has_abs"] = val.lower() == "yes"

            profile.setdefault("class", "GT3")
            profile.setdefault("engine", "mid")
            profile.setdefault("drivetrain", "RWD")
            profile.setdefault("aero", "medium")
            profile.setdefault("weight", 1200)
            profile.setdefault("power", 450)
            profile.setdefault("has_abs", True)
            profile.setdefault("has_tc", True)
            profile.setdefault("bias", {})
            profile.setdefault("notes", f"User-defined: {car_text}")

            remember_car(car_text, profile)
            return car_text, profile

        if self.car_class_var.get():
            cls_name = self.car_class_var.get()
            profile = {
                "class": cls_name, "engine": "mid", "drivetrain": "RWD",
                "aero": "medium", "weight": 1200, "power": 450,
                "has_abs": True, "has_tc": True, "bias": {},
                "notes": f"Generic {cls_name}",
            }
            return cls_name, profile

        return None, None

    def _resolve_track(self):
        """Resolve track input to (name, track_data) through DB -> learned -> infer -> wizard."""
        if self._selected_track_data:
            return self._selected_track_name, self._selected_track_data

        track_text = self.track_entry_var.get().strip()
        if not track_text and not self.track_type_var.get():
            return None, None

        if track_text:
            results = find_track(track_text)
            if results:
                return results[0]

            learned = get_learned_track(track_text)
            if learned:
                return track_text, learned

            inference = infer_track(track_text)
            profile = inference["inferred"]

            if inference["questions"]:
                answers = run_wizard(self.root,
                                     f"Tell me about: {track_text}", inference["questions"])
                if answers is None:
                    return None, None
                for key, val in answers.items():
                    if key == "type":
                        for tt_name in TRACK_TYPES:
                            if tt_name.lower() in val.lower() or val.lower().startswith(tt_name.lower()[:10]):
                                profile["type"] = tt_name
                                break
                        else:
                            profile["type"] = val.split("(")[0].strip()

            profile.setdefault("type", "Technical / Tight Circuit")
            profile.setdefault("surface", 3)
            profile.setdefault("top_speed", 3)
            profile.setdefault("slow_corners", 4)
            profile.setdefault("elevation", "medium")
            profile.setdefault("length_km", 5.0)
            profile.setdefault("bias", {})
            profile.setdefault("notes", f"User-defined: {track_text}")

            remember_track(track_text, profile)
            return track_text, profile

        if self.track_type_var.get():
            tt_name = self.track_type_var.get()
            profile = {
                "type": tt_name, "surface": 3, "top_speed": 3,
                "slow_corners": 4, "elevation": "medium", "length_km": 5.0,
                "bias": {}, "notes": f"Generic {tt_name}",
            }
            return tt_name, profile

        return None, None

    def _generate_baseline(self):
        apply_meta = self.apply_meta_var.get()

        car_name, car_data = self._resolve_car()
        if not car_data:
            messagebox.showwarning("Need a Car",
                                   "Type a car name or select a car class to generate a setup.")
            return

        track_name, track_data = self._resolve_track()

        # Persist the resolved context so other tabs (Problem Solver, Journal) can use it.
        self._selected_car_name = car_name
        self._selected_car_data = car_data
        self._selected_track_name = track_name
        self._selected_track_data = track_data

        setup, tips, warnings, meta_changes = generate_smart_baseline(
            car_data, track_data, apply_meta)

        label = car_name or "Unknown"
        if track_name:
            label += f" @ {track_name}"

        self.setup = setup
        self._apply_setup_to_ui()
        self.status_var.set(f"rFactor 2 Setup Editor — {label}")
        self.journal_log_baseline(car_name, track_name)

        t = self.advisor_results
        t.config(state=tk.NORMAL)
        t.delete("1.0", tk.END)
        t.insert(tk.END, f"Baseline Generated: {label}\n\n", "heading")

        if car_name in CARS:
            t.insert(tk.END, "Car source: Built-in database\n", "tip")
        elif get_learned_car(car_name or ""):
            t.insert(tk.END, "Car source: Remembered from previous session\n", "tip")
        else:
            t.insert(tk.END, "Car source: Inferred from name / wizard answers\n", "tip")

        if track_data:
            if track_name in TRACKS:
                t.insert(tk.END, "Track source: Built-in database\n\n", "tip")
            elif get_learned_track(track_name or ""):
                t.insert(tk.END, "Track source: Remembered from previous session\n\n", "tip")
            else:
                t.insert(tk.END, "Track source: Inferred from name / wizard answers\n\n", "tip")
        else:
            t.insert(tk.END, "\n")

        if warnings:
            t.insert(tk.END, "CAR & TRACK NOTES:\n", "heading")
            for w in warnings:
                t.insert(tk.END, f"  * {w}\n\n", "warning")

        if meta_changes:
            t.insert(tk.END, "rF2 META APPLIED:\n", "heading")
            for desc, explanation in meta_changes:
                t.insert(tk.END, f"  * {desc}\n", "meta")
                t.insert(tk.END, f"    {explanation}\n\n")

        if tips:
            t.insert(tk.END, "TRACK-SPECIFIC TIPS:\n", "heading")
            for tip in tips:
                t.insert(tk.END, f"  * {tip}\n\n", "tip")

        t.insert(tk.END, "\nNEXT STEPS:\n", "heading")
        t.insert(tk.END, (
            "  1. Save this baseline (File > Save Setup) before making changes.\n"
            "  2. Go to the Workflow Guide tab for step-by-step tuning instructions.\n"
            "  3. Run 5-10 laps, then use the Problem Solver tab to fix handling issues.\n"
            "  4. Use Compare to see your changes vs the baseline.\n"
        ))
        t.config(state=tk.DISABLED)
