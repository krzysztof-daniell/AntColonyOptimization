from math import inf

from logic.ant_logic import AntLogic
from logic.pheromone_logic import PheromoneLogic


class ACOController:
    def __init__(self, width, height, drawn_pheromone_matrix,
                 pheromone: PheromoneLogic, ant: AntLogic):
        self.pheromone = pheromone(width, height, drawn_pheromone_matrix)
        self.ants = [ant(self.pheromone)
                     for _ in range(self.pheromone.fields_to_move)]
        self._auto_p = self.pheromone.fields_to_move / (width * height)
        self._auto_p = self._auto_p if self._auto_p < 0.8 else 0.8
        self.auto_evaporate_coefficent = 1 - self._auto_p
        self.auto_deposit_coefficent = self._auto_p
        self.best_solution = inf
        self.best_solution_path = []
        self.iterations = 0

    def choose_path_of_an_ant(self, ant: AntLogic, alpha: float):
        ant.choose_path(alpha)

    def evaporate_pheromone(self, evaporate_coefficient: float):
        self.pheromone.evaporate_pheromone(evaporate_coefficient)

    def deposit_pheromone(self, deposit_coefficent: float):
        for ant in self.ants:
            if ant.solution:
                q = deposit_coefficent / ant.distance

                for position in set(ant.solution):
                    self.pheromone.deposit_pheromone(position, q)

                if ant.distance < self.best_solution:
                    self.best_solution = ant.distance
                    self.best_solution_path = ant.solution

                ant.solution = []
                ant.distance = 0

        self.iterations += 1
