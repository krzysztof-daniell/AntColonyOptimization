import tkinter as tk
import tkinter.messagebox as messagebox
import webbrowser

from controller.aco_controller import ACOController
from graphics.display_map_canvas import DisplayMapCanvas
from graphics.draw_map_canvas import DrawMapCanvas
from logic.ant_logic import AntLogic
from logic.pheromone_logic import PheromoneLogic


class GraphicalUserInterface:
    def __init__(
        self,
        width: int,
        height: int,
        field_size: int,
        display_map: DisplayMapCanvas,
        draw_map: DrawMapCanvas,
        aco_controller: ACOController,
    ):
        self._width = width
        self._height = height
        self._field_size = field_size
        self._master = self._create_master()
        self._frame = tk.Frame(self._master)
        self._display_map_object = display_map
        self._display_map = None
        self._display_best_solution_object = display_map
        self._display_best_solution = None
        self._draw_map_object = draw_map
        self._draw_map = None
        self._drawn_map_matrix = None
        self.aco_controller_object = aco_controller
        self.aco_controller = None

    def _create_master(self) -> tk.Tk:
        master = tk.Tk()
        master.title('Ant Colony Optimization')
        master.protocol("WM_DELETE_WINDOW", self._on_closing)

        return master

    def _on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self._master.destroy()

    def _destroy_frame(self):
        self._frame.destroy()

    def web_callback(self, url: str) -> None:
        webbrowser.open_new(url)

    def run(self):
        self._destroy_frame()
        self._frame = tk.Frame(self._master)
        self._frame.grid()

        url = 'https://en.wikipedia.org/wiki/Ant_colony_optimization_algorithms'
        text = tk.Label(self._frame, text='Ant colony optimization algorithms',
                        fg='blue', cursor='hand2', justify=tk.LEFT)
        text.grid(row=0, padx=10)
        text.bind("<Button-1>", lambda e: self.web_callback(url))

        draw_button = tk.Button(
            self._frame, text='Draw map', command=self.draw_map)
        draw_button.grid(row=1, pady=5)

        self._master.mainloop()

    def _change_scale(self, variable):
        variable.set()

    def _create_aco_controller(self):
        self.aco_controller = self.aco_controller_object(
            self._width,
            self._height,
            self._drawn_map_matrix,
            PheromoneLogic,
            AntLogic,
        )

    def create_display_map(self):
        self._drawn_map_matrix = self._draw_map.pheromone_matrix

        self._create_aco_controller()
        self._destroy_frame()
        self._frame = tk.Frame(self._master)
        self._frame.grid()

        self._display_map = self._display_map_object(
            self._width,
            self._height,
            self._field_size,
            self._frame,
            self.aco_controller.pheromone,
        )
        self._display_map.create_canvas()
        self._display_map.canvas.grid(
            row=0, column=1, rowspan=20, columnspan=3)

        evaporate_label = tk.Label(self._frame, text='Evaporate coefficent:')
        evaporate_label.grid(row=0, column=0, sticky=tk.W)
        evaporate_coefficent = tk.DoubleVar(self._frame)
        evaporate_coefficent.set(self.aco_controller.auto_evaporate_coefficent)
        evaporate_slider = tk.Scale(
            self._frame,
            from_=0.001,
            to=0.999,
            orient=tk.HORIZONTAL,
            resolution=0.001,
            variable=evaporate_coefficent,
        )
        def evaporate_scale_changed(x): return evaporate_coefficent.set(x)
        evaporate_slider.config(command=evaporate_scale_changed)
        evaporate_slider.grid(row=1, column=0, sticky=tk.N)

        deposit_label = tk.Label(self._frame, text='Deposit coefficent:')
        deposit_label.grid(row=6, column=0, sticky=tk.W)
        deposit_coefficent = tk.DoubleVar(self._frame)
        deposit_coefficent.set(self.aco_controller.auto_deposit_coefficent)
        deposit_slider = tk.Scale(
            self._frame,
            from_=0.001,
            to=0.999,
            orient=tk.HORIZONTAL,
            resolution=0.001,
            variable=deposit_coefficent,
        )
        def deposit_scale_changed(x): return deposit_coefficent.set(x)
        deposit_slider.config(command=deposit_scale_changed)
        deposit_slider.grid(row=7, column=0, sticky=tk.N)

        alpha_label = tk.Label(self._frame, text='Alpha:')
        alpha_label.grid(row=12, column=0, sticky=tk.W)
        alpha = tk.IntVar(self._frame)
        alpha.set(5)
        alpha_slider = tk.Scale(
            self._frame,
            from_=1,
            to=5,
            orient=tk.HORIZONTAL,
            variable=alpha,
        )
        def alpha_scale_changed(x): return alpha.set(x)
        alpha_slider.config(command=alpha_scale_changed)
        alpha_slider.grid(row=13, column=0, sticky=tk.N)

        string_variable = tk.StringVar(self._frame)
        text_field = tk.Label(
            self._frame,
            textvariable=string_variable,
        )
        text_field.grid(row=20, column=0, columnspan=2, sticky=tk.W)

        finish_button = tk.Button(
            self._frame,
            text='Display best solution',
            command=self.display_best_solution,
        )
        finish_button.grid(row=20, column=3, sticky=tk.E, padx=10, pady=5)

        while True:
            self._aco_step(
                evaporate_coefficent,
                deposit_coefficent,
                alpha,
                string_variable,
            )

        self._master.mainloop()

    def _aco_step(self, evaporate_coefficent, deposit_coefficent, alpha,
                  string_variable):
        for ant in self.aco_controller.ants:
            self.aco_controller.choose_path_of_an_ant(ant, alpha.get())
            self.change_ant_position_on_display_map(ant)

        self.update_display_map()
        self.aco_controller.evaporate_pheromone(
            evaporate_coefficent.get())
        self.aco_controller.deposit_pheromone(
            deposit_coefficent.get())

        string_variable.set(
            f'Iterations: {self.aco_controller.iterations}')

    def display_best_solution(self):
        self._destroy_frame()
        self._frame = tk.Frame(self._master)
        self._frame.grid()

        best_solution = self.aco_controller.get_best_solution()

        if best_solution[0]:
            best_solution, best_solution_distance = best_solution
        else:
            best_solution_distance = 'not found'

        text_field = tk.Label(
            self._frame,
            text=f'Length of the best solution: {best_solution_distance}',
        )
        text_field.grid(row=0)

        self._display_best_solution = self._display_best_solution_object(
            self._width,
            self._height,
            self._field_size,
            self._frame,
            self.aco_controller.pheromone,
        )
        self._display_best_solution.create_canvas()
        self._display_best_solution.canvas.grid(row=1)
        self._display_best_solution.change_solution_color(
            best_solution)

        start_again_button = tk.Button(
            self._frame, text='Start again', command=self.run)
        start_again_button.grid(row=2, pady=5)

    def change_ant_position_on_display_map(self, ant: AntLogic):
        self._display_map.change_field_color(ant)

    def update_display_map(self):
        self._display_map.update_canvas()

    def call_display_map_loop(self):
        self._master.mainloop()

    def draw_map(self):
        self._destroy_frame()
        self._frame = tk.Frame(self._master)
        self._frame.grid()

        self._draw_map = self._draw_map_object(
            self._width, self._height, self._field_size, self._frame)
        self._draw_map.create_canvas()
        self._draw_map.canvas.grid(row=0, column=1, rowspan=5)

        place_home = tk.Label(
            self._frame,
            text='Place home:\n\n<Mouse-Left (double click)>',
            justify=tk.LEFT,
        )
        place_home.grid(row=0, column=0, sticky='NW')

        place_food = tk.Label(
            self._frame,
            text='Place food:\n\n<Mouse-Right (double click)>',
            justify=tk.LEFT,
        )
        place_food.grid(row=1, column=0, sticky='NW')

        draw_wall = tk.Label(
            self._frame,
            text='Draw wall:\n\n<Mouse-Right (click or press)>',
            justify=tk.LEFT,
        )
        draw_wall.grid(row=2, column=0, sticky='NW')

        erease_wall = tk.Label(
            self._frame,
            text='Erease:\n\n<Mouse-Left (click or press)>',
            justify=tk.LEFT,
        )
        erease_wall.grid(row=3, column=0, sticky='NW')

        draw_button = tk.Button(
            self._frame,
            text='Start ACO',
            command=self.create_display_map,
        )
        draw_button.grid(row=4, column=0, padx=10, pady=5)

        self._master.mainloop()

    @property
    def drawn_pheromone_matrix(self):
        return self._draw_map.pheromone_matrix
