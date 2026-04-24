"""Journal tab — show recent parameter-change history across sessions."""

import tkinter as tk
from tkinter import ttk

from rf2 import history
from ui.scroll_helper import build_scrollable


class JournalMixin:
    def _build_journal_tab(self):
        outer, frame = build_scrollable(self.notebook)

        ttk.Label(frame, text="Setup Journal",
                  font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(frame, text=(
            "Append-only log of every parameter change, baseline generation, and "
            "setup save/load/import/export. Survives across sessions — review it to "
            "remember what you tried and why."
        ), wraplength=800).pack(anchor="w", pady=(0, 10))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=(0, 5))
        ttk.Button(btn_frame, text="Refresh", command=self._refresh_journal).pack(side=tk.LEFT)
        ttk.Label(btn_frame, text="  (showing most recent 200 entries)",
                  foreground="gray40").pack(side=tk.LEFT)

        self.journal_text = tk.Text(frame, height=30, wrap=tk.WORD, state=tk.DISABLED,
                                     font=("TkDefaultFont", 9))
        self.journal_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.journal_text.tag_configure("baseline", foreground="purple",
                                         font=("TkDefaultFont", 9, "bold"))
        self.journal_text.tag_configure("change", foreground="dark blue")
        self.journal_text.tag_configure("save", foreground="dark green")

        self._refresh_journal()
        return outer

    def _refresh_journal(self):
        entries = history.read_entries(limit=200)
        t = self.journal_text
        t.config(state=tk.NORMAL)
        t.delete("1.0", tk.END)
        if not entries:
            t.insert(tk.END, "(No journal entries yet. Make some changes and they'll appear here.)\n")
        for entry in entries:
            line = history.format_entry(entry) + "\n"
            kind = entry.get("kind", "")
            tag = "baseline" if kind == "baseline" else "save" if kind in ("save", "export_svm") else "change"
            t.insert(tk.END, line, tag)
        t.config(state=tk.DISABLED)

    # Hooks used by other tabs -------------------------------------------------

    def journal_log(self, category, param, old_value, new_value, reason=""):
        car = self._selected_car_name if getattr(self, "_selected_car_name", None) else None
        track = self._selected_track_name if getattr(self, "_selected_track_name", None) else None
        history.log_change(car, track, category, param, old_value, new_value, reason)

    def journal_log_baseline(self, car, track):
        history.log_baseline(car, track)

    def journal_log_event(self, kind, **fields):
        history.log_event(kind, **fields)
