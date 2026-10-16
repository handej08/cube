import copy
from cube import RubiksCube, EP, CP, Turn, Corner, Edge, C
from pyTwistyScrambler import scrambler333

def main():
    cube: SmartCube = SmartCube()
    #cube.sequence("Z2 R U R' U' L' U' L U U2 F U' F' U F' U F")
    #cube.sequence("L' D L")
    print(f"Scramble: {cube.scramble()}")
    print(cube.turn_tape)

    cube.show()
    cube.cross()
    cube.show()
    cube.f2l()
    cube.show()

class SmartCube(RubiksCube):
    def __init__(self: SmartCube):
        super().__init__()
        self.color_order: list[str] = ["W", "Y", "G", "B", "R", "O"]
        self.color_opposites: dict[str] = {"W": "Y", "Y": "W", "G": "B", "B": "G", "R": "O", "O": "R"}

        self.f2l_order: list[str] = ["G", "O", "B", "R"]

        self.f2l_sides: dict[tuple[EP | CP | int]] = {
            # edge corner major/minor
            "G": (EP.GO, CP.WGO, 1),
            "O": (EP.BO, CP.WBO, 0),
            "B": (EP.BR, CP.WBR, 1),
            "R": (EP.GR, CP.WGR, 0)
        }

        self.f2l_relatives : list[list[EP | CP]] = [[EP.YB, EP.YO, EP.YG, EP.YR, EP.GR, EP.GO, EP.BO, EP.BR], [CP.YBR, CP.YBO, CP.YGO, CP.YGR, CP.WGR, CP.WGO, CP.WBO, CP.WBR]]

        self.f2l_library: dict[tuple] = {
            # Based on https://drive.google.com/file/d/1nzAXYUWZJ6H2wIOXaHdWXep3W57tArbR/view
            (5, 0, 5, 0): "",
            #1A
            (3, 0, 2, 0): "y F R U2 R' F' y'",
            (0, 1, 2, 0): "F' L' U2 L F",
            (0, 0, 2, 0): "U (R U2 R') U (R U' R')",
            (3, 1, 2, 0): "y U' (L' U2 L) U' (L' U L) y'",
            (2, 0, 2, 0): "U (F R' F' R) U (R U R')",
            (1, 1, 2, 0): "F (U R U' R') F' (R U' R')",
            (1, 0, 2, 0): "(R U2 R') U' (R U R')",
            (2, 1, 2, 0): "y (L' U2 L) U (L' U' L) y'",

            (0, 0, 2, 2): "(R U R')",
            (3, 1, 2, 1): "y (L' U' L) y'",
            (3, 0, 2, 2): "U' (R U R') U (R U R')",
            (0, 1, 2, 1): "y U (L' U' L) U' (L' U' L) y'",
            (2, 0, 2, 2): "R' U2 R2 U R2 U R",
            (1, 1, 2, 1): "y L U2 L2 U' L2 U' L' y'",
            (1, 0, 2, 2): "U' (R U' R') U (R U R')",
            (2, 1, 2, 1): "y U (L' U L) U' (L' U' L) y'",

            (2, 1, 2, 2): "y U' (L' U L) y'",
            (1, 0, 2, 1): "U (R U' R')",
            (0, 1, 2, 2): "y U (L' U2 L) U2 (L' U L) y'",
            (3, 0, 2, 1): "U' (R U2 R') U2 (R U' R')",
            (0, 0, 2, 1): "U' (R U R') U2 (R U' R')",
            (3, 1, 2, 2): "y U (L' U' L) U2 (L' U L) y'",
            (2, 0, 2, 1): "y (L' U L) y' U2 (R U R')",
            (1, 1, 2, 2): "(R U' R') y U2 (L' U' L) y'",
            #1B
            (5, 0, 2, 2): "U (R U R') U2 (R U R')",
            (5, 0, 2, 1): "U' R U' R' U2 R U' R'",
            (5, 1, 2, 2): "U (F' U' F) U' (R U R')",
            (5, 1, 2, 1): "y U' (F U F') U (L' U' L) y'",
            (5, 0, 2, 0): "(U R U' R') (U R U' R') (U R U' R')",
            (5, 1, 2, 0): "(R U' R') (F' U2 F)",

            (1, 0, 5, 1): "(R U R') U' (R U R')",
            (2, 1, 5, 2): "y (L' U' L) U (L' U' L) y'",
            (1, 0, 5, 2): "(R U' R') U (R U' R')",
            (2, 1, 5, 1): "y (L' U L) U' (L' U L) y'",
            (1, 0, 5, 0): "U' (R' F R F') (R U R')",
            (2, 1, 5, 0): "U (R U' R') (F R' F' R)",
            #1C
            (5, 0, 5, 1): "(R U' R') U (R U2 R' U R U' R')",
            (5, 0, 5, 2): "(R U' R') U' (R U R' U2 R U' R')",
            (5, 1, 5, 1): "(R U' R') (F' L' U2 L F)",
            (5, 1, 5, 2): "(F' L' U2 L F) (R U R')",
            (5, 1, 5, 0): "R2 U2 F R2 F' U2 R' U R'",
            #2A
            (6, 0, 2, 0): "U' R' U R2 U' R'",
            (4, 0, 2, 0): "y U L U' L2 U L y'",
            (6, 1, 2, 0): "y R' F R2 U' R' U2 F' y'",
            (4, 1, 2, 0): "L F' L2 U L U2 F",
            (7, 0, 0, 0): "y2 U2 L2 D F2 D' L2 y2",
            (7, 1, 0, 0): "y2 L F' U F L' y2",

            (6, 0, 2, 2): "R' U' R2 U R'",
            (4, 0, 2, 1): "y L U L2 U' L y'",
            (6, 1, 2, 2): "F D R D' F'",
            (4, 1, 2, 1): "L' (F' U' F) L",
            (4, 0, 2, 2): "U' (L' U' L) (R U' R')",
            (6, 0, 2, 1): "U (R U R') (L' U L)",
            (4, 1, 2, 2): "(F U2 F') (R U R')",
            (6, 1, 2, 1): "R' U2 R F' U' F",
            (7, 0, 0, 2): "y2 U (R U R') (L U L') y2",
            (7, 0, 0, 1): "y2 U' (R U' R') (L U' L') y2",
            (7, 1, 0, 2): "y2 U2 F' (L U L') F y2",
            (7, 1, 0, 1): "y2 U2 R (B' U' B) R' y2",
            #2B
            (1, 1, 6, 0): "y U (R U' R') (L' U L) y'",
            (1, 0, 6, 0): "y2 (L' U2 L) U' (L U L') y2",
            (1, 1, 6, 2): "y U2 (R U' R') U (L' U' L) y'",
            (1, 0, 6, 2): "y2 U' L' U' L2 U2 L' y2",
            (1, 1, 6, 1): "y2 F B' U F' B y2",
            (1, 0, 6, 1): "y U' (R U R') (F U F') y'",

            (2, 0, 4, 0): "U' (L' U L) (R U' R')",
            (2, 1, 4, 0): "y' (R U2 R') U (R' U' R) y",
            (2, 0, 4, 1): "y' (F R' F' R) U (R' U2 R) y",
            (2, 1, 4, 1): "y' U R U R2 U2 R y",
            (2, 0, 4, 2): "y' F' B U' F B' y",
            (2, 1, 4, 2): "U (L' U' L) (F' U' F)",

            (3, 0, 7, 0): "y2 U' (F' U F) (L U2 L') y2",
            (0, 1, 7, 0): "y' U (F U' F') (R' U2 R) y",
            (3, 0, 7, 2): "y2 (R U' R') (L U2 L') y2",
            (0, 1, 7, 1): "y' (L' U L) (R' U2 R) y",
            (3, 0, 7, 1): "y2 (R U' R') U (L U L') y2",
            (0, 1, 7, 2): "y2 (R' F R F') (L U2 L') y2",
            #3
            (6, 0, 5, 0): "R2 U' R2 U R2",
            (6, 1, 5, 0): "B' D' R D B",
            (4, 0, 5, 0): "F L F2 L' F'",
            (4, 1, 5, 0): "L D F' D' L'",
            (7, 0, 5, 0): "y' L2 D' B2 D L2 y",
            (7, 1, 5, 0): "y' (L' D' B) U (B' D L) y",

            (4, 1, 4, 0): "y2 (B U B') (L U2 L') y2",
            (6, 1, 6, 0): "y' (B' U' B) (R' U2 R) y",
            (7, 0, 7, 0): "y2 R (L U2 L') R' y2",

            (5, 1, 4, 1): "L F2 L' F U' F",
            (5, 1, 6, 2): "y R' F2 R F' U F' y'",
            (5, 1, 4, 0): "(R' F R U' F') (R U' R')",
            (5, 1, 6, 0): "y (L F' L' U F) (L' U L) y'",
            (5, 1, 4, 2): "y (L U F' L' F) U2 (L' U' L) y'",
            (5, 1, 6, 1): "(R' U' F R F') U2 (R U R')",
            #not included
            (4, 1, 4, 1): "L' U' L F' U2 F U F' U' F",
            (4, 1, 4, 2): "L' U' L U F' U F U' F' U' F",
            (8, 0, 8, 1): "L U L' R U' R U R U R'",
            (8, 0, 8, 2): "L U' L' U R U' R' U2 R U' R'",
            (5, 0, 7, 1): "L U L' R U2 R' U R U R'",
            (6, 1, 5, 2): "R U' R2 U2 R F' U' F",

        }

        self.oll_library: dict[tuple] = {
            (2, 1, 1, 1, 2, 1, 1, 1): "R U2 R2 F R F' U2 R' F R F'",
            (1, 1, 2, 1, 2, 1, 1, 1): "r U r' U2 r U2 R' U2 R U' r'",
            (1, 1, 1, 1, 1, 1, 0, 1): "r' R2 U R' U r U2 r' U M'",
            (2, 1, 2, 1, 0, 1, 2, 1): "M U' r U2 r' U' R U' R' M'",
            (0, 0, 1, 1, 1, 1, 1, 0): "l' U2 L U L' U l",
            (2, 0, 0, 0, 2, 1, 2, 1): "r U2 R' U' R U' r'",
            (1, 0, 1, 1, 1, 1, 0, 0): "r U R' U R U2 r'",
            (2, 0, 2, 0, 0, 1, 2, 1): "l' U' L U' L' U2 l",
            (2, 0, 2, 1, 0, 1, 2, 0): "R U R' U' R' F R2 U R' U' F'",
            (1, 1, 0, 1, 1, 0, 1, 0): "R U R' U R' F R F' R U2 R'",
            (1, 0, 0, 1, 1, 1, 1, 0): "r U R' U R' F R F' R U2 r'",
            (0, 0, 2, 0, 2, 1, 2, 1): "M' R' U' R U' R' U2 R U' R r'",
            (1, 1, 1, 0, 1, 1, 0, 0): "F U R U' R2 F' R U R U' R'",
            (2, 1, 2, 0, 0, 1, 2, 0): "R' F R U R' F' R F U' F'",
            (0, 1, 1, 0, 1, 1, 1, 0): "l' U' l L' U' L U l' U l",
            (2, 1, 0, 0, 2, 1, 2, 0): "r U r' R U R' U' r U' r'",
            (0, 1, 1, 1, 0, 1, 2, 1): "F R' F' R2 r' U R U' R' U' M'",
            (0, 1, 0, 1, 1, 1, 2, 1): "r U R' U R U2 r2 U' R U' R' U2 r",
            (0, 1, 0, 1, 2, 1, 1, 1): "r' R U R U R' U' M' R' F R F'",
            (0, 1, 0, 1, 0, 1, 0, 1): "r U R' U' M2 U R U' R' U' M'",
            (1, 0, 2, 0, 1, 0, 2, 0): "R U2 R' U' R U R' U' R U' R'",
            (2, 0, 2, 0, 1, 0, 1, 0): "R U2 R2 U' R2 U' R2 U2 R",
            (1, 0, 2, 0, 0, 0, 0, 0): "R2 D' R U2 R' D R U2 R",
            (1, 0, 0, 0, 0, 0, 2, 0): "r U R' U' r' F R F'",
            (2, 0, 0, 0, 1, 0, 0, 0): "F' r U R' U' r' F R",
            (2, 0, 0, 0, 2, 0, 2, 0): "R U2 R' U' R U' R'",
            (1, 0, 1, 0, 1, 0, 0, 0): "R U R' U R U2 R'",
            (0, 0, 0, 1, 0, 1, 0, 0): "r U R' U' r' R U R U' R'",
            (1, 0, 0, 1, 0, 1, 2, 0): "R U R' U' R U' R' F' U' F R U R'",
            (2, 0, 1, 1, 0, 1, 0, 0): "F R' F R2 U' R' U' R U R' F2",
            (1, 0, 0, 0, 0, 1, 2, 1): "R' U' F U R U' R' F' R",
            (0, 0, 2, 1, 1, 1, 0, 0): "L U F' U' L' U L F L'",
            (1, 1, 0, 0, 0, 1, 2, 0): "R U R' U' R' F R F'",
            (2, 1, 1, 0, 0, 1, 0, 0): "R U R2 U' R' F R U R U' F'",
            (0, 1, 1, 0, 0, 0, 2, 1): "R U2 R2 F R F' R U2 R'",
            (0, 0, 2, 0, 0, 1, 1, 1): "L' U' L U' L' U L U L F' L' F",
            (0, 0, 1, 1, 0, 1, 2, 0): "F R' F' R U R U' R'",
            (1, 0, 0, 1, 2, 1, 0, 0): "R U R' U R U' R' U' R' F R F'",
            (1, 1, 0, 0, 2, 1, 0, 0): "L F' L' U' L U F U' L'",
            (0, 1, 2, 0, 0, 1, 1, 0): "R' F R U R' U' F' U R",
            (1, 0, 2, 1, 0, 1, 0, 0): "R U R' U R U2 R' F R U R' U' F'",
            (0, 1, 0, 1, 1, 0, 2, 0): "R' U' R U' R' U2 R F R U R' U' F'",
            (2, 0, 0, 0, 0, 1, 1, 1): "F' U' L' U L F",
            (0, 0, 1, 1, 2, 1, 0, 0): "F U R U' R' F'",
            (2, 1, 0, 0, 0, 1, 1, 0): "F R U R' U' F'",
            (0, 0, 1, 1, 2, 0, 0, 1): "R' U' R' F R F' U R",
            (1, 0, 1, 0, 2, 1, 2, 1): "R' U' R' F R F' R' F R F' U R",
            (2, 0, 2, 1, 1, 1, 1, 0): "F R U R' U' R U R' U' F'",
            (2, 0, 2, 0, 1, 1, 1, 1): "r U' r2 U r2 U r2 U' r",
            (2, 1, 2, 0, 1, 0, 1, 1): "r' U r2 U' r2 U' r2 U r'",
            (1, 1, 1, 0, 2, 1, 2, 0): "F U R U' R' U R U' R' F'",
            (1, 0, 1, 1, 2, 0, 2, 1): "R U R' U R U' B U' B' R'",
            (1, 0, 2, 0, 1, 1, 2, 1): "l' U2 L U L' U' L U L' U l",
            (1, 0, 2, 1, 1, 1, 2, 0): "r U2 R' U' R U R' U' R U' r'",
            (1, 1, 2, 0, 1, 1, 2, 0): "R' F R U R U' R2 F' R2 U' R' U R U R'",
            (2, 1, 1, 0, 2, 1, 1, 0): "r' U' r U' R' U R U' R' U R r' U r",
            (0, 1, 0, 0, 0, 1, 0, 0): "R U R' U' M' U R U' r'",

        }

        self.oll_relatives: list[EP | CP] = [CP.YBR, EP.YB, CP.YBO, EP.YO, CP.YGO, EP.YG, CP.YGR, EP.YR]

        self.pll_library: dict[str] = {
            #based on https://www.speedsolving.com/wiki/index.php/PLL
            # the color of each stricker on left and front, the color is first come first serve
            "0101223" : "x L2 D2 L' U' L D2 L' U L' x'", #Aa
            "0102031" : "x' L2 D2 L U L' D2 L U' L x", #Ab
            "0001232" : "R2 B2 R2 L U' L F2 R' D L' F2 R L'", #F
            "0102331" : "F B U2 F' B' L' U R' U2 L U' R", #Ga
            "0102313" : "y R2 F2 U R2 D' R2 D B2 U' F2 B2 R2 y'", #Gb
            "0101232" : "y' B2 R2 L2 U' R2 U R2 D' R2 D L2 B2 y", #Gc
            "0102013" : "y2 L U L' B2 D' R U' R' U R' D B2 y2", #Gd
            "0001123" : "y2 L2 D L D' L B2 R' U R B2 y2", #Ja
            "0001223" : "R2 D' R' D R' B2 L U' L' B2", #Jb
            "0102231" : "y2 F U2 F' U R B' R' F R B R' U F' y2", #Ra
            "0101023" : "R2 F R U R U' R' F' R U2 R' U2 R", #Rb
            "0102213" : "y F2 U' F2 D R2 B2 U B2 D' R2 y'", #T
            "0121032" : "F R B R' F' R L F L' B' L F' R' L'", #E
            "0112331" : "R' U R2 B2 U R' B2 R U' B2 R2 U' R", #Na
            "0012231" : "L U' L2' B2' U' L B2' L' U B2' L2' U L'", #Nb
            "0112231" : "R' U R' U' B' D B' D' B2 R' B' R B R", #V
            "0123312" : "R2 U' R2 U' R2 U F U F' R2 F U' F'", #Y
            "0102321" : "R2 F2 B2 L2 D' R2 F2 B2 L2", #H
            "0101213" : "y B2 U' R L' B2 R' L U' B2 y'", #Ua
            "0102023" : "y B2' U L' R B2' L R' U B2' y'", #Ub
            "0101012" : "y' R L' U2 D2 R L' D' R2 L2 U F2 B2 y", #Z

            "0001112" : "" #PLL skip
            
        }

        self.pll_relatives: list[EP | CP] = [CP.YBR, EP.YR, CP.YGR, CP.YGR, EP.YG, CP.YGO, CP.YGO, EP.YO, CP.YBO, CP.YBO, EP.YB, CP.YBR]

        self.pll_relatives_stickers: list[int] = [1, 1, 2, 1, 1, 2, 1]
    
    def count_turns(self: SmartCube, sequence: str) -> int:
        ret: int = 0
        for i in "udfbrl":
            ret += sequence.lower().count(i)
        return ret

    def solve(self: SmartCube, *, verbose: bool = True, visual: bool = False, step_verbose: bool = False):

        #track turns
        turns: list[str] = []
        self.pop_turn_tape()

        self.cross()
        turns.append(self.pop_turn_tape())
        if step_verbose:
            print(f"Cross ({self.count_turns(turns[-1])}): {turns[-1]}")
        if visual:
            self.show()

        self.f2l()
        turns.append(self.pop_turn_tape())
        if step_verbose:
            print(f"F2L ({self.count_turns(turns[-1])}): {turns[-1]}")
        if visual:
            self.show()

        self.oll()
        turns.append(self.pop_turn_tape())
        if step_verbose:
            print(f"OLL ({self.count_turns(turns[-1])}): {turns[-1]}")
        if visual:
            self.show()

        self.pll()
        turns.append(self.pop_turn_tape())
        if step_verbose:
            print(f"PLL ({self.count_turns(turns[-1])}): {turns[-1]}")
        if visual:
            self.show()

        solution: str = ""
        for i in turns:
            solution += i

        compact_solution: str = self.compact_sequence(solution)

        if not self.is_solved():
            raise Exception("Could not solve cube")

        if verbose:
            print(f"Solution ({self.count_turns(compact_solution)}): {compact_solution}")

        return self.is_solved()

    def compact_sequence(self: SmartCube, sequence: str) -> str:
        #compact duplicate moves
        #keep track of changes
        prev_seq = sequence
        while True:
            new_seq: list[str] = [" "]
            for i, x in enumerate(prev_seq):
                if not x.lower() in "udfblrxyz":
                    continue
                turn: str = x
                # replace 2 and ' with star counters
                if i < len(prev_seq) - 1:
                    if prev_seq[i+1] == "2":
                        turn += "*"
                    elif prev_seq[i+1] == "'":
                        turn += "**"
                if turn[0].lower() == new_seq[-1][0].lower():
                    # change previous and it's stars
                    new_seq[-1] = new_seq[-1][0] + "*" * ((len(turn) + len(new_seq[-1])-1) % 4)
                else:
                    new_seq.append(turn)
            #replace stars with 2 and '
            new_seq_styled: list[str] = [f"{i} ".replace("***", "4").replace("**", "'").replace("*", "2") for i in new_seq[1:]]
            new_seq_compact = ""
            for i in new_seq_styled:
                # remove full turns
                if "4" not in i:
                    new_seq_compact += i
            # return if nothing changed
            if new_seq_compact == prev_seq:
                return new_seq_compact
            else:
                prev_seq = new_seq_compact

    def pop_turn_tape(self: SmartCube, *, compact: bool = True):
        #compacted tape
        return self.compact_sequence(super().pop_turn_tape()) if compact else super().pop_turn_tape()


    def scramble(self: SmartCube, verbose: bool = False) -> str:
        scramble_wca: str = scrambler333.get_WCA_scramble()
        self.sequence(scramble_wca, verbose=verbose)
        return scramble_wca

    def fast_scramble(self: SmartCube,*, length: int = 30, verbose: bool = False) -> str:

        #makes scramble using random moves
        scramble_fast: str = " ".join([random.choice(list(Turn)[:17]).name for _ in range(length)]).replace("_", "'")
        scramble_compact = self.compact_sequence(scramble_fast)
        self.sequence(scramble_compact, verbose=verbose)
        return scramble_compact

    def find_piece(self: SmartCube, variety: int, piece: EP | CP) -> tuple:
        for i, p in enumerate(self.cube[variety]):
            if p.id == piece:
                return (EP(i), p) if variety == 0 else (CP(i), p)

    def face_cycle(self, rotation_instructions):
        super().face_cycle(rotation_instructions)
        self.color_order[rotation_instructions[0]], self.color_order[rotation_instructions[1]], self.color_order[rotation_instructions[2]], self.color_order[rotation_instructions[3]] = self.color_order[rotation_instructions[3]], self.color_order[rotation_instructions[0]], self.color_order[rotation_instructions[1]], self.color_order[rotation_instructions[2]]
             
    def cross_score(self: SmartCube) -> tuple:
        # creates scores for cross piece positions
        cross_pieces = [self.find_piece(0, EP.WB), self.find_piece(0, EP.WR), self.find_piece(0, EP.WG), self.find_piece(0, EP.WO)]
        scores = [-1 for _ in cross_pieces]
        for i, p in enumerate(cross_pieces):
            if p[0] == p[1].id and p[1].rotation == 0:
                scores[i] = 10
            elif p[0] in [EP.WB, EP.WR, EP.WG, EP.WO]:
                if p[1].rotation == 0:
                    scores[i] = 1
                else:
                    scores[i] = 5
            elif p[0] in [EP.YB, EP.YR, EP.YG, EP.YO]:
                if p[1].rotation == 0:
                    scores[i] = 2
                else:
                    scores[i] = 4
            else:
                scores[i] = 3
        return cross_pieces, scores
        

    def cross(self: SmartCube, verbose: bool = False):
        #uses second best if true
        skip_first: bool = False
        while True:
            cross_pieces, scores = self.cross_score()
            if min(scores) == 10:
                break
            #pretend best is solved, prevents loops
            if skip_first:
                scores[min(range(len(scores)), key=scores.__getitem__)] = 10
            target = min(range(len(scores)), key=scores.__getitem__)
            target_piece = cross_pieces[target]
            skip_first = False
            match scores[target]:
                case 1:
                    if max(scores) < 10:
                        while self.find_piece(0, target_piece[1].id)[0] != target_piece[1].id:
                            self.turn(Turn.U, verbose=verbose)
                    else:
                        # if it will cause loop: use second best instead
                        opposite_piece: Edge = self.get_piece(0, EP[(target_piece[0].name.replace("W", "Y"))])
                        if opposite_piece.rotation == 0 and "W" in opposite_piece.id.name:
                            skip_first = True
                        else:
                            self.turn(Turn(self.color_order.index(target_piece[0].name[1])*3+1), verbose=verbose)
                case 2:
                    while self.find_piece(0, target_piece[1].id)[0].name[1] != target_piece[1].id.name[1]:
                        self.turn(Turn.D, verbose=verbose)
                    self.turn(Turn(self.color_order.index(target_piece[1].id.name[1])*3+1), verbose=verbose)

                case 3:
                    side_color: str = target_piece[0].name[int(not bool(target_piece[1].rotation))]
                    piece_to_replace: EP = self.cube[0][target_piece[1].id.value].id
                    rotations = 0
                    while self.find_piece(0, piece_to_replace)[0].name[1] != side_color:
                        self.turn(Turn.U, verbose=verbose)
                        rotations = (rotations + 1) % 4
                    while self.find_piece(0, target_piece[1].id)[0].name[0] != "W":
                        self.turn(Turn(self.color_order.index(side_color)*3), verbose=verbose)
                    for _ in range(rotations):
                        self.turn(Turn.U_, verbose=verbose)

                case 4:
                    
                    while self.find_piece(0, target_piece[1].id)[0].name[1] == target_piece[1].id.name[1] or self.find_piece(0, target_piece[1].id)[0].name[1] == self.color_opposites[target_piece[1].id.name[1]]:
                        self.turn(Turn.D, verbose=verbose)
                    side: Turn = Turn(self.color_order.index(self.find_piece(0, target_piece[1].id)[0].name[1])*3)
                    while target_piece[1].id.name[1] not in self.find_piece(0, target_piece[1].id)[0].name:
                        self.turn(side, verbose=verbose)
                    while self.find_piece(0, target_piece[1].id)[0] != target_piece[1].id:
                        self.turn(Turn(self.color_order.index(target_piece[1].id.name[1])*3), verbose=verbose)



                case 5:
                    side_color: str = target_piece[0].name[1]
                    self.turn(Turn(self.color_order.index(side_color)*3), verbose=verbose)

    def f2l(self: SmartCube, verbose: bool = False):
        self.rotate(Turn.Z2, verbose=verbose)
        #for each pair
        for side in self.f2l_order * 4:
            #turn upper
            for _ in range(4):
                try:
                    edge: tuple = self.find_piece(0, self.f2l_sides[side][0])
                    corner: tuple = self.find_piece(1, self.f2l_sides[side][1])
                    #print(f"..{edge[0]}")
                    edge_state: tuple = (self.f2l_relatives[0].index(edge[0]), edge[1].rotation)
                    corner_state: tuple = (self.f2l_relatives[1].index(corner[0]), corner[1].rotation)
                    #print("e: ", *edge_state, " c: ", *corner_state)
                    
                    #major minor offset
                    # only for upper pieces if minor
                    if edge_state[0] < 4 and not bool(self.f2l_sides[side][2]):
                        #print("changing due to offset")
                        edge_state: tuple = (self.f2l_relatives[0].index(edge[0]), int(not bool(edge_state[1])))

                    state: tuple[int] = (*edge_state, *corner_state)

                    #print("e: ", *edge_state, " c: ", *corner_state)
            
                    
                    self.sequence(self.f2l_library[state], verbose=verbose)
                    #print("Solving")
                    break
                except KeyError:
                    self.turn(Turn.U, verbose=verbose)

            #rotate to next
            self.sequence("y", verbose=verbose)
            #change relatives
            for relatives in self.f2l_relatives:
                relatives[0], relatives[1], relatives[2], relatives[3], relatives[4], relatives[5], relatives[6], relatives[7] = relatives[3], relatives[0], relatives[1], relatives[2], relatives[5], relatives[6], relatives[7], relatives[4]

    def oll(self: SmartCube, verbose: bool = False):
        # find case
        oll_case: list[int] = []
        for i, rel_piece in enumerate(self.oll_relatives):
            piece: Edge | Corner = self.get_piece(int(not(bool(i % 2))), rel_piece)
            oll_case.append(piece.rotation)
        for i in range(4):
            try:
                solution: str = self.oll_library[tuple(oll_case)]
                #solve
                self.sequence("y'" * i + solution + "y" * i, verbose=verbose)

                return
            except KeyError:
                #turn and check from other view
                #account for rotation by shuffling 
                for _ in range(2):
                    front: int = oll_case.pop(0)
                    oll_case.append(front)

    def pll(self: SmartCube, verbose: bool = False):
        
        for i in range(4):
            pll_case: str = ""
            found_colors: list[C] = []
            for j, rel_piece in enumerate(self.pll_relatives[:len(self.pll_relatives_stickers)]):
                piece: Edge | Corner = self.get_piece(int(len(rel_piece.name) > 2), rel_piece)
                
                sticker: C = piece.stickers[self.pll_relatives_stickers[j]]
                if sticker in found_colors:
                    pll_case += str(found_colors.index(sticker))
                else: 
                    pll_case += str(len(found_colors))
                    found_colors.append(sticker)
            try:
                solution: str = self.pll_library[pll_case]
                self.sequence("y" * i + solution + "y'" * i, verbose=verbose)
                #does auf
                self.auf()
                return
            except KeyError:
                #turn and check from other view
                #account for rotation by shuffling 
                front_3: list[EP | CP] = self.pll_relatives[:3]
                self.pll_relatives = self.pll_relatives[3:] + front_3

    def auf(self: SmartCube, verbose: bool = False):
        while (self.get_piece(0, EP.YG).id != EP.YG):
            self.sequence("U", verbose=verbose)
        #rotate to standard
        self.sequence("z2")

    def is_solved(self: SmartCube):
        for piece in self.cube[0] + self.cube[1]:
            if self.get_piece(int(len(piece.stickers) == 3), piece.id) != piece:
                return False
        return True

if __name__ == "__main__":
    main()
