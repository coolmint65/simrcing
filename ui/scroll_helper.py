"""Helper to build a scrollable frame inside a tab.

The tabs all need the same canvas + scrollbar + mousewheel-binding boilerplate;
this module centralizes it.
"""

import tkinter as tk
from tkinter import ttk


def build_scrollable(parent, padding=15):
    """Return (outer, inner) where outer goes into the notebook and inner is
    a padded ttk.Frame you can pack children into. Mouse wheel is bound for
    Windows/Mac (<MouseWheel>) and X11 (<Button-4>/<Button-5>)."""
    outer = ttk.Frame(parent)
    canvas = tk.Canvas(outer, highlightthickness=0)
    scrollbar = ttk.Scrollbar(outer, orient=tk.VERTICAL, command=canvas.yview)
    inner = ttk.Frame(canvas, padding=padding)

    inner.bind("<Configure>",
               lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.bind("<MouseWheel>",
                lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
    canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    return outer, inner
