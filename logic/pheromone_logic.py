from typing import Tuple


class PheromoneLogic:
    def __init__(self, width: int, height: int, drawn_pheromone_matrix):
        self._width = width
        self._height = height
        self._drawn_pheromone_matrix = drawn_pheromone_matrix
        self.home_position = ()
        self.food_position = ()
        self.fields_to_move = 0
        self.pheromone = self._initialize_pheromone()

    def _initialize_pheromone(self):
        matrix = []

        for row in range(self._height):
            matrix.append([])

            for column in range(self._width):
                if self._drawn_pheromone_matrix[row][column] == -2:
                    self.home_position = (row, column)
                    self._drawn_pheromone_matrix[row][column] = 0
                elif self._drawn_pheromone_matrix[row][column] == -3:
                    self.food_position = (row, column)
                    self._drawn_pheromone_matrix[row][column] = 0

                if self._drawn_pheromone_matrix[row][column] == 0:
                    self.fields_to_move += 1

                matrix[row].append(self._drawn_pheromone_matrix[row][column])

        return matrix

    def evaporate_pheromone(self, evaporate_coefficient: float):
        for row in range(self._height):
            for column in range(self._width):
                if self.pheromone[row][column] > 0:
                    self.pheromone[row][column] *= evaporate_coefficient

    def deposit_pheromone(self, ant_position: Tuple[int, int],
                          deposit_coefficent: float):
        row, column = ant_position
        self.pheromone[row][column] += deposit_coefficent
