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

    def all_positions_in_plane(self):
        """Recall our pose might be able to move up, down, left, right, up+right, up+left,
        down+right, down+left, but NOT up+down or left+right.
        """
        positions = [self.data]

        up = np.array_equal(self.data[0], np.zeros((3,)))
        down = np.array_equal(self.data[2], np.zeros((3,)))
        left = np.array_equal(self.data[:, 0], np.zeros((3,)))
        right = np.array_equal(self.data[:, 2], np.zeros((3,)))

        if up:
            u = np.zeros((3, 3), dtype=int)
            u[0, :] = self.data[1, :]
            u[1, :] = self.data[2, :]
            u[2, :] = self.data[0, :]  # zeros
            positions.append(u)
            if left:
                le = np.zeros((3, 3), dtype=int)
                le[:, 0] = u[:, 1]
                le[:, 1] = u[:, 2]
                le[:, 2] = u[:, 0]  # zeros
                positions.append(le)
            elif right:
                r = np.zeros((3, 3), dtype=int)
                r[:, 0] = u[:, 2]  # zeros
                r[:, 1] = u[:, 0]
                r[:, 2] = u[:, 1]
                positions.append(r)

        if down:
            d = np.zeros((3, 3), dtype=int)
            d[0, :] = self.data[2, :]  # zeros
            d[1, :] = self.data[0, :]
            d[2, :] = self.data[1, :]
            positions.append(d)
            if left:
                le = np.zeros((3, 3), dtype=int)
                le[:, 0] = d[:, 1]
                le[:, 1] = d[:, 2]
                le[:, 2] = d[:, 0]  # zeros
                positions.append(le)
            elif right:
                r = np.zeros((3, 3), dtype=int)
                r[:, 0] = d[:, 2]  # zeros
                r[:, 1] = d[:, 0]
                r[:, 2] = d[:, 1]
                positions.append(r)

        if left:
            d = np.zeros((3, 3), dtype=int)
            d[:, 0] = self.data[:, 1]
            d[:, 1] = self.data[:, 2]
            d[:, 2] = self.data[:, 0]  # zeros
            positions.append(d)

        if right:
            d = np.zeros((3, 3), dtype=int)
            d[:, 0] = self.data[:, 2]  # zeros
            d[:, 1] = self.data[:, 0]
            d[:, 2] = self.data[:, 1]
            positions.append(d)

        return positions

    # Special methods:
    def __str__(self):
        return str(self.data)

    def __eq__(self, other):
        return np.array_equal(reduced_form(self.data), reduced_form(other.data))


class Position:

    # Constructor:
    def __init__(self, data=None):
        if data is None:
            self.data = np.zeros((3, 3, 3))
        else:
            self.data = np.array(data)


class Piece:

    # Constructor:
    def __init__(self, initial=None):
        self._initial = Pose(initial)
        self._unique_poses = []
        self.positions_in_plane = []

    # Public methods:
    def all_poses(self):
        """Generator to return all possible poses."""

        for i_rot in range(4):
            yield self._initial.rotate(i_rot)

        for i_rot in range(4):
            yield self._initial.mirror().rotate(i_rot)

    def build_all_unique_poses(self):
        """Take only poses that are not equal to existing ones."""

        unique_poses = []
        for new_pose in self.all_poses():
            already_taken_into_account = False
            for old_pose in unique_poses:
                if new_pose == old_pose:
                    already_taken_into_account = True
                    break

            if not already_taken_into_account:
                unique_poses.append(new_pose)

        self._unique_poses = unique_poses

    def build_all_positions(self):

        positions = []
        for pose in self._unique_poses:
            for position in pose.all_positions_in_plane():
                positions.append(position)

        self.positions_in_plane = positions

