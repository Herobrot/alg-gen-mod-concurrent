import tkinter as tk
from tkinter import ttk

class InputFields:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        
        vcmd = (self.frame.register(self.validate_float), '%P')
        
        self.fields = {}
        field_configs = {
            'population_size': {
                'label': 'Tamaño de Población:',
                'default': '100'
            },
            'crossover_rate': {
                'label': 'Tasa de Cruce (0-1):',
                'default': '0.8'
            },
            'mutation_rate': {
                'label': 'Tasa de Mutación (0-1):',
                'default': '0.1'
            },
            'min_interval_mutation_rate': {
                'label': 'Intervalo Mín. Mutación:',
                'default': '-0.5'
            },
            'max_interval_mutation_rate': {
                'label': 'Intervalo Máx. Mutación:',
                'default': '0.5'
            }
        }
        
        for row, (field_name, config) in enumerate(field_configs.items()):            
            field_frame = ttk.Frame(self.frame)
            field_frame.pack(fill=tk.X, padx=5, pady=2)
                        
            label = ttk.Label(field_frame, text=config['label'])
            label.pack(side=tk.LEFT)
                        
            entry = ttk.Entry(
                field_frame,
                validate='key',
                validatecommand=vcmd,
                width=10
            )
            entry.insert(0, config['default'])
            entry.pack(side=tk.RIGHT)
            
            self.fields[field_name] = entry
    
    def validate_float(self, value):
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
        
    def highlight_invalid_fields(self, invalid_fields):    
        for name, field in self.fields.items():
            if name in invalid_fields:
                field.config(background='red')
            else:
                field.config(background='white')
    
    def get_frame(self):
        return self.frame
    
    def get_values(self):
        return {
            name: float(field.get())
            for name, field in self.fields.items()
        }
    
    def set_values(self, values_dict):
        for name, value in values_dict.items():
            if name in self.fields:
                self.fields[name].delete(0, tk.END)
                self.fields[name].insert(0, str(value))
    
    def get_frame(self):
        return self.frame