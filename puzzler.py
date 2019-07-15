# Standard libs:
from libpuzzler import core


# Main:
blue = core.Piece([[0, 0, 0],
                   [1, 1, 0],
                   [1, 1, 1]])

orange = core.Piece([[1, 0, 0],
                     [1, 1, 1],
                     [0, 1, 0]])

purple = core.Piece([[0, 0, 0],
                     [1, 1, 0],
                     [1, 0, 0]])

green = core.Piece([[0, 1, 1],
                    [0, 0, 1],
                    [0, 1, 1]])

yellow = core.Piece([[1, 0, 0],
                     [1, 1, 1],
                     [1, 0, 0]])

red = core.Piece([[0, 1, 1],
                  [0, 0, 1],
                  [0, 0, 1]])

cube = core.Cube([orange, blue, purple, green, yellow, red])

print(cube)

for _ in range(100):
    cube.next()

    print("")
    print(cube._current_piece_index)
    print(cube._position_indices)
    print(cube._location_indices)
