import copy

class Cube:
    def __init__(self):
        self.state = {
            face: [face] * 9 for face in  ['U', 'D', 'F', 'B', 'L', 'R']
        }
    def get(self, face, idx):
        return self.state[face][idx]
      
    def rotate(self, face):
        s = self.state[face]
        self.state[face] = [s[6], s[3], s[0], s[7], s[4], s[1], s[8], s[5], s[2]]
   
    def apply_move(self, move):
        for _ in range(self._move_times(move)):
            self._rotate_face(move[0])
            self._rotate_adjacent_edges(move[0])

    def _move_times(self, move):
        return 2 if "2" in move else 3 if "'" in move else 1
    
    def _rotate_face(self, face):
        self.rotate(face)
    
    def _rotate_adjacent_edges(self, face):
        s = self.state
        
        def cycle(edge_list):
            temp = [s[f][i] for f, idxs in edge_list for i in idxs]
            temp = temp[-3:] + temp[:-3]
            idx = 0
            for f, idxs in edge_list:
                for i in idxs:
                    s[f][i] = temp[idx]
                    idx += 1

        edges = {
            'U': [('F', [0, 1, 2]), ('R', [0, 1, 2]), ('B', [0, 1, 2]), ('L', [0, 1, 2])],
            'D': [('F', [6, 7, 8]), ('L', [6, 7, 8]), ('B', [6, 7, 8]), ('R', [6, 7, 8])],
            'F': [('U', [6, 7, 8]), ('R', [0, 3, 6]), ('D', [2, 1, 0]), ('L', [8, 5, 2])],
            'B': [('U', [2, 1, 0]), ('L', [0, 3, 6]), ('D', [6, 7, 8]), ('R', [8, 5, 2])],
            'L': [('U', [0, 3, 6]), ('F', [0, 3, 6]), ('D', [0, 3, 6]), ('B', [8, 5, 2])],
            'R': [('U', [8, 5, 2]), ('B', [0, 3, 6]), ('D', [8, 5, 2]), ('F', [8, 5, 2])],
        }

        if face in edges:
            cycle(edges[face])
     
    def print_cube(self):
        for face in ['U', 'D', 'F', 'B', 'L', 'R']:
            print(face, self.state[face])

    def solve(self):
        moves = []
        eo_solver = ZZ_EO_Solver(self)
        moves += eo_solver.solve_eo_line()

        f2l_solver = ZZF2LSolver(self)
        moves += f2l_solver.solve()

        return moves
    
class ZZ_EO_Solver:
    def __init__(self, cube):
        self.cube = cube
    def solve(self):
        white_edges = self.find_white_edges()
        for edge in white_edges:
            if not self.is_oriented(edge):
                self.flip_edge(edge)
        return []  # Or return the list of moves if you're tracking them

    def find_white_edges(self):
        eo_edges = [
            ('F', 1), ('F', 5),
            ('B', 1), ('B', 5),
            ('L', 1), ('L', 5),
            ('R', 1), ('R', 5),
            ('U', 3), ('U', 5),
            ('D', 3), ('D', 5),
        ]
        return [e for e in eo_edges if self.cube.get(e[0], e[1]) == 'W']

    def is_oriented(self, edge):
        return edge[0] in ('F', 'B')

    def flip_edge(self, edge):
        face, idx = edge
        flip_seq = {
            ('F', 1): ['R', 'U', "R'", 'U'],
            ('F', 5): ['L', 'U', "L'", 'U'],
            ('B', 1): ['L', 'U', "L'", 'U'],
            ('B', 5): ['R', 'U', "R'", 'U'],
        }
        for move in flip_seq.get((face, idx), []):
            self.cube.apply_move(move)

def insert_df_db(self):
    # Map edge color positions to target DF and DB spots
    target_edges = {
        'DF': ('D', 7),
        'DB': ('D', 1)
    }

    for label, (face, idx) in target_edges.items():
        inserted = False
        for f in ['F', 'B', 'R', 'L', 'U', 'D']:
            for i in [1, 3, 5, 7]:
                if self.cube.get(f, i) == 'W':
                    # Simple placeholder logic (should be replaced with actual move planning)
                    self.cube.apply_move("U")  # Rotate until aligned
                    self.cube.apply_move("F'")  # Insert down
                    inserted = True
                    break
            if inserted:
                break

            
class ZZF2LSolver:
    def __init__(self, cube):
        self.cube = cube
        self.moves = []
        self.color_face = self.get_color_face_mapping()

    def solve(self):
        pairs = self.detect_f2l_pairs()
        for corner_pos, edge_pos in pairs:
            if self.is_slot_solved(corner_pos):
                continue
            slot_face = self.get_slot_face(corner_pos)
            self.rotate_slot_to_FR(slot_face)
            pair_type = self.classify_f2l_pair(corner_pos, edge_pos)
            self.advanced_extract_pair(corner_pos, edge_pos, pair_type)
            self.advanced_insert_pair(pair_type)
        return self.optimize_moves(self.moves)

    # ----------------------------------
    # MAPPING AND HELPERS
    # ----------------------------------
    def get_color_face_mapping(self):
        return {self.cube.state[face][4]: face for face in ['U', 'D', 'F', 'B', 'L', 'R']}

    def get_slot_face(self, corner_pos):
        colors = set(self.get_corner_colors(corner_pos)[1:])
        if colors == {'G', 'R'}:
            return 'F'
        elif colors == {'G', 'O'}:
            return 'F'
        elif colors == {'B', 'R'}:
            return 'B'
        elif colors == {'B', 'O'}:
            return 'B'
        return 'F'  # default

    def rotate_slot_to_FR(self, slot_face):
        u_rotations = {
            'F': [],
            'R': ['U'],
            'B': ['U2'],
            'L': ["U'"]
        }
        self.moves.extend(u_rotations.get(slot_face, []))

    def get_corner_colors(self, corner_pos):
        colors = []
        for face, i, j in corner_pos:
         index = i * 3 + j
        colors.append(self.cube.state[face][index])
        return colors

    def get_adjacent_corner_faces(self, face, i, j):
        map = {
            ('U', 0, 0): [('L', 0, 2), ('B', 0, 0)],
            ('U', 0, 2): [('B', 0, 2), ('R', 0, 0)],
            ('U', 2, 0): [('L', 0, 0), ('F', 0, 0)],
            ('U', 2, 2): [('F', 0, 2), ('R', 0, 2)],
        }
        return map.get((face, i, j), [])

    def detect_f2l_pairs(self):
        # Simplified detection — assumes 2 corner/edge pairs for example
        return [(
    [('U', 2, 2), ('R', 0, 0), ('F', 0, 2)],  # corner at URF
    ('F', 'R')                               # edge between F-R
), (
    [('U', 2, 0), ('L', 0, 2), ('F', 0, 0)],  # corner at ULF
    ('F', 'L')                               # edge between F-L
)]

    def classify_f2l_pair(self, corner_pos, edge_pos):
        corner_colors = self.get_corner_colors(corner_pos)

        if 'W' not in corner_colors:
            return 'advanced'  # assume solved or misplaced

    # Detect if corner is in U-layer and edge is also in U-layer
        corner_in_U = any(face == 'U' for face, _, _ in corner_pos)
        edge_in_U = 'U' in edge_pos

        if corner_in_U and edge_in_U:
            return 'both_in_U'
        elif corner_in_U:
            return 'corner_in_U'
        elif edge_in_U:
            return 'edge_in_U'
        else:
            return 'both_inserted'


    def is_slot_solved(self, corner_pos):
        # You can complete this properly based on actual sticker match
        return False

    # ----------------------------------
    # ADVANCED EXTRACT + INSERT LOGIC
    # ----------------------------------

    def advanced_extract_pair(self, corner_pos, edge_pos, pair_type):
        if pair_type == 'stuck':
            self.moves.extend(["R", "U", "R'"])  # Bring up corner
        elif pair_type == 'split':
            self.moves.extend(["U", "R", "U'", "R'"])  # Pair it
        else:
            pass  # already paired

    def advanced_insert_pair(self, pair_type):
        if pair_type == 'good_pair':
            self.moves.extend(["U'", "R'", "U", "R"])
        elif pair_type == 'split':
            self.moves.extend(["U2", "R", "U'", "R'", "U", "R", "U'", "R'"])
        elif pair_type == 'stuck':
            self.moves.extend(["R", "U", "R'", "U'", "R", "U", "R'"])
        else:
            self.moves.extend(["U'", "R'", "U", "R"])

    # ----------------------------------
    # MOVE OPTIMIZATION
    # ----------------------------------

    def optimize_moves(self, moves):
        optimized = []
        i = 0
        while i < len(moves):
            if i + 1 < len(moves) and moves[i] == moves[i + 1]:
                optimized.append(moves[i] + '2')
                i += 2
            elif i + 2 < len(moves) and moves[i] == moves[i + 1] == moves[i + 2]:
                optimized.append(moves[i] + "'")
                i += 3
            else:
                optimized.append(moves[i])
                i += 1
        return optimized



