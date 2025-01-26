# src/gui/components/input_fields.py
from tkinter import ttk


class InputFields:
    def __init__(self, parent):
        self.fields = {
            "delta": ("Delta", "0.005"),
            "min_val": ("Intervalo Min", "-200"),
            "max_val": ("Intervalo Max", "500"),
            "iteration": ("Iteraciones", "100"),
            "pop_max": ("Población Max", "150"),
            "pop_min": ("Población Min", "20"),
            "crossover_rate": ("Crossover Rate", "0.5"),
            "mutation_rate": ("Mutation Rate", "0.5"),
            "bit_mutation_rate": ("Probabilidad por bit", "0.5"),
        }
        self.entries = {}
        self._create_fields(parent)

    def _create_fields(self, parent):
        for i, (key, (label, default)) in enumerate(self.fields.items()):
            ttk.Label(parent, text=label).grid(row=i, column=0, pady=5, padx=10)
            entry = ttk.Entry(parent, width=25)
            entry.insert(0, default)
            entry.grid(row=i, column=1, pady=5, padx=10)
            self.entries[key] = entry

    def get_values(self):
        return {key: float(self.entries[key].get()) for key in self.fields.keys()}
