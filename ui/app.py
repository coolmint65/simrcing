"""Main application — composes all tab mixins into RF2SetupApp."""

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from rf2.parameters import SETUP_CATEGORIES, get_default_setup
from rf2 import svm as svm_io
from rf2 import telemetry

from ui.advisor_tab import AdvisorMixin
from ui.problem_tab import ProblemMixin
from ui.workflow_tab import WorkflowMixin
from ui.editor_tab import EditorMixin
from ui.journal_tab import JournalMixin
from ui.calc_tab import CalcMixin


_PREFS_DIR = os.path.join(os.path.expanduser("~"), ".rf2_setup")
_PREFS_FILE = os.path.join(_PREFS_DIR, "prefs.json")


def _load_prefs():
    try:
        with open(_PREFS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _save_prefs(prefs):
    os.makedirs(_PREFS_DIR, exist_ok=True)
    with open(_PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=2)


class RF2SetupApp(AdvisorMixin, ProblemMixin, WorkflowMixin, EditorMixin,
                  JournalMixin, CalcMixin):
    def __init__(self, root):
        self.root = root
        self.root.title("rFactor 2 Car Setup Program")
        self.root.geometry("960x720")
        self.root.minsize(800, 600)

        self.setup = get_default_setup()
        self.compare_setup = None
        self.compare_name = ""
        self.widgets = {}

        self._prefs = _load_prefs()
        self.unit_system = tk.StringVar(value=self._prefs.get("unit_system", "metric"))

        self._selected_car_data = None
        self._selected_car_name = None
        self._selected_track_data = None
        self._selected_track_name = None

        self._build_menu()
        self._build_ui()

    # ---- Menu ---------------------------------------------------------------

    def _build_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Setup", command=self.new_setup)
        file_menu.add_command(label="Open Setup...", command=self.load_setup)
        file_menu.add_command(label="Save Setup...", command=self.save_setup)
        file_menu.add_separator()
        file_menu.add_command(label="Import rF2 .svm...", command=self.import_svm)
        file_menu.add_command(label="Export rF2 .svm...", command=self.export_svm)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        compare_menu = tk.Menu(menubar, tearoff=0)
        compare_menu.add_command(label="Load Setup to Compare...", command=self.load_compare)
        compare_menu.add_command(label="Clear Comparison", command=self.clear_compare)
        menubar.add_cascade(label="Compare", menu=compare_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_radiobutton(label="Metric (mm, kPa, N/mm, L)",
                                   variable=self.unit_system, value="metric",
                                   command=self._on_unit_system_change)
        view_menu.add_radiobutton(label="Imperial (in, psi, lbf/in, gal)",
                                   variable=self.unit_system, value="imperial",
                                   command=self._on_unit_system_change)
        menubar.add_cascade(label="Units", menu=view_menu)

        tools_menu = tk.Menu(menubar, tearoff=0)
        tools_menu.add_command(label="Check rF2 Telemetry Connection",
                                command=self._check_telemetry)
        menubar.add_cascade(label="Tools", menu=tools_menu)

    # ---- Telemetry ----------------------------------------------------------

    def _check_telemetry(self):
        try:
            with telemetry.connect() as t:
                temps = t.tire_temps()
        except telemetry.TelemetryUnavailable as e:
            messagebox.showwarning("Telemetry", str(e))
            return
        if temps is None:
            messagebox.showinfo("Telemetry",
                                 "Connected, but could not parse the buffer. "
                                 "The plugin version might not match what this app expects. "
                                 "Tire temp readings will be unavailable.")
            return
        msg = "Live tire temps:\n" + "\n".join(f"  {k}: {v:.1f} °C" for k, v in temps.items())
        messagebox.showinfo("Telemetry", msg)

    # ---- Unit toggle --------------------------------------------------------

    def _on_unit_system_change(self):
        self._prefs["unit_system"] = self.unit_system.get()
        _save_prefs(self._prefs)
        messagebox.showinfo("Units",
                            f"Unit preference saved as {self.unit_system.get()}. "
                            "Sliders remain metric (rF2 native); imperial is used "
                            "in tooltips and calculator labels only.")

    # ---- UI layout ----------------------------------------------------------

    def _build_ui(self):
        info_frame = ttk.Frame(self.root, padding=5)
        info_frame.pack(fill=tk.X)
        self.status_var = tk.StringVar(value="rFactor 2 Setup Editor — New Setup")
        ttk.Label(info_frame, textvariable=self.status_var,
                  font=("TkDefaultFont", 11, "bold")).pack(side=tk.LEFT)

        self.compare_var = tk.StringVar(value="")
        ttk.Label(info_frame, textvariable=self.compare_var,
                  foreground="blue").pack(side=tk.RIGHT)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.notebook.add(self._build_advisor_tab(), text=">> Advisor")
        self.notebook.add(self._build_problem_solver_tab(), text=">> Problem Solver")
        self.notebook.add(self._build_workflow_tab(), text=">> Workflow Guide")
        self.notebook.add(self._build_calc_tab(), text=">> Calculators")
        self.notebook.add(self._build_journal_tab(), text=">> Journal")

        sep = ttk.Frame(self.notebook)
        self.notebook.add(sep, text="---", state="disabled")

        for cat, params in SETUP_CATEGORIES.items():
            self.notebook.add(self._build_category_tab(cat, params), text=cat)

    # ---- File operations ----------------------------------------------------

    def new_setup(self):
        self.setup = get_default_setup()
        self._apply_setup_to_ui()
        self.status_var.set("rFactor 2 Setup Editor — New Setup")

    def save_setup(self):
        path = filedialog.asksaveasfilename(
            title="Save Setup",
            defaultextension=".json",
            filetypes=[("JSON Setup Files", "*.json"), ("All Files", "*.*")],
            initialdir=self._setups_dir())
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.setup, f, indent=2)
        basename = os.path.basename(path)
        self.status_var.set(f"rFactor 2 Setup Editor — {basename}")
        self.journal_log_event("save", path=path)
        messagebox.showinfo("Saved", f"Setup saved to:\n{path}")

    def load_setup(self):
        path = filedialog.askopenfilename(
            title="Open Setup",
            filetypes=[("JSON Setup Files", "*.json"), ("All Files", "*.*")],
            initialdir=self._setups_dir())
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", f"Failed to load setup:\n{e}")
            return
        self._merge_into_setup(data)
        self._apply_setup_to_ui()
        basename = os.path.basename(path)
        self.status_var.set(f"rFactor 2 Setup Editor — {basename}")
        self.journal_log_event("load", path=path)

    def import_svm(self):
        path = filedialog.askopenfilename(
            title="Import rF2 .svm",
            filetypes=[("rF2 Setup Files", "*.svm"), ("All Files", "*.*")])
        if not path:
            return
        try:
            partial, unmapped = svm_io.read_svm(path)
        except OSError as e:
            messagebox.showerror("Error", f"Failed to read .svm:\n{e}")
            return
        self._merge_into_setup(partial)
        self._apply_setup_to_ui()
        self.status_var.set(f"rFactor 2 Setup Editor — {os.path.basename(path)}")
        self.journal_log_event("import_svm", path=path)
        note = ""
        if unmapped:
            note = (f"\n\n{len(unmapped)} key(s) in the .svm were not recognized and "
                    "kept at defaults. Unmapped sample: "
                    + ", ".join(f"{s}/{k}" for s, k in unmapped[:5])
                    + ("..." if len(unmapped) > 5 else ""))
        messagebox.showinfo("Imported .svm",
                             f"Loaded {sum(len(v) for v in partial.values())} "
                             f"parameters from {os.path.basename(path)}.{note}")

    def export_svm(self):
        path = filedialog.asksaveasfilename(
            title="Export to rF2 .svm",
            defaultextension=".svm",
            filetypes=[("rF2 Setup Files", "*.svm"), ("All Files", "*.*")])
        if not path:
            return
        try:
            omitted = svm_io.write_svm(path, self.setup)
        except OSError as e:
            messagebox.showerror("Error", f"Failed to write .svm:\n{e}")
            return
        self.journal_log_event("export_svm", path=path)
        msg = f"Exported {os.path.basename(path)}."
        if omitted:
            msg += f"\n\n{len(omitted)} parameter(s) had no .svm mapping and were omitted."
        messagebox.showinfo("Exported .svm", msg)

    # ---- Compare ------------------------------------------------------------

    def load_compare(self):
        path = filedialog.askopenfilename(
            title="Load Setup to Compare",
            filetypes=[("JSON Setup Files", "*.json"), ("All Files", "*.*")],
            initialdir=self._setups_dir())
        if not path:
            return
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            messagebox.showerror("Error", f"Failed to load compare setup:\n{e}")
            return
        merged = get_default_setup()
        for cat in merged:
            if cat in data:
                for name in merged[cat]:
                    if name in data[cat]:
                        merged[cat][name] = data[cat][name]
        self.compare_setup = merged
        self.compare_name = os.path.basename(path)
        self.compare_var.set(f"Comparing with: {self.compare_name}")
        self._update_all_compare_labels()

    def clear_compare(self):
        self.compare_setup = None
        self.compare_name = ""
        self.compare_var.set("")
        self._update_all_compare_labels()

    # ---- Internal helpers ---------------------------------------------------

    def _setups_dir(self):
        return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "setups")

    def _merge_into_setup(self, partial):
        """Merge a partial dict into self.setup, keeping defaults for missing keys."""
        if not self.setup:
            self.setup = get_default_setup()
        for cat, params in partial.items():
            if cat not in self.setup:
                continue
            for name, val in params.items():
                if name in self.setup[cat]:
                    self.setup[cat][name] = val


def main():
    root = tk.Tk()

    style = ttk.Style()
    available_themes = style.theme_names()
    for preferred in ("clam", "alt", "default"):
        if preferred in available_themes:
            style.theme_use(preferred)
            break

    app = RF2SetupApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
