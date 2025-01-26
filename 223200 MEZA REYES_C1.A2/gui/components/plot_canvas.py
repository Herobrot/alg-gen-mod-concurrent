import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class PlotCanvas:
    def __init__(self, parent):
        self.fig, (self.ax, self.fitness_ax) = plt.subplots(2, 1, figsize=(8, 8))
        self.fig.tight_layout(pad=3.0)
        plt.subplots_adjust(hspace=0.4)

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.best_fitness_history = []
        self.worst_fitness_history = []
        self.avg_fitness_history = []

    def clear(self):
        self.ax.clear()
        self.fitness_ax.clear()
        self.canvas.draw()

    def update_plots(self, algorithm):
        self._update_population_plot(algorithm)
        self._update_fitness_plot(algorithm)
        self.canvas.draw()

    def _update_population_plot(self, algorithm):
        self.ax.clear()
        x_values = np.arange(
            algorithm.interval[0],
            algorithm.interval[1] + algorithm.delta,
            algorithm.delta,
        )
        y_values = [algorithm.fitness_function.calculate(x) for x in x_values]

        self.ax.plot(x_values, y_values, label="f(x)", color="blue")
        self.ax.set_title("Algoritmo Genético y f(x)")
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("f(x)")

        current_population = algorithm.get_decoded_population()
        for x, y in current_population:
            self.ax.plot(x, y, "kx")

        if algorithm.best_x is not None:
            self.ax.plot(algorithm.best_x, algorithm.best_fitness, "mx")
        if algorithm.worse_x is not None:
            self.ax.plot(algorithm.worse_x, algorithm.worse_fitness, "rx")

        self.ax.legend()

    def _update_fitness_plot(self, algorithm):
        current_best = max(algorithm.fitness)
        current_worst = min(algorithm.fitness)
        current_avg = sum(algorithm.fitness) / len(algorithm.fitness)

        self.best_fitness_history.append(current_best)
        self.worst_fitness_history.append(current_worst)
        self.avg_fitness_history.append(current_avg)

        self.fitness_ax.clear()
        self.fitness_ax.set_title("Evolución de la Aptitud")
        self.fitness_ax.set_xlabel("Iteraciones")
        self.fitness_ax.set_ylabel("Aptitud")

        iterations = range(1, len(self.best_fitness_history) + 1)
        self.fitness_ax.plot(
            iterations, self.best_fitness_history, label="Mejor", color="green"
        )
        self.fitness_ax.plot(
            iterations, self.worst_fitness_history, label="Peor", color="red"
        )
        self.fitness_ax.plot(
            iterations, self.avg_fitness_history, label="Promedio", color="blue"
        )
        self.fitness_ax.legend()
    def save_fx_plot(self, filepath):
        self.ax.figure.savefig(filepath, bbox_inches="tight")

