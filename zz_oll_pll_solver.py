from oll_pll_cases import OLL_CASES
from pll_cases import PLL_CASES
from pll_patterns import PLL_PATTERNS

class ZZ_LLSolver:
    def __init__(self, cube):
        print("[DEBUG] ZZ_LLSolver initialized.")
        self.cube = cube
        self.OLL_CASES = OLL_CASES
        self.PLL_CASES = PLL_CASES
        self.PLL_PATTERNS = PLL_PATTERNS
        print("[DEBUG] OLL_CASES loaded:", len(self.OLL_CASES))

    def solve(self):
        print("[DEBUG] Entering LL solve")
        moves = []

        if not self.is_oll_solved():
            moves += self.solve_oll()

        if not self.is_pll_solved():
            moves += self.solve_pll()

        return moves

    def is_oll_solved(self):
        return all(color == 'Y' for color in self.cube.state['U'])

    def is_pll_solved(self):
        return self.cube.is_solved()

    def solve_oll(self):
        for _ in range(4):
            u_face = self.cube.state['U']
            print("[DEBUG] Raw U face colors:", u_face)
            if len(u_face) != 9:
                raise ValueError("[ERROR] U face does not have 9 stickers")

            orientation_mask = ''.join(['1' if color == 'Y' else '0' for color in u_face])
            print("[DEBUG] Trying orientation mask:", orientation_mask)

            if orientation_mask in self.OLL_CASES:
                oll_name, oll_algo = self.OLL_CASES[orientation_mask]
                print(f"[DEBUG] OLL matched: {oll_name}, applying {oll_algo}")
                self.cube.apply_moves(oll_algo)
                return oll_algo.split()
            else:
                self.cube.apply_moves("U")  # Rotate U and try again

        raise ValueError(f"[ERROR] OLL case not recognized: {orientation_mask} — Possible incorrect cube state.")

    def solve_pll(self):
        for _ in range(4):
            for pll_name, algo in self.PLL_PATTERNS.items():
                if self.match_pll(pll_name):
                    print(f"[DEBUG] PLL match found: {pll_name}, applying {algo}")
                    self.cube.apply_moves(algo)
                    return algo.split()
            self.cube.apply_moves("U")  # Rotate U and try again

        raise ValueError("PLL case not recognized")

    def match_pll(self, pll_name):
        pattern = self.PLL_CASES.get(pll_name)
        if not pattern:
            return False

        for face, expected_colors in pattern.items():
            if self.cube.state.get(face) != expected_colors:
                return False

        return True



