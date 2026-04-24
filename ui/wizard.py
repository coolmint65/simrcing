"""Multi-choice wizard dialog for asking the user about unknown cars/tracks."""

import tkinter as tk
from tkinter import ttk


def run_wizard(root, title, questions):
    """Show a modal dialog with one group of radio buttons per question.

    questions: list of (key, question_text, [option_strings])
    Returns {key: selected_value} or None if cancelled.
    """
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.geometry("500x400")
    dialog.transient(root)
    dialog.grab_set()

    result = {}
    vars_map = {}

    frame = ttk.Frame(dialog, padding=15)
    frame.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frame, text=title, font=("TkDefaultFont", 12, "bold")).pack(
        anchor="w", pady=(0, 10))
    ttk.Label(frame, text=("I need a few details to build the right setup. "
                           "I'll remember your answers for next time."),
              wraplength=450, foreground="gray40").pack(anchor="w", pady=(0, 15))

    for key, question, options in questions:
        q_frame = ttk.LabelFrame(frame, text=question, padding=8)
        q_frame.pack(fill=tk.X, pady=5)
        var = tk.StringVar(value=options[0])
        vars_map[key] = (var, options)
        for opt in options:
            ttk.Radiobutton(q_frame, text=opt, variable=var, value=opt).pack(
                anchor="w", padx=5)

    cancelled = [False]

    def on_ok():
        for key, (var, _options) in vars_map.items():
            result[key] = var.get()
        dialog.destroy()

    def on_cancel():
        cancelled[0] = True
        dialog.destroy()

    btn_frame = ttk.Frame(frame)
    btn_frame.pack(fill=tk.X, pady=(15, 0))
    ttk.Button(btn_frame, text="OK — Generate Setup", command=on_ok).pack(
        side=tk.LEFT, padx=(0, 10))
    ttk.Button(btn_frame, text="Cancel", command=on_cancel).pack(side=tk.LEFT)

    dialog.wait_window()
    return None if cancelled[0] else result
