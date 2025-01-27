import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np

class PlotCanvas:
    def __init__(self, parent):
        self.evo_fit = "Evolución del Fitness"
        self.gen = "Generación"
        self.best = "Mejor Fitness"
        self.versus = "Predicción vs Real"
        self.index = "Índice"
        self.val = "Valor"

        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        self.figure = Figure(figsize=(10, 4), dpi=100)
        self.fitness_ax = self.figure.add_subplot(121)
        self.prediction_ax = self.figure.add_subplot(122)
        
        self.fitness_ax.set_title(self.evo_fit)
        self.fitness_ax.set_xlabel(self.gen)
        self.fitness_ax.set_ylabel(self.best)
        
        self.prediction_ax.set_title(self.versus)
        self.prediction_ax.set_xlabel(self.index)
        self.prediction_ax.set_ylabel(self.val)
        
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        self.fitness_data = []
        self.prediction_data = None
        self.real_data = None
        
    def update_fitness_plot(self, fitness_value):
        self.fitness_data.append(fitness_value)
        self.fitness_ax.clear()
        self.fitness_ax.set_title(self.evo_fit)
        self.fitness_ax.set_xlabel(self.gen)
        self.fitness_ax.set_ylabel(self.best)
        self.fitness_ax.plot(self.fitness_data, 'b-')
        self.canvas.draw()
    
    def update_prediction_plot(self, y_pred, y_real):
        self.prediction_data = y_pred
        self.real_data = y_real
        
        self.prediction_ax.clear()
        self.prediction_ax.set_title(self.versus)
        self.prediction_ax.set_xlabel(self.index)
        self.prediction_ax.set_ylabel(self.val)
        
        indices = np.arange(len(y_real))
        self.prediction_ax.plot(indices, y_real, 'b-', label='Real')
        self.prediction_ax.plot(indices, y_pred, 'r--', label='Predicción')
        self.prediction_ax.legend()
        
        self.canvas.draw()
    
    def clear_plots(self):
        self.fitness_data = []
        self.prediction_data = None
        self.real_data = None
        
        self.fitness_ax.clear()
        self.prediction_ax.clear()
        
        self.fitness_ax.set_title(self.evo_fit)
        self.fitness_ax.set_xlabel(self.gen)
        self.fitness_ax.set_ylabel(self.best)
        
        self.prediction_ax.set_title(self.versus)
        self.prediction_ax.set_xlabel(self.index)
        self.prediction_ax.set_ylabel(self.val)
        
        self.canvas.draw()
    
    def get_frame(self):
        return self.frame