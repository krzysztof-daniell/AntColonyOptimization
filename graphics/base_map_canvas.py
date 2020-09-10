import tkinter as tk


class BaseMapCanvas:
    def __init__(self, width: int, height: int, field_size: int,
                 master: tk.Tk):
        self.width = width
        self.height = height
        self.field_size = field_size
        self.canvas = tk.Canvas(master, width=width *
                                field_size, height=height * field_size)
        self.canvas.grid()
        self.canvas_matrix = self._create_matrix()

    def _create_matrix(self):
        return [[0 for _ in range(self.width)] for _ in range(self.height)]

    def update_canvas(self):
        self.canvas.update()
