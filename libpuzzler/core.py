# Standard libs:
import numpy as np


# Functions:
def reduced_form(np_array):
    """Return input array with all-zero columns and rows removed."""

    i_min, i_max = 0, 3
    j_min, j_max = 0, 3

    if np.array_equal(np_array[0], np.zeros((3,))):
        i_min = 1

    if np.array_equal(np_array[2], np.zeros((3,))):
        i_max = 2

    if np.array_equal(np_array[:, 0], np.zeros((3,))):
        j_min = 1

    if np.array_equal(np_array[:, 2], np.zeros((3,))):
        j_max = 2

    return np_array[i_min:i_max, j_min:j_max]


# Classes:
class Pose:

    # Constructor:
    def __init__(self, data=None):
        if data is None:
            self.data = np.zeros((3, 3))
        else:
            self.data = np.array(data)

    # Public properties:
    def rotate(self, k=1):
        """Return the Pose, but rotated k*90 degrees CW."""

        return Pose(data=np.rot90(self.data, k=k, axes=(1, 0)))

    def mirror(self):
        """Return mirror image of Pose, wrt plane Pose is contained in.
        ...    xxx
        xx. -> xx.
        xxx    ...
        """
        return Pose(np.array([self.data[2, :], self.data[1, :], self.data[0, :]]))

    # Special methods:
    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        return np.array_equal(reduced_form(self.data), reduced_form(other.data))


class Piece:

    # Constructor:
    def __init__(self, initial=None):
        self._initial = Pose(initial)
        self.poses = []

    # Public methods:
    def generate_all_poses(self):
        """Generator to return all possible poses."""

        for i_rot in range(4):
            yield self._initial.rotate(i_rot)

        for i_rot in range(4):
            yield self._initial.mirror().rotate(i_rot)

    def generate_all_unique_poses(self):
        """Take only poses that are not equal to existing ones."""

        unique_poses = []
        for new_pose in self.generate_all_poses():
            already_taken_into_account = False
            for old_pose in unique_poses:
                if new_pose == old_pose:
                    already_taken_into_account = True
                    break

            if not already_taken_into_account:
                unique_poses.append(new_pose)

        self.poses = unique_poses

