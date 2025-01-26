from tkinter import ttk

class StartButton:
    def __init__(self, parent, command):
        self.style = ttk.Style()
        self.style.configure("Large.TButton", font=("Helvetica", 12))

        self.button = ttk.Button(
            parent, text="Iniciar", command=command, style="Large.TButton"
        )
        self.button.grid(row=9, column=0, columnspan=2, pady=25, padx=10, sticky="ew")

    def enable(self):
        self.button.config(state="normal")

    def disable(self):
        self.button.config(state="disabled")
