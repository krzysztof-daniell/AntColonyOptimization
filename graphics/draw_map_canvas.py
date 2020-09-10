from graphics.base_map_canvas import BaseMapCanvas


class DrawMapCanvas(BaseMapCanvas):
    def __init__(self, width, height, field_size, master):
        super().__init__(width, height, field_size, master)
        self.canvas.bind('<Button-1>', self._draw_wall)
        self.canvas.bind('<B1-Motion>', self._draw_wall)
        self.canvas.bind('<Button-3>', self._erease_wall)
        self.canvas.bind('<B3-Motion>', self._erease_wall)
        self.canvas.bind('<Double-Button-1>', self._set_home_position)
        self.canvas.bind('<Double-Button-3>', self._set_food_position)
        self.pheromone_matrix = self._create_matrix()
        self.home_position = ()
        self.food_position = ()

    def _draw_wall(self, event) -> None:
        row = event.y // self.field_size
        column = event.x // self.field_size

        try:
            self.canvas.itemconfig(
                self.canvas_matrix[row][column], fill='black')
            self.pheromone_matrix[row][column] = -1
        except IndexError:
            pass

    def _erease_wall(self, event) -> None:
        row = event.y // self.field_size
        column = event.x // self.field_size

        try:
            self.canvas.itemconfig(
                self.canvas_matrix[row][column], fill='white')
            self.pheromone_matrix[row][column] = 0
        except IndexError:
            pass

    def _set_home_position(self, event) -> None:
        row = event.y // self.field_size
        column = event.x // self.field_size

        try:
            if self.home_position:
                self.canvas.itemconfig(
                    self.canvas_matrix[self.home_position[0]][self.home_position[1]], fill='white')
                self.pheromone_matrix[self.home_position[0]
                                      ][self.home_position[1]] = 0

            self.canvas.itemconfig(
                self.canvas_matrix[row][column], fill='blue')
            self.pheromone_matrix[row][column] = -2
            self.home_position = (row, column)

            if self.home_position == self.food_position:
                self.food_position == ()
        except IndexError:
            pass

    def _set_food_position(self, event) -> None:
        row = event.y // self.field_size
        column = event.x // self.field_size

        try:
            if self.food_position:
                self.canvas.itemconfig(
                    self.canvas_matrix[self.food_position[0]][self.food_position[1]], fill='white')
                self.pheromone_matrix[self.food_position[0]
                                      ][self.food_position[1]] = 0

            self.canvas.itemconfig(
                self.canvas_matrix[row][column], fill='green')
            self.pheromone_matrix[row][column] = -3
            self.food_position = (row, column)

            if self.food_position == self.home_position:
                self.home_position = ()
        except IndexError:
            pass

    def create_canvas(self) -> None:
        for row in range(self.height):
            for column in range(self.width):
                x_1 = column * self.field_size
                y_1 = row * self.field_size
                x_2 = x_1 + self.field_size
                y_2 = y_1 + self.field_size

                self.canvas_matrix[row][column] = self.canvas.create_rectangle(
                    (x_1, y_1, x_2, y_2), fill='white')
