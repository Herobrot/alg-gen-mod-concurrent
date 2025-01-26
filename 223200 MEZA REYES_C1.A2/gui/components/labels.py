from tkinter import ttk

class ResultLabels:
    def __init__(self, parent):
        self.style = ttk.Style()
        self.style.configure("Header.TLabel", font=("Helvetica", 14, "bold"))

        self.labels = {}
        self._create_labels(parent)

    def _create_labels(self, parent):
        label_texts = {
            "best_x": "Mejor x: ---",
            "best_fx": "Mejor f(x): ---",
            "delta_system": "Delta del sistema: ---",
            "num_points": "Cantidad de puntos: ---",
            "num_bits": "Cantidad de bits: ---",
            "string_bits": "Cadena de bits: ---",
        }

        for i, (key, text) in enumerate(label_texts.items()):
            label = ttk.Label(parent, text=text, style="Header.TLabel", padding=(10, 5))
            label.grid(row=9 + i, column=0, columnspan=2, sticky="w", pady=8, padx=10)
            self.labels[key] = label

    def update_values(self, algorithm):
        updates = {
            "best_x": f"Mejor x: {algorithm.best_x:.6f}",
            "best_fx": f"Mejor f(x): {algorithm.best_fitness:.6f}",
            "delta_system": f"Delta del sistema: {algorithm.delta_system:.6f}",
            "num_points": f"Cantidad de puntos: {algorithm.n_points}",
            "num_bits": f"Cantidad de bits: {algorithm.bits}",
            "string_bits": f"Cadena de bits: {algorithm.best_solution.binary if algorithm.best_solution else '---'}",
        }

        for key, text in updates.items():
            self.labels[key].configure(text=text)
