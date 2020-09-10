# AntColonyOptimization

## Requirements
Python version: 3.8.5

Please use 'Draw map' option because 'Choose map' option is not implemented yet.

## Description
Implementation of the ACO algorithm for finding the shortest path between home and food on the map. You could draw your own map. GUI is implemented in tkinter and whole code is using only standard Python library. Next step of the project will be code refactoring and using NumPy for matrix operations and unit tests.

## Controls
* Mouse double right click - place home
* Mouse double left click - place food
* Mouse right click or press - draw walls
* Mouse right click or press - erease walls or home/food

## Tips
If ants don't find any path after 2500 iterations try increasing the pheromone coefficent and the deposit coefficent.
