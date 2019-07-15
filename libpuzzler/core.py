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

    # Public methods:
    def piece_fits(self, piece_index, position_index, location_index):
        """Return True if piece in position and location fits."""
        
        pos = self._pieces[piece_index].positions_in_plane[position_index]
        face = self.get_face(location_index)
        
        return 2 not in pos+face
    
    def place_piece(self, piece_index, position_index, location_index):
        
        pos = self._pieces[piece_index].positions_in_plane[position_index]
        self._position_indices[piece_index] = position_index
        self._location_indices[piece_index] = location_index

        self.put_into_face(location_index, pos)

    def remove_piece(self, piece_index):
        """Remove i-th piece."""

        i_pos = self._position_indices[piece_index]
        i_loc = self._location_indices[piece_index]
        pos = -1 * self._pieces[piece_index].positions_in_plane[i_pos]

        self.put_into_face(i_loc, pos)

    def get_face(self, index):
        """Return 3x3 face located at location index 'index'."""
        
        if index in [0, 1, 2]:
            return self._data[:, :, index]
        
        if index in [3, 4, 5]:
            return self._data[:, index - 3, :]
        
        if index in [6, 7, 8]:
            return self._data[index - 6, :, :]
    
    def put_into_face(self, index, value):
    
        if index in [0, 1, 2]:
            self._data[:, :, index] += value
    
        if index in [3, 4, 5]:
            self._data[:, index - 3, :] += value
    
        if index in [6, 7, 8]:
            self._data[index - 6, :, :] += value

    def first_available_for_piece(self, piece_index):
        """Return first available position+location for piece_index-th Piece."""

        current_piece = self._pieces[piece_index]
        current_i_loc = self._location_indices[piece_index]
        current_i_pos = self._position_indices[piece_index]
        n_pos = len(current_piece.positions_in_plane)

        # Current location, all remaining positions:
        for i_pos in range(current_i_pos+1, n_pos):
            if self.piece_fits(piece_index, i_pos, current_i_loc):
                return current_i_loc, i_pos

        # For locations forward, all positions:
        for i_loc in range(current_i_loc+1, 9):
            for i_pos in range(n_pos):
                if self.piece_fits(piece_index, i_pos, i_loc):
                    return i_loc, i_pos

        return None, None

    def run(self):
        """Find solution."""

        i_piece = 0
        while True:
            loc, pos = self.first_available_for_piece(i_piece)
            if loc is None:
                self._location_indices[i_piece] = 0
                self._position_indices[i_piece] = 0
                i_piece -= 1
                if i_piece < 0:
                    print("failure")
                    break
                else:
                    self.remove_piece(i_piece)
            else:
                self.place_piece(i_piece, pos, loc)
                i_piece += 1
                if i_piece == len(self._pieces):
                    print("success")
                    print(self._location_indices)
                    print(self._position_indices)
                    break

    # Special methods:
    def __str__(self):
        return "\n".join(["   ".join([str(self._data[i, :, k]) for k in range(3)]) for i in range(3)])

