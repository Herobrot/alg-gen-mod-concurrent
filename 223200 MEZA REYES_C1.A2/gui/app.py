# src/gui/app.py
from algorithm.genetic_algorithm import GeneticAlgorithm # type: ignore
from utils.threading_utils import run_in_thread # type: ignore
from utils.validation import validate_inputs # type: ignore
from utils.video_generator import create_video_from_frames # type: ignore
from gui.components.input_fields import InputFields # type: ignore
from gui.components.plot_canvas import PlotCanvas # type: ignore
from gui.components.labels import ResultLabels # type: ignore
from gui.components.buttons import StartButton # type: ignore
from gui.layout_manager import LayoutManager # type: ignore
import tkinter as tk
from tkinter import ttk, messagebox
import os


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_components()

    def setup_window(self):
        self.root.title("Algoritmo Genetico Concurrente - 223200")
        self.root.geometry("1200x900")
        self.layout_manager = LayoutManager(self.root)

    def setup_components(self):
        self.input_fields = InputFields(self.layout_manager.main_frame)
        self.plot_canvas = PlotCanvas(self.layout_manager.container_frame)
        self.result_labels = ResultLabels(self.layout_manager.main_frame)
        self.start_button = StartButton(
            self.layout_manager.main_frame, self.start_algorithm
        )

    def start_algorithm(self):
        try:
            params = self.input_fields.get_values()
            if not validate_inputs(params):
                raise ValueError("Invalid input values")

            self.start_button.disable()
            self.plot_canvas.clear()

            algorithm = GeneticAlgorithm(**params)
            algorithm.initialize_population()

            run_in_thread(self.evolution_process, algorithm, params["iteration"])

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.start_button.enable()

    def evolution_process(self, algorithm, iterations):
        iterations = int(iterations)
        temp_dir = "temp_frames"
        os.makedirs(temp_dir, exist_ok=True)

        try:
            for i in range(iterations):
                algorithm.evolve(i)
                self.update_gui(algorithm)

                frame_path = os.path.join(temp_dir, f"frame_{i:04d}.png")
                self.plot_canvas.fig.savefig(frame_path)

            output_file = "videos/evolution_video.mp4"
            create_video_from_frames(temp_dir, output_file)
            messagebox.showinfo("Video Generado", f"El video se ha guardado como {output_file}")

        finally:
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            os.rmdir(temp_dir)


    def update_gui(self, algorithm):
        self.plot_canvas.update_plots(algorithm)
        self.result_labels.update_values(algorithm)

    def run(self):
        self.root.mainloop()
