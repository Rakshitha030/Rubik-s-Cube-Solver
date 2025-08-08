   # 
    # -- FULL PLL (subset shown here; extend with all 21) --
PLL_CASES = {
    # Corner Permutations
    'PLL_Aa': (
        lambda cube: cube.match_pll_pattern('Aa'),
        "x R' U R' D2 R U' R' D2 R2 x'"
    ),
    'PLL_Ab': (
        lambda cube: cube.match_pll_pattern('Ab'),
        "x' R U' R D2 R' U R D2 R2 x"
    ),
    'PLL_E': (
        lambda cube: cube.match_pll_pattern('E'),
        "x' R U' R' D R U R' D' R U R' D R U' R' D' x"
    ),

    # Edge 3-Cycles
    'PLL_Ua': (
        lambda cube: cube.match_pll_pattern('Ua'),
        "R U' R U R U R U' R' U' R2"
    ),
    'PLL_Ub': (
        lambda cube: cube.match_pll_pattern('Ub'),
        "R2 U R U R' U' R' U' R' U R'"
    ),
    'PLL_Z': (
        lambda cube: cube.match_pll_pattern('Z'),
        "M2 U M2 U M' U2 M2 U2 M' U2"
    ),
    'PLL_H': (
        lambda cube: cube.match_pll_pattern('H'),
        "M2 U M2 U2 M2 U M2"
    ),

    # T, J, R perms
    'PLL_T': (
        lambda cube: cube.match_pll_pattern('T'),
        "R U R' U' R' F R2 U' R' U' R U R' F'"
    ),
    'PLL_Ja': (
        lambda cube: cube.match_pll_pattern('Ja'),
        "L' U' L F L' U' L U L F' L2 U L U"
    ),
    'PLL_Jb': (
        lambda cube: cube.match_pll_pattern('Jb'),
        "R U R' F' R U R' U' R' F R2 U' R' U'"
    ),
    'PLL_Ra': (
        lambda cube: cube.match_pll_pattern('Ra'),
        "R U' R' U' R U R D R' U' R D' R' U2 R'"
    ),
    'PLL_Rb': (
        lambda cube: cube.match_pll_pattern('Rb'),
        "R' U2 R U2 R' F R U R' U' R' F' R2 U'"
    ),

    # V, F, G perms
    'PLL_V': (
        lambda cube: cube.match_pll_pattern('V'),
        "R' U R' d' R' F' R2 U' R' U R' F R F"
    ),
    'PLL_F': (
        lambda cube: cube.match_pll_pattern('F'),
        "R' U' F' R U R' U' R' F R2 U' R' U'"
    ),

    # G perms
    'PLL_Ga': (
        lambda cube: cube.match_pll_pattern('Ga'),
        "R2 U R' U R' U' R U' R2 D U' R U R' D'"
    ),
    'PLL_Gb': (
        lambda cube: cube.match_pll_pattern('Gb'),
        "R' U' R U D' R2 U R' U R U' R U' R2 D"
    ),
    'PLL_Gc': (
        lambda cube: cube.match_pll_pattern('Gc'),
        "R2 U' R U' R U R' U R2 D' U R' U' R D"
    ),
    'PLL_Gd': (
        lambda cube: cube.match_pll_pattern('Gd'),
        "R U R' U' D R2 U' R U' R' U R' U R2 D'"
    )
}