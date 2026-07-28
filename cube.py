from enum import Enum
from copy import deepcopy
from termcolor import colored
from math import floor

def main():
    cube: RubiksCube = RubiksCube()
    cube.sequence("R2 D2 B2 D' L2 D2 L2 D2 R2 F2 R F R' B' L D2 F' D2 R2 F2")
    cube.show()

class RubiksCube:
    def __init__(self: RubiksCube):
        self.cube: tuple(list[Piece]) = ([
            Edge(EP.WB, C.WHITE, C.BLUE),
            Edge(EP.WR, C.WHITE, C.RED),
            Edge(EP.WG, C.WHITE, C.GREEN),
            Edge(EP.WO, C.WHITE, C.ORANGE),
            Edge(EP.YG, C.YELLOW, C.GREEN),
            Edge(EP.YR, C.YELLOW, C.RED),
            Edge(EP.YB, C.YELLOW, C.BLUE),
            Edge(EP.YO, C.YELLOW, C.ORANGE),
            Edge(EP.GO, C.GREEN, C.ORANGE),
            Edge(EP.GR, C.GREEN, C.RED),
            Edge(EP.BR, C.BLUE, C.RED),
            Edge(EP.BO, C.BLUE, C.ORANGE)
        ],
        [
            Corner(CP.WBO, C.WHITE, C.ORANGE, C.BLUE),
            Corner(CP.WBR, C.WHITE, C.BLUE, C.RED),
            Corner(CP.WGR, C.WHITE, C.RED, C.GREEN),
            Corner(CP.WGO, C.WHITE, C.GREEN, C.ORANGE),
            Corner(CP.YGO, C.YELLOW, C.ORANGE, C.GREEN),
            Corner(CP.YGR, C.YELLOW, C.GREEN, C.RED),
            Corner(CP.YBR, C.YELLOW, C.RED, C.BLUE),
            Corner(CP.YBO, C.YELLOW, C.BLUE, C.ORANGE)
        ])

        self.colors = ["white", "light_yellow", "green", "blue", "red", (255, 165, 0)]

        self.display = [[(-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (1, CP.WBO, 0), (0, EP.WB, 0), (1, CP.WBR, 0)],
                        [(-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (0, EP.WO, 0), (2, C.WHITE, 0), (0, EP.WR, 0)],
                        [(-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (1, CP.WGO, 0), (0, EP.WG, 0), (1, CP.WGR, 0)],

                        [],

                        [(1, CP.WBO, 1), (0, EP.WO, 1), (1, CP.WGO, 2),  (-1, 0, 0),  (1, CP.WGO, 1), (0, EP.WG, 1), (1, CP.WGR, 2),  (-1, 0, 0),  (1, CP.WGR, 1), (0, EP.WR, 1), (1, CP.WBR, 2),  (-1, 0, 0),  (1, CP.WBR, 1), (0, EP.WB, 1), (1, CP.WBO, 2)],
                        [(0, EP.BO, 1), (2, C.ORANGE, 0), (0, EP.GO, 1),  (-1, 0, 0),  (0, EP.GO, 0), (2, C.GREEN, 0), (0, EP.GR, 0),  (-1, 0, 0),  (0, EP.GR, 1), (2, C.RED, 0), (0, EP.BR, 1),  (-1, 0, 0),  (0, EP.BR, 0), (2, C.BLUE, 0), (0, EP.BO, 0)],
                        [(1, CP.YBO, 2), (0, EP.YO, 1), (1, CP.YGO, 1),  (-1, 0, 0),  (1, CP.YGO, 2), (0, EP.YG, 1), (1, CP.YGR, 1),  (-1, 0, 0),  (1, CP.YGR, 2), (0, EP.YR, 1), (1, CP.YBR, 1),  (-1, 0, 0),  (1, CP.YBR, 2), (0, EP.YB, 1), (1, CP.YBO, 1)],

                        [],

                        [(-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (1, CP.YGO, 0), (0, EP.YG, 0), (1, CP.YGR, 0)],
                        [(-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (0, EP.YO, 0), (2, C.YELLOW, 0), (0, EP.YR, 0)],
                        [(-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (-1, 0, 0), (1, CP.YBO, 0), (0, EP.YB, 0), (1, CP.YBR, 0)],
                        ]

        self.turn_library: list[tuple[list[tuple]]] = [
            (((EP.WG, 0), (EP.WO, 0), (EP.WB, 0), (EP.WR, 0)), ((CP.WGR, 0), (CP.WGO, 0), (CP.WBO, 0), (CP.WBR, 0))), #U 0
            (((EP.YG, 0), (EP.YR, 0), (EP.YB, 0), (EP.YO, 0)), ((CP.YGR, 0), (CP.YBR, 0), (CP.YBO, 0), (CP.YGO, 0))), #D 1
            (((EP.WG, 1), (EP.GR, 0), (EP.YG, 1), (EP.GO, 0)), ((CP.WGO, 1), (CP.WGR, 2), (CP.YGR, 1), (CP.YGO, 2))), #F 2
            (((EP.WB, 1), (EP.BO, 0), (EP.YB, 1), (EP.BR, 0)), ((CP.WBR, 1), (CP.WBO, 2), (CP.YBO, 1), (CP.YBR, 2))), #B 3
            (((EP.GR, 1), (EP.WR, 1), (EP.BR, 1), (EP.YR, 1)), ((CP.WGR, 1), (CP.WBR, 2), (CP.YBR, 1), (CP.YGR, 2))), #R 4
            (((EP.WO, 1), (EP.GO, 1), (EP.YO, 1), (EP.BO, 1)), ((CP.WBO, 1), (CP.WGO, 2), (CP.YGO, 1), (CP.YBO, 2)))  #L 5
        ]

        self.rotation_library: list[list[int]] = [
            [2, 0, 3, 1], #X
            [2, 5, 3, 4], #Y
            [0, 4, 1, 5]  #Z
        ]

    def show(self: RubiksCube):
        value = ""
        for row in self.display:
            for item in row:
                piece_variety, piece, offset = item
                match piece_variety:
                    # empty
                    case -1:
                        value += "  "
                    # edge and corner
                    case 0 | 1:
                        value += colored("■ ", self.colors[self.get_sticker(piece_variety, piece, offset).value])
                    # center
                    case 2:
                        value += colored("■ ", self.colors[piece.value])
            value += "\n"
        print(value)

    def get_sticker(self: RubiksCube, variety: int, piece: int, offset: int):
        found_piece: Piece = self.cube[variety][piece.value]
        return found_piece.stickers[(found_piece.rotation + offset) % found_piece.size]
    
    def get_piece(self: RubiksCube, variety: int, piece: int):
        return self.cube[variety][piece.value]

    def cycle(self: RubiksCube, variety: int, *stickers: tuple):
        # either all edges or all corners
        group: list[Edge | Corner] = self.cube[variety]
        last: Edge | Corner = deepcopy(group[stickers[-1][0].value])
        for i in range(len(stickers) - 1, 0, -1):
            group[stickers[i-1][0].value].rotation = (group[stickers[i-1][0].value].rotation + stickers[i-1][1] - stickers[i][1]) % len(group[stickers[i-1][0].value].stickers)
            #shuffle
            group[stickers[i][0].value] = group[stickers[i-1][0].value]
        last.rotation = (last.rotation + stickers[-1][1] - stickers[0][1]) % len(last.stickers)
        group[stickers[0][0].value] = last

    def turn(self: RubiksCube, turn: Turn, verbose: bool = False):
        turn_type: int = turn.value % 3
        turn_instructions: tuple[list[tuple]] = self.turn_library[floor(turn.value/3)]
        for _ in range(turn_type + 1):
            self.cycle(0, *turn_instructions[0])
            self.cycle(1, *turn_instructions[1])
        if verbose:
            print(turn.name.replace("_", "'"))

    def rotate(self: RubiksCube, rot: Turn, verbose: bool = False):
        rot_type: int = rot.value % 3
        rot_instructions: list[int] = self.rotation_library[floor(rot.value/3) - 6]
        for _ in range(rot_type + 1):
            self.face_cycle(rot_instructions)
        if verbose:
            print(rot.name.replace("_", "'"))

    def face_cycle(self: RubiksCube, rotation_instructions: list[int]):
        self.turn_library[rotation_instructions[0]], self.turn_library[rotation_instructions[1]], self.turn_library[rotation_instructions[2]], self.turn_library[rotation_instructions[3]] = self.turn_library[rotation_instructions[3]], self.turn_library[rotation_instructions[0]], self.turn_library[rotation_instructions[1]], self.turn_library[rotation_instructions[2]]

    def sequence(self: RubiksCube, seq: str, verbose = False):
        for i, x in enumerate(seq):
            is_last: bool = (i == len(seq) - 1)
            move = "udfbrlxyz".find(x.lower())*3
            if not is_last:
                move += 1 * (seq[i+1] == "2")
                move += 2 * (seq[i+1] == "'")
            if x.lower() in "udfbrl":       
                self.turn(Turn(move), verbose=verbose)
            elif x.lower() in "xyz":
                self.rotate(Turn(move), verbose=verbose)



class C(Enum):
    WHITE = 0
    YELLOW = 1
    GREEN = 2
    BLUE = 3
    RED = 4
    ORANGE = 5

#edge id
class EP(Enum):
    WB = 0
    WR = 1
    WG = 2
    WO = 3
    YG = 4
    YR = 5
    YB = 6
    YO = 7
    GO = 8
    GR = 9
    BR = 10
    BO = 11

#corner id
class CP(Enum):
    WBO = 0
    WBR = 1
    WGR = 2
    WGO = 3
    YGO = 4
    YGR = 5
    YBR = 6
    YBO = 7

class Turn(Enum):
    U = 0
    U2 = 1
    U_ = 2
    D = 3
    D2 = 4
    D_ = 5
    F = 6
    F2 = 7
    F_ = 8
    B = 9
    B2 = 10
    B_ = 11
    R = 12
    R2 = 13
    R_ = 14
    L = 15
    L2 = 16
    L_ = 17

    X = 18
    X2 = 19
    X_ = 20
    Y = 21
    Y2 = 22
    Y_ = 23
    Z = 24
    Z2 = 25
    Z_ = 26

class Piece:
    def __init__(self, id: EP | CP, *stickers: list, rotation = 0):
        # clockwise, main is sticker on w/y, else g/b
        self.stickers: list[C] = stickers
        self.rotation: int = rotation
        self.id: EP | CP = id

class Corner(Piece):
    def __init__(self, id: EP | CP, *stickers: list):
        super().__init__(id, *stickers)
        self.size = 3

class Edge(Piece):
    def __init__(self, id: EP | CP, *stickers: list):
        super().__init__(id, *stickers)
        self.size = 2

if __name__ == "__main__":
    main()
    