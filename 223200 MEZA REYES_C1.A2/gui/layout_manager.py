from tkinter import ttk

class LayoutManager:
    def __init__(self, root):
        self.root = root
        self._configure_root()
        self._create_frames()

    def _configure_root(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

    def _create_frames(self):
        self.container_frame = ttk.Frame(self.root, padding="10")
        self.container_frame.grid(row=0, column=0, sticky="nsew")
        self.container_frame.grid_columnconfigure(0, weight=0)
        self.container_frame.grid_columnconfigure(1, weight=1)

        self.main_frame = ttk.Frame(self.container_frame, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
