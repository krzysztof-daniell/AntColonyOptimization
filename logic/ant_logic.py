from math import sqrt
from random import choice, choices
from typing import List, Tuple

from logic.pheromone_logic import PheromoneLogic


class AntLogic:
    def __init__(self, pheromone: PheromoneLogic):
        self._pheromone_matrix = pheromone.pheromone
        self._home_position = pheromone.home_position
        self._food_position = pheromone.food_position
        self.position = choice([self._home_position, self._food_position])
        self._mode = 0 if self.position == self._home_position else 1
        self.tabu_list = []
        self.solution = []
        self.last_solution = []
        self.distance = 0
        self._possible_moves = [(-1, -1), (-1, 0), (-1, 1),
                                (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def calculate_distance(self, solution: List[Tuple[int, int]]):
        distance = 0

        for (x_1, y_1), (x_2, y_2) in zip(solution[:-1], solution[1:]):
            distance += sqrt(abs(x_1 - x_2) + abs(y_1 - y_2))

        return distance

    def choose_path(self, alpha: int):
        self.tabu_list.append(self.position)
        possible_paths = []
        probabilities = []

        for row, column in self._possible_moves:
            possible_path = (self.position[0] + row, self.position[1] + column)

            if possible_path[0] < 0 or possible_path[1] < 0:
                continue

            try:
                pheromone_value = self._pheromone_matrix[possible_path[0]
                                                         ][possible_path[1]]

                if pheromone_value < 0:
                    continue

                if possible_path in self.tabu_list:
                    probabilities.append(0)
                else:
                    probabilities.append(pheromone_value ** alpha)

                possible_paths.append(possible_path)
            except IndexError:
                continue

        if sum(probabilities) > 0:
            moves = []
            weights = []

            for i, probability in enumerate(probabilities):
                if probability > 0:
                    weights.append(probability)
                    moves.append(possible_paths[i])

            choosen_move = choices(population=moves, weights=weights)[0]
        else:
            choosen_move = choice(possible_paths)

        if choosen_move == self._home_position and self._mode == 1:
            self._mode = 0
            self.tabu_list.append(choosen_move)
            self.solution = self.tabu_list
            self.distance = self.calculate_distance(self.solution)
            self.tabu_list = []
        elif choosen_move == self._food_position and self._mode == 0:
            self._mode = 1
            self.tabu_list.append(choosen_move)
            self.solution = self.tabu_list
            self.distance = self.calculate_distance(self.solution)
            self.tabu_list = []

        self.position = choosen_move
