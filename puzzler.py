# Standard libs:
from libpuzzler import core


# Main:
pose = core.Pose([[0, 0, 0], [1, 1, 0], [1, 1, 1]])
piece = core.Piece(pose)

for pose in piece.generate_all_poses():
    print("")
    print(pose)
