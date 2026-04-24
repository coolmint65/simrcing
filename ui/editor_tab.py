"""Setup parameter editor tabs — one tab per category with sliders for each parameter."""

import tkinter as tk
from tkinter import ttk

from rf2.parameters import SETUP_CATEGORIES, param_decimals


class EditorMixin:
    def _build_category_tab(self, cat, params):
        outer = ttk.Frame(self.notebook)
        canvas = tk.Canvas(outer, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient=tk.VERTICAL, command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind("<Configure>",
                          lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.bind("<MouseWheel>",
                    lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.widgets[cat] = {}
        for row, (name, meta) in enumerate(params.items()):
            vmin, vmax, step, default, unit, tip = meta
            self._build_param_row(scroll_frame, cat, name, vmin, vmax, step,
                                  default, unit, tip, row)

        return outer

    def _build_param_row(self, parent, cat, name, vmin, vmax, step, default, unit, tip, row):
        is_float = isinstance(step, float)

        frame = ttk.LabelFrame(parent, text=f"{name} ({unit})", padding=(10, 5))
        frame.grid(row=row, column=0, sticky="ew", padx=10, pady=4)
        parent.columnconfigure(0, weight=1)

        var = tk.DoubleVar(value=default) if is_float else tk.IntVar(value=default)

        slider_frame = ttk.Frame(frame)
        slider_frame.pack(fill=tk.X)

        ttk.Label(slider_frame, text=str(vmin), width=6, anchor="e").pack(side=tk.LEFT)

        scale = ttk.Scale(slider_frame, from_=vmin, to=vmax, variable=var,
                          orient=tk.HORIZONTAL,
                          command=lambda val, c=cat, n=name, s=step, f=is_float:
                              self._on_scale_change(val, c, n, s, f))
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        ttk.Label(slider_frame, text=str(vmax), width=6).pack(side=tk.LEFT)

        fmt = f"{{:.{param_decimals(step)}f}}" if is_float else "{}"
        value_label = ttk.Label(slider_frame, text=fmt.format(default),
                                width=8, anchor="center",
                                font=("TkDefaultFont", 10, "bold"))
        value_label.pack(side=tk.LEFT, padx=(5, 0))

        compare_label = ttk.Label(slider_frame, text="", width=12, foreground="red")
        compare_label.pack(side=tk.LEFT, padx=(5, 0))

        tip_label = ttk.Label(frame, text=tip, wraplength=700,
                              foreground="gray40", font=("TkDefaultFont", 8))
        tip_label.pack(fill=tk.X, pady=(2, 0))

        self.widgets[cat][name] = (var, scale, value_label, compare_label,
                                   step, is_float, vmin, vmax)

    def _on_scale_change(self, val, cat, name, step, is_float):
        raw = float(val)
        info = self.widgets[cat][name]
        var, _scale, value_label, _compare_label, _st, _fl, vmin, vmax = info

        snapped = round(round((raw - vmin) / step) * step + vmin, 10)
        snapped = max(vmin, min(vmax, snapped))

        if is_float:
            decimals = param_decimals(step)
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
                    decimals = param_decimals(info[4])
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
            for name, widget_tuple in params.items():
                var, _scale, value_label, _compare_label, step, is_float, _vmin, _vmax = widget_tuple
                val = self.setup.get(cat, {}).get(name, var.get())
                var.set(val)
                if is_float:
                    decimals = param_decimals(step)
                    value_label.config(text=f"{val:.{decimals}f}")
                else:
                    value_label.config(text=str(val))
        self._update_all_compare_labels()
