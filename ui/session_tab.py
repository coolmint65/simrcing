"""Session Planner tab — plan a race weekend (sessions, fuel, tires, setup)."""

import os
import tkinter as tk
from tkinter import ttk, messagebox

from rf2 import session as session_mod
from rf2 import svm as svm_io
from ui.scroll_helper import build_scrollable


class SessionMixin:
    def _build_session_tab(self):
        outer, frame = build_scrollable(self.notebook)

        ttk.Label(frame, text="Race Weekend Planner",
                  font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(frame, text=(
            "Plan a full race weekend (sessions, fuel, tires, setup). Saves per "
            "car+track+date to user_profiles/sessions/."
        ), wraplength=800).pack(anchor="w", pady=(0, 10))

        # ---- Saved weekends -------------------------------------------------
        list_frame = ttk.LabelFrame(frame, text="Saved Weekends", padding=10)
        list_frame.pack(fill=tk.X, pady=5)

        self.session_list = tk.Listbox(list_frame, height=5,
                                        font=("TkDefaultFont", 9))
        self.session_list.pack(fill=tk.X)
        self.session_list.bind("<<ListboxSelect>>",
                                lambda _e: self._session_load_selected())

        btns = ttk.Frame(list_frame)
        btns.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(btns, text="New Weekend", command=self._session_new).pack(
            side=tk.LEFT, padx=(0, 5))
        ttk.Button(btns, text="Refresh", command=self._session_refresh_list).pack(
            side=tk.LEFT, padx=(0, 5))
        ttk.Button(btns, text="Delete Selected",
                   command=self._session_delete_selected).pack(side=tk.LEFT)

        # ---- Editor ---------------------------------------------------------
        editor = ttk.LabelFrame(frame, text="Editor", padding=10)
        editor.pack(fill=tk.BOTH, expand=True, pady=5)

        hdr = ttk.Frame(editor)
        hdr.pack(fill=tk.X, pady=2)
        ttk.Label(hdr, text="Car:", width=8).pack(side=tk.LEFT)
        self.session_car_var = tk.StringVar()
        ttk.Entry(hdr, textvariable=self.session_car_var, width=30).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(hdr, text="Track:", width=8).pack(side=tk.LEFT)
        self.session_track_var = tk.StringVar()
        ttk.Entry(hdr, textvariable=self.session_track_var, width=30).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(hdr, text="Date:").pack(side=tk.LEFT)
        self.session_date_var = tk.StringVar()
        ttk.Entry(hdr, textvariable=self.session_date_var, width=12).pack(side=tk.LEFT)

        self.session_frames_container = ttk.Frame(editor)
        self.session_frames_container.pack(fill=tk.BOTH, expand=True, pady=(10, 5))

        action = ttk.Frame(editor)
        action.pack(fill=tk.X)
        ttk.Button(action, text="Add Session",
                   command=self._session_add_row).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(action, text="Use Currently Loaded Car & Track",
                   command=self._session_use_loaded).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(action, text="Save",
                   command=self._session_save).pack(side=tk.LEFT, padx=(0, 5))

        self.session_summary_var = tk.StringVar(value="")
        ttk.Label(editor, textvariable=self.session_summary_var,
                  foreground="dark blue", font=("TkDefaultFont", 10, "bold"),
                  wraplength=800, justify="left").pack(anchor="w", pady=(10, 0))

        self._session_rows = []
        self._session_weekends_index = []
        self._session_refresh_list()
        return outer

    # ---- List actions -------------------------------------------------------

    def _session_refresh_list(self):
        self._session_weekends_index = session_mod.list_weekends()
        self.session_list.delete(0, tk.END)
        for _path, w in self._session_weekends_index:
            label = f"{w.date or '?'}  {w.car or '?'} @ {w.track or '?'} ({len(w.sessions)} session(s))"
            self.session_list.insert(tk.END, label)

    def _session_load_selected(self):
        sel = self.session_list.curselection()
        if not sel:
            return
        path, weekend = self._session_weekends_index[sel[0]]
        self._session_fill_editor(weekend)
        self._session_current_path = path

    def _session_delete_selected(self):
        sel = self.session_list.curselection()
        if not sel:
            return
        path, weekend = self._session_weekends_index[sel[0]]
        if not messagebox.askyesno("Delete",
                                     f"Delete '{weekend.car} @ {weekend.track} "
                                     f"{weekend.date}'?"):
            return
        session_mod.delete(path)
        self._session_refresh_list()

    # ---- Editor -------------------------------------------------------------

    def _session_new(self):
        car = self._selected_car_name if getattr(self, "_selected_car_name", None) else ""
        track = self._selected_track_name if getattr(self, "_selected_track_name", None) else ""
        weekend = session_mod.new_default_weekend(car, track)
        self._session_fill_editor(weekend)
        self._session_current_path = None

    def _session_use_loaded(self):
        if getattr(self, "_selected_car_name", None):
            self.session_car_var.set(self._selected_car_name)
        if getattr(self, "_selected_track_name", None):
            self.session_track_var.set(self._selected_track_name)

    def _session_fill_editor(self, weekend):
        self.session_car_var.set(weekend.car)
        self.session_track_var.set(weekend.track)
        self.session_date_var.set(weekend.date)
        for row in self._session_rows:
            row["frame"].destroy()
        self._session_rows = []
        for sess in weekend.sessions:
            self._session_add_row(sess)
        self._session_recalc_summary()

    def _session_add_row(self, sess=None):
        if sess is None:
            sess = session_mod.Session()
        row_frame = ttk.LabelFrame(self.session_frames_container,
                                    text="Session", padding=6)
        row_frame.pack(fill=tk.X, pady=3)

        fields = {}
        defs = [
            ("name", "Type", 12, sess.name),
            ("duration_min", "Minutes", 8, sess.duration_min),
            ("duration_laps", "Laps", 6, sess.duration_laps),
            ("expected_lap_time_s", "Ref Lap (s)", 10, sess.expected_lap_time_s),
            ("fuel_per_lap_l", "L/lap", 7, sess.fuel_per_lap_l),
            ("starting_compound", "Compound", 10, sess.starting_compound),
        ]
        row_line = ttk.Frame(row_frame)
        row_line.pack(fill=tk.X)
        for key, label, width, default in defs:
            ttk.Label(row_line, text=label + ":").pack(side=tk.LEFT, padx=(0, 2))
            var = tk.StringVar(value=str(default))
            entry = ttk.Entry(row_line, textvariable=var, width=width)
            entry.pack(side=tk.LEFT, padx=(0, 5))
            entry.bind("<KeyRelease>", lambda _e: self._session_recalc_summary())
            fields[key] = var

        notes_row = ttk.Frame(row_frame)
        notes_row.pack(fill=tk.X, pady=(3, 0))
        ttk.Label(notes_row, text="Setup:").pack(side=tk.LEFT, padx=(0, 2))
        setup_var = tk.StringVar(value=sess.setup_path)
        setup_entry = ttk.Entry(notes_row, textvariable=setup_var, width=60)
        setup_entry.pack(side=tk.LEFT, padx=(0, 5))
        fields["setup_path"] = setup_var
        ttk.Button(notes_row, text="Load Setup",
                   command=lambda v=setup_var: self._session_load_setup(v)).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Label(notes_row, text="Notes:").pack(side=tk.LEFT, padx=(10, 2))
        notes_var = tk.StringVar(value=sess.notes)
        ttk.Entry(notes_row, textvariable=notes_var, width=30).pack(side=tk.LEFT)
        fields["notes"] = notes_var

        ttk.Button(row_frame, text="Remove",
                   command=lambda rf=row_frame: self._session_remove_row(rf)).pack(
            side=tk.RIGHT, pady=(3, 0))

        self._session_rows.append({"frame": row_frame, "fields": fields})
        self._session_recalc_summary()

    def _session_remove_row(self, row_frame):
        self._session_rows = [r for r in self._session_rows if r["frame"] != row_frame]
        row_frame.destroy()
        self._session_recalc_summary()

    def _session_collect(self):
        sessions = []
        for row in self._session_rows:
            f = row["fields"]
            try:
                sess = session_mod.Session(
                    name=f["name"].get(),
                    duration_min=float(f["duration_min"].get() or 0),
                    duration_laps=int(float(f["duration_laps"].get() or 0)),
                    expected_lap_time_s=float(f["expected_lap_time_s"].get() or 0),
                    fuel_per_lap_l=float(f["fuel_per_lap_l"].get() or 0),
                    starting_compound=f["starting_compound"].get(),
                    setup_path=f["setup_path"].get(),
                    notes=f["notes"].get(),
                )
            except ValueError:
                continue
            sessions.append(sess)
        return session_mod.RaceWeekend(
            car=self.session_car_var.get(),
            track=self.session_track_var.get(),
            date=self.session_date_var.get(),
            sessions=sessions,
        )

    def _session_recalc_summary(self):
        weekend = self._session_collect()
        lines = []
        total_fuel = 0.0
        for s in weekend.sessions:
            laps = s.estimated_laps()
            fuel = s.required_fuel_l()
            total_fuel += fuel
            lines.append(
                f"  {s.name}: ~{laps} laps, ~{fuel:.1f} L fuel "
                f"(compound: {s.starting_compound})"
            )
        lines.append(f"\nTotal fuel across weekend: ~{total_fuel:.1f} L")
        self.session_summary_var.set("\n".join(lines))

    def _session_load_setup(self, setup_var):
        path = setup_var.get().strip()
        if not path or not os.path.exists(path):
            messagebox.showinfo("Session Planner",
                                 "Setup path is empty or file does not exist.")
            return
        try:
            partial, unmapped = svm_io.read_svm(path)
        except OSError as e:
            messagebox.showerror("Session Planner", f"Could not load setup: {e}")
            return
        self._merge_into_setup(partial)
        self._apply_setup_to_ui()
        self.status_var.set(
            f"rFactor 2 Setup Editor — {os.path.basename(path)} "
            "(from Session Planner)")
        self.journal_log_event("session_load_setup", path=path)

    def _session_save(self):
        weekend = self._session_collect()
        if not weekend.car or not weekend.track:
            messagebox.showwarning("Session Planner",
                                    "Fill in Car and Track before saving.")
            return
        path = session_mod.save(weekend)
        self.journal_log_event("session_save", path=path,
                                car=weekend.car, track=weekend.track)
        self._session_refresh_list()
        messagebox.showinfo("Session Planner", f"Saved to:\n{path}")
