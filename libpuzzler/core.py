# Standard libs:
import numpy as np


# Classes:
class Pose:

    # Constructor:
    def __init__(self, data=None):
        if data is None:
            self._data = np.zeros((3, 3))
        else:
            self._data = np.array(data)

    # Public properties:
    def rotate(self, k=1):
        """Return the Pose, but rotated k*90 degrees CW."""

        return Pose(data=np.rot90(self._data, k=k, axes=(1, 0)))

    def mirror(self):
        """Return mirror image of Pose, wrt plane Pose is contained in.
        ...    xxx
        xx. -> xx.
        xxx    ...
        """
        return Pose(np.array([self._data[2, :], self._data[1, :], self._data[0, :]]))

    # Special methods:
    def __str__(self):
        return str(self._data)


class Piece:

    # Constructor:
    def __init__(self, pose):
        self._initial = pose
        self._poses = [pose]

    # Public methods:
    def generate_all_poses(self):
        for i_rot in range(4):
            yield self._initial.rotate(i_rot)

        for i_rot in range(4):
            yield self._initial.mirror().rotate(i_rot)

