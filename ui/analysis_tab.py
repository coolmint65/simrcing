"""Analysis tab — run statistics across the library corpus for a car+track
and flag where your current setup deviates from the crowd."""

import tkinter as tk
from tkinter import ttk, messagebox

from rf2 import analysis, setup_library
from rf2.parameters import param_decimals, SETUP_CATEGORIES
from ui.scroll_helper import build_scrollable


class AnalysisMixin:
    def _build_analysis_tab(self):
        outer, frame = build_scrollable(self.notebook)

        ttk.Label(frame, text="Setup Corpus Analysis",
                  font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(frame, text=(
            "Analyzes every library setup matching the car + track you specify. "
            "Shows how consensual each parameter is, which of your current values "
            "are outliers, and which saved setup best represents the median."
        ), wraplength=800).pack(anchor="w", pady=(0, 10))

        input_frame = ttk.LabelFrame(frame, text="Target", padding=10)
        input_frame.pack(fill=tk.X, pady=5)

        row = ttk.Frame(input_frame)
        row.pack(fill=tk.X, pady=2)
        ttk.Label(row, text="Car:", width=8).pack(side=tk.LEFT)
        self.analysis_car_var = tk.StringVar()
        ttk.Entry(row, textvariable=self.analysis_car_var, width=30).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(row, text="Track:", width=8).pack(side=tk.LEFT)
        self.analysis_track_var = tk.StringVar()
        ttk.Entry(row, textvariable=self.analysis_track_var, width=30).pack(side=tk.LEFT)

        btn_row = ttk.Frame(input_frame)
        btn_row.pack(fill=tk.X, pady=(5, 0))
        ttk.Button(btn_row, text="Use Currently Loaded Car & Track",
                   command=self._analysis_use_loaded).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_row, text="Analyze",
                   command=self._analysis_run).pack(side=tk.LEFT, padx=(0, 5))

        self.analysis_results = tk.Text(frame, height=30, wrap=tk.WORD, state=tk.DISABLED,
                                         font=("TkDefaultFont", 9))
        self.analysis_results.pack(fill=tk.BOTH, expand=True, pady=5)
        self.analysis_results.tag_configure("heading", font=("TkDefaultFont", 11, "bold"))
        self.analysis_results.tag_configure("sub", font=("TkDefaultFont", 10, "bold"),
                                             foreground="gray20")
        self.analysis_results.tag_configure("outlier", foreground="dark red",
                                             font=("TkDefaultFont", 9, "bold"))
        self.analysis_results.tag_configure("consensus", foreground="dark green")
        self.analysis_results.tag_configure("dim", foreground="gray50")

        return outer

    def _analysis_use_loaded(self):
        if getattr(self, "_selected_car_name", None):
            self.analysis_car_var.set(self._selected_car_name)
        if getattr(self, "_selected_track_name", None):
            self.analysis_track_var.set(self._selected_track_name)

    def _analysis_run(self):
        if not hasattr(self, "library_index"):
            messagebox.showinfo("Analysis",
                                 "Library hasn't been scanned yet. "
                                 "Open the Library tab first.")
            return

        car_q = self.analysis_car_var.get().strip()
        track_q = self.analysis_track_var.get().strip()
        entries = self.library_index.search(car_q, track_q)
        if len(entries) < 2:
            messagebox.showinfo("Analysis",
                                 f"Need at least 2 matching setups to compare; "
                                 f"found {len(entries)}.")
            return

        loaded = analysis.load_setups(entries)
        if len(loaded) < 2:
            messagebox.showerror("Analysis",
                                  "Could not read enough .svm files to compare.")
            return

        stats = analysis.param_stats(loaded)
        outliers = analysis.outliers_vs(stats, self.setup)
        ranked = analysis.consensus_rank(stats)
        closest, closest_d = analysis.closest_to_median(loaded, stats)

        t = self.analysis_results
        t.config(state=tk.NORMAL)
        t.delete("1.0", tk.END)

        header = f"Analyzed {len(loaded)} setup(s)"
        if car_q:
            header += f" for car '{car_q}'"
        if track_q:
            header += f" at '{track_q}'"
        t.insert(tk.END, header + "\n\n", "heading")

        if closest:
            t.insert(tk.END, "CLOSEST TO MEDIAN (most representative of the corpus):\n", "sub")
            t.insert(tk.END,
                      f"  {closest.name}  "
                      f"({closest.raw_car_folder or closest.car} @ "
                      f"{closest.raw_track_folder or closest.track})\n",
                      "consensus")
            t.insert(tk.END, f"  Normalized distance: {closest_d:.3f}\n\n", "dim")

        if outliers:
            t.insert(tk.END,
                      f"YOUR OUTLIERS ({len(outliers)} parameter(s) "
                      f">{analysis.OUTLIER_SIGMA}σ from corpus median):\n",
                      "sub")
            for cat, param, ours, median, z, stdev in outliers[:20]:
                info = SETUP_CATEGORIES.get(cat, {}).get(param)
                if info:
                    dec = param_decimals(info[2])
                    ours_s = f"{ours:.{dec}f}"
                    med_s = f"{median:.{dec}f}"
                    sd_s = f"σ={stdev:.{dec}f}"
                else:
                    ours_s, med_s, sd_s = str(ours), str(median), f"σ={stdev}"
                z_s = f"{z:.1f}σ" if z != float("inf") else "unanimous corpus"
                t.insert(tk.END,
                          f"  [{cat}] {param}: you={ours_s}  median={med_s}  "
                          f"({sd_s}, {z_s})\n",
                          "outlier")
            t.insert(tk.END, "\n")
        else:
            t.insert(tk.END,
                      "YOUR OUTLIERS: your current setup has no values >2σ from "
                      "the corpus median. Solid.\n\n",
                      "consensus")

        t.insert(tk.END, "STRONGEST CONSENSUS (everyone agrees):\n", "sub")
        for cat, param, cov in ranked[:10]:
            s = stats.get((cat, param), {})
            median = s.get("median", "?")
            info = SETUP_CATEGORIES.get(cat, {}).get(param)
            if info and isinstance(median, (int, float)):
                dec = param_decimals(info[2])
                med_s = f"{median:.{dec}f}"
            else:
                med_s = str(median)
            t.insert(tk.END,
                      f"  [{cat}] {param} = {med_s}  (CoV={cov:.3f}, n={s.get('n', 0)})\n",
                      "consensus")

        t.insert(tk.END, "\nMOST DIVERGENT (people disagree):\n", "sub")
        for cat, param, cov in reversed(ranked[-10:]):
            s = stats.get((cat, param), {})
            rng = f"{s.get('min', '?')} → {s.get('max', '?')}"
            t.insert(tk.END,
                      f"  [{cat}] {param}: range {rng}  "
                      f"(CoV={cov:.3f}, n={s.get('n', 0)})\n")

        t.insert(tk.END,
                  "\nHint: outliers aren't automatically bad — you may be faster "
                  "than the corpus. But they're worth examining.\n",
                  "dim")
        t.config(state=tk.DISABLED)
