from typing import List, Tuple

from graphics.base_map_canvas import BaseMapCanvas
from logic.ant_logic import AntLogic
from logic.pheromone_logic import PheromoneLogic


class DisplayMapCanvas(BaseMapCanvas):
    def __init__(self, width, height, field_size, master,
                 pheromone: PheromoneLogic):
        super().__init__(width, height, field_size, master)
        self._pheromone_matrix = pheromone.pheromone
        self._home_position = pheromone.home_position
        self._food_position = pheromone.food_position

    def create_canvas(self) -> None:
        for row in range(self.height):
            for column in range(self.width):
                x_1 = column * self.field_size
                y_1 = row * self.field_size
                x_2 = x_1 + self.field_size
                y_2 = y_1 + self.field_size

                if self._home_position == (row, column):
                    color = 'blue'
                elif self._food_position == (row, column):
                    color = 'green'
                elif self._pheromone_matrix[row][column] >= 0:
                    color = 'white'
                else:
                    color = 'black'

                self.canvas_matrix[row][column] = self.canvas.create_rectangle(
                    (x_1, y_1, x_2, y_2), fill=color)

    def change_field_color(self, ant: AntLogic) -> None:
        current_position = ant.position
        previous_position = ant.tabu_list[-1] if ant.tabu_list else 0
        home_food_tabu = [self._home_position, self. _food_position]

        if current_position not in home_food_tabu:
            row, column = current_position
            self.canvas.itemconfig(self.canvas_matrix[row][column], fill='red')

        if previous_position and previous_position not in home_food_tabu:
            row, column = previous_position
            self.canvas.itemconfig(
                self.canvas_matrix[row][column], fill='white')

    def change_solution_color(self, best_solution: List[Tuple[int, int]]):
        home_food_tabu = [self._home_position, self. _food_position]

        for position in best_solution:
            if position not in home_food_tabu:
                row, column = position
                self.canvas.itemconfig(
                    self.canvas_matrix[row][column], fill='red')
                self.canvas.itemconfig(
                    self.canvas_matrix[row][column], fill='red')
