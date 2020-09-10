from controller.aco_controller import ACOController
from graphics.display_map_canvas import DisplayMapCanvas
from graphics.draw_map_canvas import DrawMapCanvas
from gui.gui import GraphicalUserInterface

if __name__ == "__main__":
    width = 20
    height = 20
    field_size = 20

    gui = GraphicalUserInterface(
        width,
        height,
        field_size,
        DisplayMapCanvas,
        DrawMapCanvas,
        ACOController,
    )
    gui.run()
