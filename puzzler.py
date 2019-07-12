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

purple.build_all_unique_poses()
p = purple._unique_poses[0]

print(p)

for pos in p.all_positions_in_plane():
    print("")
    print(pos)
