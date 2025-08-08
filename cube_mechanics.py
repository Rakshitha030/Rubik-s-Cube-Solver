import random

FACES = ['U', 'D', 'F', 'B', 'L', 'R']

class Cube:
    def __init__(self, state=None):
        if state:
            self.state = state
        else:
            self.state = {face: [face] * 9 for face in FACES}
        self.move_log = []

    def validate(self):
        for face in FACES:
            if face not in self.state or len(self.state[face]) != 9:
                raise ValueError(f"Invalid state for face {face}: {self.state.get(face)}")

    def rotate_face(self, face):
        s = self.state[face]
        self.state[face] = [s[6], s[3], s[0],
                            s[7], s[4], s[1],
                            s[8], s[5], s[2]]

    def rotate_face_ccw(self, face):
        s = self.state[face]
        self.state[face] = [s[2], s[5], s[8],
                            s[1], s[4], s[7],
                            s[0], s[3], s[6]]

    def rotate_adjacent(self, face, ccw=False):
        adjacent_map = {
            'U': [('B', [0,1,2]), ('R', [0,1,2]), ('F', [0,1,2]), ('L', [0,1,2])],
            'D': [('F', [6,7,8]), ('R', [6,7,8]), ('B', [6,7,8]), ('L', [6,7,8])],
            'F': [('U', [6,7,8]), ('R', [0,3,6]), ('D', [2,1,0]), ('L', [8,5,2])],
            'B': [('U', [2,1,0]), ('L', [0,3,6]), ('D', [6,7,8]), ('R', [8,5,2])],
            'L': [('U', [0,3,6]), ('F', [0,3,6]), ('D', [0,3,6]), ('B', [8,5,2])],
            'R': [('U', [8,5,2]), ('B', [0,3,6]), ('D', [8,5,2]), ('F', [8,5,2])]
        }

        faces = adjacent_map[face]
        values = [self.state[f][i] for f, idxs in faces for i in idxs]

        shift = -3 if ccw else 3
        values = values[shift:] + values[:shift]

        for (f, idxs), i in zip(faces, range(0, 12, 3)):
            for j, idx in enumerate(idxs):
                self.state[f][idx] = values[i + j]

    def apply_move(self, move):
        face = move[0]
        if face not in FACES:
            raise ValueError(f"Invalid move face: {face}")
        self.move_log.append(move)

        if len(move) == 1:
            self.rotate_face(face)
            self.rotate_adjacent(face)
        elif move[1] == "'":
            self.rotate_face_ccw(face)
            self.rotate_adjacent(face, ccw=True)
        elif move[1] == '2':
            self.rotate_face(face)
            self.rotate_adjacent(face)
            self.rotate_face(face)
            self.rotate_adjacent(face)
        else:
            raise ValueError(f"Invalid move format: {move}")

    def apply_moves(self, moves):
        for move in moves.split():
            self.apply_move(move)

    def print_cube(self):
        for face in FACES:
            print(face + ":", self.state[face])



