"""Workflow Guide tab — step-by-step setup workflow documentation."""

import tkinter as tk
from tkinter import ttk

from rf2.knowledge import SETUP_WORKFLOW
from ui.scroll_helper import build_scrollable


class WorkflowMixin:
    def _build_workflow_tab(self):
        outer, frame = build_scrollable(self.notebook)

        ttk.Label(frame, text="Step-by-Step Setup Workflow",
                  font=("TkDefaultFont", 14, "bold")).pack(anchor="w", pady=(0, 5))
        ttk.Label(frame, text=(
            "Follow these steps in order to build a proper setup from the ground up. "
            "This is the correct order of operations used by professional race engineers. "
            "Don't skip steps — each one depends on the previous being reasonably dialed in."
        ), wraplength=800).pack(anchor="w", pady=(0, 15))

        for step_info in SETUP_WORKFLOW:
            step_frame = ttk.LabelFrame(
                frame,
                text=f"Step {step_info['step']}: {step_info['title']}",
                padding=10,
            )
            step_frame.pack(fill=tk.X, pady=5)

            ttk.Label(step_frame, text=step_info["description"], wraplength=800,
                      font=("TkDefaultFont", 9)).pack(anchor="w", fill=tk.X)

            check_frame = ttk.Frame(step_frame)
            check_frame.pack(fill=tk.X, pady=(8, 0))
            ttk.Label(check_frame, text="What to verify: ",
                      font=("TkDefaultFont", 9, "bold")).pack(side=tk.LEFT, anchor="n")
            ttk.Label(check_frame, text=step_info["what_to_check"],
                      wraplength=700, foreground="dark green",
                      font=("TkDefaultFont", 9)).pack(side=tk.LEFT, fill=tk.X, expand=True)

        return outer
