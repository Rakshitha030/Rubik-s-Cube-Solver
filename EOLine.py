EDGE_POSITIONS = [
    (('U', 1), ('B', 1)), (('U', 3), ('L', 1)), (('U', 5), ('R', 1)), (('U', 7), ('F', 1)),
    (('D', 1), ('F', 7)), (('D', 3), ('L', 7)), (('D', 5), ('R', 7)), (('D', 7), ('B', 7)),
    (('F', 3), ('L', 5)), (('F', 5), ('R', 3)),
    (('B', 3), ('R', 5)), (('B', 5), ('L', 3)),
]

# Rotation logic to simulate Y-axis cube rotation
def rotate_face_y(face):
    rotation = {'F': 'R', 'R': 'B', 'B': 'L', 'L': 'F', 'U': 'U', 'D': 'D'}
    return rotation.get(face, face)

class EO_EOLineSolver:
    def __init__(self, cube):
        self.cube = cube
        self.moves = []

    def is_oriented(self, edge, col1, col2):
        # An edge with W must lie between U/D and another face to be oriented
        return not ('W' in (col1, col2) and edge[0][0] not in ['U', 'D'] and edge[1][0] not in ['U', 'D'])

    def get_unoriented_white_edges(self):
        unoriented = []
        for edge in EDGE_POSITIONS:
            (f1, i1), (f2, i2) = edge
            col1 = self.cube.state[f1][i1]
            col2 = self.cube.state[f2][i2]
            if 'W' in (col1, col2) and not self.is_oriented(edge, col1, col2):
                unoriented.append(edge)
        return unoriented

    def get_oriented_white_edges(self):
        oriented = []
        for edge in EDGE_POSITIONS:
            (f1, i1), (f2, i2) = edge
            col1 = self.cube.state[f1][i1]
            col2 = self.cube.state[f2][i2]
            if 'W' in (col1, col2) and self.is_oriented(edge, col1, col2):
                oriented.append(edge)
        return oriented

    def move_edge_to_down(self, edge):
        """Rotate Y until white edge comes to D layer if possible."""
        for _ in range(4):
            (f1, i1), (f2, i2) = edge
            if f1 == 'D' or f2 == 'D':
                return
            f1 = rotate_face_y(f1)
            f2 = rotate_face_y(f2)
            edge = ((f1, i1), (f2, i2))

    def flip_all_unoriented_edges(self):
        for _ in range(10):  # Try max 10 times
            unoriented = self.get_unoriented_white_edges()
            if not unoriented:
                return
            edge = unoriented[0]
            self.move_edge_to_down(edge)
            self.cube.apply_moves("F R' D R F'")  # Flip sequence (can customize if needed)
            self.moves += ["F", "R'", "D", "R", "F'"]
    def align_df(self):
        """Align DF edge with front color (F1 == F4)"""
        for _ in range(4):
            if self.cube.state['D'][7] == 'W' and self.cube.state['F'][1] == self.cube.state['F'][4]:
                return
            self.cube.apply_move("D")
            self.moves.append("D")

    def align_db(self):
        """Align DB edge with back color (B1 == B4)"""
        for _ in range(4):
            if self.cube.state['D'][1] == 'W' and self.cube.state['B'][1] == self.cube.state['B'][4]:
                return
            self.cube.apply_move("D")
            self.moves.append("D")

    def solve(self):
        self.flip_all_unoriented_edges()
        self.align_df()
        self.align_db()
        return self.moves

    def find_edge(self, sticker1, sticker2):
        for edge in EDGE_POSITIONS:
            if (edge[0] == sticker1 and edge[1] == sticker2) or \
               (edge[1] == sticker1 and edge[0] == sticker2):
                return edge
        return None

def apply_dynamic_eo_flips(cube):
    unoriented_edges = cube.get_unoriented_white_edges()
    if not unoriented_edges:
        return False

    for edge in unoriented_edges:
        positions = sorted([edge[0], edge[1]])

        if positions == [('F', 1), ('U', 7)]:
            cube.apply_moves("F R D R' D' F'")
            return True
        elif positions == [('B', 1), ('U', 1)]:
            cube.apply_moves("B L D L' D' B'")
            return True
        elif positions == [('L', 1), ('U', 3)]:
            cube.apply_moves("L F D F' D' L'")
            return True
        elif positions == [('R', 1), ('U', 5)]:
            cube.apply_moves("R B D B' D' R'")
            return True

    return False

def rotate_middle_slice(cube, ccw=False):
    indices = [(('U', 1), ('D', 1), ('F', 1), ('B', 1))]
    temp = [cube.state[f][i] for f, i in indices[0]]
    if not ccw:
        for i in range(4):
            cube.state[indices[0][(i + 1) % 4][0]][indices[0][(i + 1) % 4][1]] = temp[i]
    else:
        for i in range(4):
            cube.state[indices[0][(i - 1) % 4][0]][indices[0][(i - 1) % 4][1]] = temp[i]
# --- EO LOGIC ---

WHITE_EDGES = [
    ('U', 1), ('U', 3), ('U', 5), ('U', 7),
    ('D', 1), ('D', 3), ('D', 5), ('D', 7),
    ('F', 1), ('F', 3), ('F', 5), ('F', 7),
    ('B', 1), ('B', 3), ('B', 5), ('B', 7),
    ('L', 1), ('L', 3), ('L', 5), ('L', 7),
    ('R', 1), ('R', 3), ('R', 5), ('R', 7)
]

def is_white_edge(color):
    return color == 'W'

def detect_white_edges(cube):
    white_edges = []
    for face, idx in WHITE_EDGES:
        if is_white_edge(cube.state[face][idx]):
            white_edges.append((face, idx))
    return white_edges

def is_edge_oriented(edge_pos, cube):
    """Check if an edge is EO-correct (white/yellow on U or D face)."""
    face1, idx1 = edge_pos[0]
    face2, idx2 = edge_pos[1]
    color1 = cube.state[face1][idx1]
    color2 = cube.state[face2][idx2]

    # White or yellow on U or D face is considered oriented
    return (color1 in ['W', 'Y'] and face1 in ['U', 'D']) or \
           (color2 in ['W', 'Y'] and face2 in ['U', 'D']) or \
           (color1 not in ['W', 'Y'] and color2 not in ['W', 'Y'])

def detect_unoriented_edges(cube):
    unoriented = []
    for edge in EDGE_POSITIONS:
        if not is_edge_oriented(edge, cube):
            unoriented.append(edge)
    return unoriented

def count_oriented_edges(cube):
    return sum(
        1 for face, idx in WHITE_EDGES
        if is_white_edge(cube.state[face][idx]) and is_edge_oriented(((face, idx), (face, idx)), cube)
    )

def flip_all_unoriented_edges(cube):
    while apply_dynamic_eo_flips(cube):
        pass

def is_eoline_complete(cube):
    if len(cube.get_unoriented_white_edges()) > 0:
        return False

    # Check DF and DB edges are correctly aligned
    centerF = cube.state['F'][4]
    centerB = cube.state['B'][4]

    df_colors = {
        cube.state['D'][1], cube.state['F'][7]
    }
    db_colors = {
        cube.state['D'][7], cube.state['B'][7]
    }

    return 'W' in df_colors and centerF in df_colors and \
           'W' in db_colors and centerB in db_colors

def insert_df_db_edges(cube):
    white = cube.state['D'][4]
    front = cube.state['F'][4]
    back = cube.state['B'][4]

    df_edge = find_edge(cube, white, front)
    db_edge = find_edge(cube, white, back)
    def apply_dynamic_eo_flips(cube):
        unoriented_edges = detect_unoriented_edges(cube)
        for edge in unoriented_edges:
            positions = sorted([edge[0], edge[1]])

        if positions == [('F', 1), ('U', 7)]:
            cube.apply_moves("F R D R' D' F'")
            return True
        elif positions == [('B', 1), ('U', 1)]:
            cube.apply_moves("B L D L' D' B'")
            return True
        elif positions == [('L', 1), ('U', 3)]:
            cube.apply_moves("L F D F' D' L'")
            return True
        elif positions == [('R', 1), ('U', 5)]:
            cube.apply_moves("R B D B' D' R'")
            return True
    return False

def find_edge(cube, color1, color2):
    for f1, i1 in WHITE_EDGES:
        for f2, i2 in WHITE_EDGES:
            if (f1, i1) == (f2, i2):
                continue
            c1 = cube.state[f1][i1]
            c2 = cube.state[f2][i2]
            if set([c1, c2]) == set([color1, color2]):
                return ((f1, i1), (f2, i2))
    return None

def get_edge_colors(cube, edge):
    return (cube.state[edge[0][0]][edge[0][1]], cube.state[edge[1][0]][edge[1][1]])

def move_edge_to_down(cube, edge_pos, edge_colors, white_color):
    if edge_colors[0] == white_color:
        white_face, white_idx = edge_pos[0]
        color_face, color_idx = edge_pos[1]
        color = edge_colors[1]
    else:
        white_face, white_idx = edge_pos[1]
        color_face, color_idx = edge_pos[0]
        color = edge_colors[0]

    if white_face == 'D':
        return

    if white_face == 'U':
        move_map = {'F': 'F2', 'R': 'R2', 'B': 'B2', 'L': 'L2'}
        if color_face in move_map:
            cube.apply_move(move_map[color_face])
        return

    middle_edge_triggers = {
        ('F', 3): "L' U L", ('F', 5): "R U' R'",
        ('R', 3): "F U' F'", ('R', 5): "B U B'",
        ('B', 3): "R U R'", ('B', 5): "L' U' L",
        ('L', 3): "B' U B", ('L', 5): "F' U' F"
    }

    if (white_face, white_idx) in middle_edge_triggers:
        cube.apply_moves(middle_edge_triggers[(white_face, white_idx)])
        new_edge = find_edge(cube, edge_colors[0], edge_colors[1])
        move_edge_to_down(cube, new_edge, edge_colors, white_color)
        return

    if white_face in ['F', 'R', 'B', 'L']:
        cube.apply_move(white_face + "'")
        cube.apply_move("U")
        cube.apply_move(white_face)
        new_edge = find_edge(cube, edge_colors[0], edge_colors[1])
        move_edge_to_down(cube, new_edge, edge_colors, white_color)


def align_df(cube, front_color, white_color):
    for _ in range(4):
        if cube.state['F'][1] == front_color and cube.state['D'][1] == white_color:
            break
        cube.apply_move("D")
    cube.apply_move("M'")

def align_db(cube, back_color, white_color):
    for _ in range(4):
        if cube.state['B'][1] == back_color and cube.state['D'][7] == white_color:
            break
        cube.apply_move("D")
    cube.apply_move("M")
def insert_df_db_edges(cube):
    white = cube.state['D'][4]
    front = cube.state['F'][4]
    back = cube.state['B'][4]

    df_edge = find_edge(cube, white, front)
    db_edge = find_edge(cube, white, back)

    if df_edge:
        df_colors = get_edge_colors(cube, df_edge)
        move_edge_to_down(cube, df_edge[0], df_colors, white)
        align_df(cube, front, white)

    if db_edge:
        db_colors = get_edge_colors(cube, db_edge)
        move_edge_to_down(cube, db_edge[0], db_colors, white)
        align_db(cube, back, white)

def find_edge(cube, color1, color2):
    edges = [('U', 1), ('U', 3), ('U', 5), ('U', 7),
             ('D', 1), ('D', 3), ('D', 5), ('D', 7),
             ('F', 1), ('F', 5), ('B', 1), ('B', 5),
             ('L', 1), ('L', 5), ('R', 1), ('R', 5)]
    for f1, i1 in edges:
        for f2, i2 in edges:
            if f1 == f2 and i1 == i2:
                continue
            c1 = cube.state[f1][i1]
            c2 = cube.state[f2][i2]
            if set([c1, c2]) == set([color1, color2]):
                return ((f1, i1), (f2, i2))
    return None

def get_edge_colors(cube, edge):
    c1 = cube.state[edge[0][0]][edge[0][1]]
    c2 = cube.state[edge[1][0]][edge[1][1]]
    return (c1, c2)

def move_edge_to_down(cube, edge_pos, edge_colors, white_color):
    """
    Move a white edge to the D layer (DF or DB) from any position.
    """

    # Identify which sticker is white
    if edge_colors[0] == white_color:
        white_face, white_idx = edge_pos[0]
        color_face, color_idx = edge_pos[1]
        color = edge_colors[1]
    else:
        white_face, white_idx = edge_pos[1]
        color_face, color_idx = edge_pos[0]
        color = edge_colors[0]

    # === Case 1: Already in Down layer ===
    if white_face == 'D':
        return  # Already done

    # === Case 2: On U face ===
    if white_face == 'U':
        # Align it above correct center
        move_map = {'F': 1, 'R': 3, 'B': 5, 'L': 7}
        if color_face in move_map:
            for _ in range(move_map[color_face]):
                cube.apply_move("U")
        # Insert down
        cube.apply_move("F2" if color_face == 'F' else
                        "R2" if color_face == 'R' else
                        "B2" if color_face == 'B' else
                        "L2")
        return

    # === Case 3: Edge is in Middle Layer ===
    # Flip it up to U layer first, then call recursively
    # Define known middle edge triggers
    middle_edge_triggers = {
        ('F', 3): "L' U L", ('F', 5): "R U' R'",
        ('R', 3): "F U' F'", ('R', 5): "B U B'",
        ('B', 3): "R U R'", ('B', 5): "L' U' L",
        ('L', 3): "B' U B", ('L', 5): "F' U' F"
    }

    if (white_face, white_idx) in middle_edge_triggers:
        cube.apply_moves(middle_edge_triggers[(white_face, white_idx)])
        # Now should be on U face, re-call
        new_edge = find_edge(cube, edge_colors[0], edge_colors[1])
        move_edge_to_down(cube, new_edge, edge_colors, white_color)
        return

    # === Case 4: Edge is in D but misoriented ===
    # Flip it up using F moves
    if white_face in ['F', 'R', 'B', 'L']:
        cube.apply_move(white_face + "'")
        cube.apply_move("U")
        cube.apply_move(white_face)
        # Now it's on U — recall
        new_edge = find_edge(cube, edge_colors[0], edge_colors[1])
        move_edge_to_down(cube, new_edge, edge_colors, white_color)
        return

    # Default fallback (unreachable in ideal cases)
    print(f"Warning: Could not resolve {edge_pos} to down layer.")

def align_df(cube, front_color, white_color):
    for _ in range(4):
        if cube.state['F'][1] == front_color and cube.state['D'][1] == white_color:
            break
        cube.apply_move("D")
    cube.apply_move("M'")

def align_db(cube, back_color, white_color):
    for _ in range(4):
        if cube.state['B'][1] == back_color and cube.state['D'][7] == white_color:
            break
        cube.apply_move("D")
    cube.apply_move("M")
