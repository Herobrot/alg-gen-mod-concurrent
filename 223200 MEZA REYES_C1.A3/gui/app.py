import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import threading
import logging
from gui.components.buttons import Buttons # type: ignore
from gui.components.input_fields import InputFields # type: ignore
from gui.components.plot_canvas import PlotCanvas # type: ignore
from utils.validation import validate_inputs, format_validation_error # type: ignore
from algorithm.dataset_genetic_algorithm import GeneticAlgorithm # type: ignore

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info("Inicializando aplicación")
        
        try:
            self.setup_window()
            self.initialize_components()
            self.setup_variables()
            self.connect_events()
            self.logger.info("Aplicación inicializada correctamente")
        except Exception as e:
            self.logger.error(f"Error durante la inicialización: {str(e)}")
            raise

    def setup_window(self):
        self.title("Algoritmo Genético - Regresión Lineal")
        self.geometry("1200x600")
        self.create_frames()

    def create_frames(self):
        self.config_frame = ttk.Frame(self)
        self.config_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def initialize_components(self):
        self.input_fields = InputFields(self.config_frame)
        self.input_fields.get_frame().pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.buttons = Buttons(self.config_frame)
        self.buttons.get_frame().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

        self.plot_canvas = PlotCanvas(self.plot_frame)
        self.plot_canvas.get_frame().pack(fill=tk.BOTH, expand=True)

    def setup_variables(self):
        self.dataset = None
        self.algorithm = None
        self.running = False
        self.current_thread = None

    def connect_events(self):
        self.buttons.parent = self
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_dataset(self, filename):
        try:
            data = pd.read_csv(filename, delimiter=';')
            data = data.to_numpy()
            self.dataset = data[:, 1:]
            messagebox.showinfo("Éxito", "Dataset cargado correctamente")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
            return False

    def validate_parameters(self):
        try:
            params = self.input_fields.get_values()
            is_valid, invalid_fields = validate_inputs(params)
            
            if not is_valid:
                error_message = format_validation_error(invalid_fields)
                messagebox.showerror("Error de validación", error_message)
                self.input_fields.highlight_invalid_fields(invalid_fields)
                return None
            
            self.input_fields.highlight_invalid_fields([])
            return params
        except ValueError as _:
            messagebox.showerror("Error", "Por favor, verifica que todos los campos contengan números válidos.")
            return None

    def initialize_algorithm(self, params):
        return GeneticAlgorithm(
            dataset=self.dataset,
            iterations=100,
            population_size=params['population_size'],
            crossover_rate=params['crossover_rate'],
            mutation_rate=params['mutation_rate'],
            min_interval_mutation_rate=params['min_interval_mutation_rate'],
            max_interval_mutation_rate=params['max_interval_mutation_rate'] 
        )


    def update_plots(self, generation, best_fitness, y_pred, y_real):
        self.plot_canvas.update_fitness_plot(best_fitness)
        self.plot_canvas.update_prediction_plot(y_pred, y_real)

    def algorithm_worker(self):
        try:
            gen = 0
            while self.running and gen < self.algorithm.iterations:
                self.algorithm.evolve_population()
                best_solution = self.algorithm.best_solutions[-1]
                
                y_pred = np.dot(self.algorithm.X, best_solution[1][1:]) + best_solution[1][0]
                
                self.after(1, self.update_plots, gen, best_solution[0], y_pred, self.algorithm.yd)
                gen += 1
                
            if self.running:
                self.after(1, self.on_algorithm_complete)
                
        except Exception as e:
            self.after(1, lambda: messagebox.showerror("Error", f"Error en la ejecución: {str(e)}"))
            self.running = False

    def on_file_selected(self, filename):
        if self.load_dataset(filename):
            self.plot_canvas.clear_plots()

    def on_start_algorithm(self):
        if self.dataset is None:
            messagebox.showerror("Error", "Por favor, carga un dataset primero")
            return

        params = self.validate_parameters()
        if params is None:
            return

        self.algorithm = self.initialize_algorithm(params)
        self.running = True
        self.current_thread = threading.Thread(target=self.algorithm_worker, daemon=True)
        self.current_thread.start()

    def on_stop_algorithm(self):
        self.running = False
        if self.current_thread and self.current_thread.is_alive():
            self.current_thread.join(timeout=1.0)

    def on_algorithm_complete(self):
        messagebox.showinfo("Completado", "El algoritmo ha finalizado su ejecución")
        self.buttons.start_btn.config(state='normal')
        self.buttons.stop_btn.config(state='disabled')

    def on_closing(self):        
        if messagebox.askokcancel("Salir", "¿Deseas cerrar la aplicación?"):
            self.logger.info("Cerrando aplicación")
            self.on_stop_algorithm()
            self.quit()

    def show_error(self, message):        
        self.logger.error(message)
        messagebox.showerror("Error", message)

    def show_info(self, message):        
        self.logger.info(message)
        messagebox.showinfo("Información", message)

    def mainloop(self, n=0):        
        self.logger.info("Iniciando mainloop")
        try:
            super().mainloop()
        except Exception as e:
            self.logger.error(f"Error en mainloop: {str(e)}")
            raise
        finally:
            self.logger.info("Finalizando mainloop")

if __name__ == "__main__":
    app = App()
    app.mainloop()