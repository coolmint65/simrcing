"""Problem Solver tab — diagnose handling issues and apply recommended fixes."""

import tkinter as tk
from tkinter import ttk, messagebox

from rf2.parameters import SETUP_CATEGORIES, param_decimals
from rf2.knowledge import HANDLING_PROBLEMS, get_problem_recommendations
from ui.scroll_helper import build_scrollable


class ProblemMixin:
    def _build_problem_solver_tab(self):
        outer, frame = build_scrollable(self.notebook)

        ttk.Label(frame, text="Handling Problem Solver",
                  font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(frame, text=(
            "Select the handling problem you're experiencing. The solver will diagnose "
            "the likely causes and recommend specific parameter changes to fix it. "
            "Apply changes one at a time and test 2-3 laps between each."
        ), wraplength=800).pack(anchor="w", pady=(0, 15))

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
                    decimals = param_decimals(step)
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
            decimals = param_decimals(step)
            new_val = round(new_val, decimals)
        else:
            new_val = int(round(new_val))

        self.setup[cat][param] = new_val
        self._apply_setup_to_ui()
        messagebox.showinfo("Applied",
                            f"Changed [{cat}] {param} from {current} to {new_val}.\n\n"
                            f"Reason: {explanation}")
        self._current_recommendations = self._current_recommendations[1:]
