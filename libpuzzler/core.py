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
        
        self._all_positions_in_plane = None
        self._current_location_index = 0  # which location we are currently in
        self._current_position_index = 0  # which position we are currently in

    # Public methods:
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

    # Public properties:
    @property
    def all_positions_in_plane(self):
        """Recall our pose might be able to move up, down, left, right, up+right, up+left,
        down+right, down+left, but NOT up+down or left+right.
        """
        if self._all_positions_in_plane is None:
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

            self._all_positions_in_plane = positions
        
        return self._all_positions_in_plane
    
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
        self._unique_poses = None
        self._positions_in_plane = None

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

        return unique_poses

    def build_all_positions(self):

        positions = []
        for pose in self.unique_poses:
            for position in pose.all_positions_in_plane:
                positions.append(position)

        return positions
    
    def put_piece(self):
        pass
    
    # Public properties:
    @property
    def unique_poses(self):
        if self._unique_poses is None:
            self._unique_poses = self.build_all_unique_poses()
        
        return self._unique_poses
    
    @property
    def positions_in_plane(self):
        if self._positions_in_plane is None:
            self._positions_in_plane = self.build_all_positions()
        
        return self._positions_in_plane
    
    
class Cube:
    """State of the cube."""
    
    # Constructor:
    def __init__(self, pieces):
        self._data = np.zeros((3, 3, 3), dtype=int)
        self._pieces = pieces
        self._position_indices = [-1, 0, 0, 0, 0, 0]
        self._location_indices = [0, 0, 0, 0, 0, 0]
        self._current_piece_index = 0
        
    # Public methods:
    def piece_fits(self, piece_index, position_index, location_index):
        """Return True if piece in position and location fits."""
        
        pos = self._pieces[piece_index].positions_in_plane[position_index]
        face = self.get_face(location_index)
        
        return 2 not in pos+face
    
    def place_piece(self, piece_index, position_index, location_index):
        
        pos = self._pieces[piece_index].positions_in_plane[position_index]
        
        self.set_face(location_index, pos)
    
    def get_face(self, index):
        """Return 3x3 face located at location index 'index'."""
        
        if index in [0, 1, 2]:
            return self._data[:, :, index]
        
        if index in [3, 4, 5]:
            return self._data[:, index - 3, :]
        
        if index in [6, 7, 8]:
            return self._data[index - 6, :, :]
    
    def set_face(self, index, value):
    
        if index in [0, 1, 2]:
            self._data[:, :, index] = value
    
        if index in [3, 4, 5]:
            self._data[:, index - 3, :] = value
    
        if index in [6, 7, 8]:
            self._data[index - 6, :, :] = value
    
    def next(self):
        current_piece = self._pieces[self._current_piece_index]
        n_positions = len(current_piece.positions_in_plane)
        current_position = self._position_indices[self._current_piece_index]
        current_location = self._location_indices[self._current_piece_index]
        
        if current_position + 1 < n_positions:
            self._position_indices[self._current_piece_index] += 1
            
        elif current_location < 8:
            self._location_indices[self._current_piece_index] += 1
            self._position_indices[self._current_piece_index] = 0
        
        elif self._current_piece_index + 1 < len(self._pieces):
            self._current_piece_index += 1
        
        else:
            raise Exception("No solution")
        
    # Special methods:
    def __str__(self):
        return "\n".join(["   ".join([str(self._data[i, :, k]) for k in range(3)]) for i in range(3)])

