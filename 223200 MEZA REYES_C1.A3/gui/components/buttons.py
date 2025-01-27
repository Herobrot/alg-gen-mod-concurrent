import tkinter as tk
from tkinter import ttk, filedialog
import os

class Buttons:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.action_button = "Action.TButton"
                
        style = ttk.Style()
        style.configure(self.action_button, padding=5)
                
        self.upload_btn = ttk.Button(
            self.frame,
            text="Cargar CSV",
            command=self.upload_file,
            style=self.action_button
        )
        self.upload_btn.pack(side=tk.LEFT, padx=5, pady=5)
                
        self.start_btn = ttk.Button(
            self.frame,
            text="Iniciar AG",
            command=self.start_algorithm,
            style=self.action_button
        )
        self.start_btn.pack(side=tk.LEFT, padx=5, pady=5)
                
        self.stop_btn = ttk.Button(
            self.frame,
            text="Detener",
            command=self.stop_algorithm,
            style=self.action_button,
            state='disabled'
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5, pady=5)
                
        self.file_label = ttk.Label(self.frame, text="Ningún archivo seleccionado")
        self.file_label.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.selected_file = None
        
    def upload_file(self):
        filetypes = [('CSV files', '*.csv')]
        filename = filedialog.askopenfilename(
            title='Seleccionar archivo CSV',
            filetypes=filetypes
        )
        
        if filename:
            self.selected_file = filename
            self.file_label.config(text=os.path.basename(filename))            
            if hasattr(self.parent, 'on_file_selected'):
                self.parent.on_file_selected(filename)
    
    def start_algorithm(self):
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.upload_btn.config(state='disabled')        
        if hasattr(self.parent, 'on_start_algorithm'):
            self.parent.on_start_algorithm()
    
    def stop_algorithm(self):
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.upload_btn.config(state='normal')        
        if hasattr(self.parent, 'on_stop_algorithm'):
            self.parent.on_stop_algorithm()
    
    def get_frame(self):
        return self.frame