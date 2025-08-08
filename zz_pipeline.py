class ZZPipelineSolver:
    def __init__(self, cube):
        self.cube = cube
        self.moves = []

    def solve(self):
        from EOLine import EO_EOLineSolver
        from zz_f2l import ZZ_EO_Solver, ZZF2LSolver
        from zz_oll_pll_solver import ZZ_LLSolver

        # Step 1: EO + EOLine
        print("Solving EO + EOLine...")
        try:
            eoline_solver = EO_EOLineSolver(self.cube)
            eo_moves = eoline_solver.solve()
            self.moves += eo_moves
            print("EO + EOLine Moves:", eo_moves)
        except Exception as e:
            print("Error during EO + EOLine:", e)

        # Step 2: First Two Layers (F2L)
        print("Solving F2L...")
        try:
            f2l_solver = ZZF2LSolver(self.cube)
            f2l_moves = f2l_solver.solve()
            self.moves += f2l_moves
            print("F2L Moves:", f2l_moves)
        except Exception as e:
            print("Error during F2L:", e)

        # Step 3: Last Layer (OLL + PLL)
        print("Solving Last Layer...")
        try:
            ll_solver = ZZ_LLSolver(self.cube)
            ll_moves = ll_solver.solve()
            self.moves += ll_moves
            print("LL Moves:", ll_moves)
        except Exception as e:
            print("Error during LL:", e)

        return self.moves
