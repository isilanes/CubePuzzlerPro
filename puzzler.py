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

cube = core.Cube([blue, orange, purple, green, yellow, red])
print(cube)

print(cube.piece_fits(0, 0, 0))
