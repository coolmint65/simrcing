"""Library tab — browse and search the indexed .svm setup corpus."""

import os
import tkinter as tk
from datetime import datetime
from tkinter import ttk, filedialog, messagebox

from rf2 import setup_library, svm as svm_io
from ui.scroll_helper import build_scrollable


class LibraryMixin:
    def _build_library_tab(self):
        outer, frame = build_scrollable(self.notebook)

        ttk.Label(frame, text="Setup Library",
                  font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(frame, text=(
            "Indexes every .svm file under the configured root folders. "
            "Type a car and/or track to find specific setups someone (you, a team, "
            "a download) already tuned for that combo."
        ), wraplength=800).pack(anchor="w", pady=(0, 10))

        # ---- Roots ----------------------------------------------------------
        roots_frame = ttk.LabelFrame(frame, text="Library Roots", padding=10)
        roots_frame.pack(fill=tk.X, pady=5)

        self.library_roots_list = tk.Listbox(roots_frame, height=3,
                                              font=("TkDefaultFont", 9))
        self.library_roots_list.pack(fill=tk.X)

        roots_btns = ttk.Frame(roots_frame)
        roots_btns.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(roots_btns, text="Add Folder...",
                   command=self._library_add_root).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(roots_btns, text="Remove Selected",
                   command=self._library_remove_root).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(roots_btns, text="Auto-Detect rF2 UserData",
                   command=self._library_autodetect).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(roots_btns, text="Rescan All",
                   command=self._library_rescan).pack(side=tk.LEFT, padx=(0, 5))

        self.library_status_var = tk.StringVar(value="(library not yet scanned)")
        ttk.Label(roots_frame, textvariable=self.library_status_var,
                  foreground="gray40").pack(anchor="w", pady=(5, 0))

        # ---- Search ---------------------------------------------------------
        search_frame = ttk.LabelFrame(frame, text="Search", padding=10)
        search_frame.pack(fill=tk.X, pady=5)

        row = ttk.Frame(search_frame)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="Car:", width=8).pack(side=tk.LEFT)
        self.library_car_var = tk.StringVar()
        ent = ttk.Entry(row, textvariable=self.library_car_var, width=30)
        ent.pack(side=tk.LEFT, padx=(0, 10))
        ent.bind("<KeyRelease>", lambda _e: self._library_refresh_results())
        ttk.Label(row, text="Track:", width=8).pack(side=tk.LEFT)
        self.library_track_var = tk.StringVar()
        ent = ttk.Entry(row, textvariable=self.library_track_var, width=30)
        ent.pack(side=tk.LEFT)
        ent.bind("<KeyRelease>", lambda _e: self._library_refresh_results())

        # ---- Results --------------------------------------------------------
        results_frame = ttk.LabelFrame(frame, text="Results", padding=5)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ("car", "track", "name", "modified")
        self.library_tree = ttk.Treeview(results_frame, columns=columns,
                                          show="headings", height=14)
        for col, width in (("car", 180), ("track", 180), ("name", 160), ("modified", 120)):
            self.library_tree.heading(col, text=col.title())
            self.library_tree.column(col, width=width, anchor="w")
        self.library_tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        tv_scroll = ttk.Scrollbar(results_frame, orient=tk.VERTICAL,
                                    command=self.library_tree.yview)
        tv_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.library_tree.configure(yscrollcommand=tv_scroll.set)
        self.library_tree.bind("<Double-1>", lambda _e: self._library_load_selected())

        # ---- Action buttons -------------------------------------------------
        action_frame = ttk.Frame(frame)
        action_frame.pack(fill=tk.X, pady=5)
        ttk.Button(action_frame, text="Load Selected into Editor",
                   command=self._library_load_selected).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(action_frame, text="Open Containing Folder",
                   command=self._library_reveal_selected).pack(side=tk.LEFT, padx=(0, 5))

        # initial load
        self.root.after_idle(self._library_initial_load)
        return outer

    # ---- Actions ------------------------------------------------------------

    def _library_initial_load(self):
        cached = setup_library.load_cache()
        if cached and cached.entries:
            self.library_index = cached
            self._library_update_roots_list()
            self._library_set_status_from_cache(cached)
            self._library_refresh_results()
        else:
            self.library_index = setup_library.LibraryIndex()
            self._library_autodetect(silent=True)

    def _library_autodetect(self, silent=False):
        detected = setup_library.default_rf2_paths()
        if not detected:
            if not silent:
                messagebox.showinfo("Auto-Detect",
                                     "No rF2 UserData folder found in the standard locations. "
                                     "Use Add Folder... to point at it manually.")
            return
        existing = set(self._library_get_roots())
        added = []
        for path in detected:
            if path not in existing:
                existing.add(path)
                added.append(path)
        self._library_set_roots(sorted(existing))
        if added and not silent:
            messagebox.showinfo("Auto-Detect",
                                 f"Added {len(added)} folder(s):\n\n" + "\n".join(added))
        self._library_rescan()

    def _library_add_root(self):
        path = filedialog.askdirectory(title="Pick a folder containing .svm setups")
        if not path:
            return
        roots = self._library_get_roots()
        if path in roots:
            return
        roots.append(path)
        self._library_set_roots(roots)
        self._library_rescan()

    def _library_remove_root(self):
        sel = self.library_roots_list.curselection()
        if not sel:
            return
        roots = self._library_get_roots()
        path = roots[sel[0]]
        roots.remove(path)
        self._library_set_roots(roots)
        self._library_rescan()

    def _library_rescan(self):
        roots = self._library_get_roots()
        self.library_status_var.set(f"Scanning {len(roots)} root(s)...")
        self.root.update_idletasks()
        index = setup_library.scan(roots)
        self.library_index = index
        setup_library.save_cache(index)
        self._library_set_status_from_cache(index)
        self._library_refresh_results()

    def _library_set_status_from_cache(self, index):
        self.library_status_var.set(
            f"{index.count()} setups indexed across {len(index.roots)} root(s).")

    def _library_refresh_results(self):
        if not hasattr(self, "library_index"):
            return
        car_q = self.library_car_var.get().strip()
        track_q = self.library_track_var.get().strip()
        entries = self.library_index.search(car_q, track_q)[:200]
        self.library_tree.delete(*self.library_tree.get_children())
        for e in entries:
            mtime_str = datetime.fromtimestamp(e.mtime).strftime("%Y-%m-%d %H:%M")
            self.library_tree.insert(
                "", tk.END, values=(e.raw_car_folder or e.car,
                                      e.raw_track_folder or e.track,
                                      e.name, mtime_str),
                tags=(e.path,))

    def _library_selected_entry(self):
        sel = self.library_tree.selection()
        if not sel:
            return None
        item = sel[0]
        tags = self.library_tree.item(item, "tags")
        if not tags:
            return None
        path = tags[0]
        for e in self.library_index.entries:
            if e.path == path:
                return e
        return None

    def _library_load_selected(self):
        entry = self._library_selected_entry()
        if entry is None:
            messagebox.showinfo("Library", "Select a setup first.")
            return
        try:
            partial, unmapped = svm_io.read_svm(entry.path)
        except OSError as exc:
            messagebox.showerror("Library", f"Could not read setup: {exc}")
            return
        self._merge_into_setup(partial)
        self._apply_setup_to_ui()
        self.status_var.set(
            f"rFactor 2 Setup Editor — {entry.name}  "
            f"({entry.raw_car_folder or entry.car} @ {entry.raw_track_folder or entry.track})")
        self.journal_log_event("library_load", path=entry.path,
                                car=entry.car, track=entry.track, name=entry.name)
        if unmapped:
            messagebox.showinfo(
                "Library",
                f"Loaded {entry.name}. {len(unmapped)} key(s) had no mapping; "
                "those parameters stayed at defaults.")

    def _library_reveal_selected(self):
        entry = self._library_selected_entry()
        if entry is None:
            return
        folder = os.path.dirname(entry.path)
        try:
            os.startfile(folder)  # Windows only — fine for this app's target
        except (AttributeError, OSError) as exc:
            messagebox.showinfo("Library", f"Folder: {folder}\n\n(could not open: {exc})")

    # ---- Root-list bookkeeping ----------------------------------------------

    def _library_get_roots(self):
        return list(self._prefs.get("library_roots", []))

    def _library_set_roots(self, roots):
        self._prefs["library_roots"] = list(roots)
        from ui.app import _save_prefs  # lazy import to avoid import cycle at module load
        _save_prefs(self._prefs)
        self._library_update_roots_list()

    def _library_update_roots_list(self):
        self.library_roots_list.delete(0, tk.END)
        for path in self._library_get_roots():
            exists = "" if os.path.isdir(path) else "  (missing)"
            self.library_roots_list.insert(tk.END, path + exists)

    # ---- Public API called from other tabs ----------------------------------

    def library_matches_for(self, car_name, track_name):
        """Return entries matching a car+track combo, or [] if the library
        hasn't been loaded yet. Used by the Advisor tab after resolving."""
        if not hasattr(self, "library_index"):
            return []
        return self.library_index.search(car_name or "", track_name or "")[:10]
