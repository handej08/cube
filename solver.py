
from cube import RubiksCube, EP, CP, Turn

def main():
    cube: SmartCube = SmartCube()
    cube.sequence("D' L R2 B2 L2 B2 R' U2 R U2 F2 U2 D F U' L' B F D' R'")
    #cube.sequence("L' D L")

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

        """self.f2l_relatives: dict[tuple[list[EP | CP]]] = {
            "G": ([EP.YB, EP.YO, EP.YG, EP.YR, EP.GR, EP.GO, EP.BO, EP.BR], [CP.YBR, CP.YBO, CP.YGO, CP.YGR, CP.WGR, CP.WGO, CP.WBO, CP.WBR]),
            "O": ([EP.YR, EP.YB, EP.YO, EP.YG, EP.GR, EP.GO, EP.BO, EP.BR])
            "B": [],
            "R": []
        }"""

        self.f2l_relatives : list[list[EP | CP]] = [[EP.YB, EP.YO, EP.YG, EP.YR, EP.GR, EP.GO, EP.BO, EP.BR], [CP.YBR, CP.YBO, CP.YGO, CP.YGR, CP.WGR, CP.WGO, CP.WBO, CP.WBR]]

        self.f2l_library: dict[tuple] = {
            (5, 0, 5, 0): "",

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
        }

    def find_piece(self: SmartCube, variety: int, piece: EP | CP) -> tuple:
        for i, p in enumerate(self.cube[variety]):
            if p.id == piece:
                return (EP(i), p) if variety == 0 else (CP(i), p)

    def face_cycle(self, rotation_instructions):
        super().face_cycle(rotation_instructions)
        self.color_order[rotation_instructions[0]], self.color_order[rotation_instructions[1]], self.color_order[rotation_instructions[2]], self.color_order[rotation_instructions[3]] = self.color_order[rotation_instructions[3]], self.color_order[rotation_instructions[0]], self.color_order[rotation_instructions[1]], self.color_order[rotation_instructions[2]]
             
    def cross_score(self: SmartCube) -> tuple:
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
        

    def cross(self: SmartCube):
        while True:
            cross_pieces, scores = self.cross_score()
            if min(scores) == 10:
                break
            target = min(range(len(scores)), key=scores.__getitem__)
            target_piece = cross_pieces[target]
            match scores[target]:
                case 1:
                    if max(scores) < 10:
                        while self.find_piece(0, target_piece[1].id)[0] != target_piece[1].id:
                            self.turn(Turn.U, verbose=True)
                    else:
                        self.turn(Turn[f"{target_piece[0].name[1]}2"], verbose=True)
                case 2:
                    while self.find_piece(0, target_piece[1].id)[0].name[1] != target_piece[1].id.name[1]:
                        self.turn(Turn.D, verbose=True)
                    self.turn(Turn(self.color_order.index(target_piece[1].id.name[1])*3+1), verbose=True)

                case 3:
                    side_color: str = target_piece[0].name[int(not bool(target_piece[1].rotation))]
                    piece_to_replace: EP = self.cube[0][target_piece[1].id.value].id
                    rotations = 0
                    while self.find_piece(0, piece_to_replace)[0].name[1] != side_color:
                        self.turn(Turn.U, verbose=True)
                        rotations = (rotations + 1) % 4
                    while self.find_piece(0, target_piece[1].id)[0].name[0] != "W":
                        self.turn(Turn(self.color_order.index(side_color)*3), verbose=True)
                    for _ in range(rotations):
                        self.turn(Turn.U_, verbose=True)

                case 4:
                    
                    while self.find_piece(0, target_piece[1].id)[0].name[1] == target_piece[1].id.name[1] or self.find_piece(0, target_piece[1].id)[0].name[1] == self.color_opposites[target_piece[1].id.name[1]]:
                        self.turn(Turn.D, verbose=True)
                    side: Turn = Turn(self.color_order.index(self.find_piece(0, target_piece[1].id)[0].name[1])*3)
                    while target_piece[1].id.name[1] not in self.find_piece(0, target_piece[1].id)[0].name:
                        self.turn(side, verbose=True)
                    while self.find_piece(0, target_piece[1].id)[0] != target_piece[1].id:
                        self.turn(Turn(self.color_order.index(target_piece[1].id.name[1])*3), verbose=True)



                case 5:
                    side_color: str = target_piece[0].name[1]
                    self.turn(Turn(self.color_order.index(side_color)*3), verbose=True)

    def f2l(self: SmartCube):
        self.rotate(Turn.Z2, verbose=True)
        for side in self.f2l_order:
            for _ in range(4):
                try:
                    edge: tuple = self.find_piece(0, self.f2l_sides[side][0])
                    corner: tuple = self.find_piece(1, self.f2l_sides[side][1])
                    #print(f"..{edge[0]}")
                    edge_state: tuple = (self.f2l_relatives[0].index(edge[0]), edge[1].rotation)
                    corner_state: tuple = (self.f2l_relatives[1].index(corner[0]), corner[1].rotation)
                    print("e: ", *edge_state, " c: ", *corner_state)
                    
                    #major minor offset
                    if not bool(self.f2l_sides[side][2]):
                        print("changing due to offset")
                        edge_state: tuple = (self.f2l_relatives[0].index(edge[0]), int(not bool(edge_state[1])))

                    state: tuple[int] = (*edge_state, *corner_state)

                    print("e: ", *edge_state, " c: ", *corner_state)
            
                    
                    self.sequence(self.f2l_library[state], verbose=True)
                    print("Solving")
                    break
                except KeyError:
                    self.turn(Turn.U, verbose=True)

            #rotate to next
            self.sequence("y", verbose=True)
            #change relatives
            for relatives in self.f2l_relatives:
                relatives[0], relatives[1], relatives[2], relatives[3], relatives[4], relatives[5], relatives[6], relatives[7] = relatives[3], relatives[0], relatives[1], relatives[2], relatives[5], relatives[6], relatives[7], relatives[4]



if __name__ == "__main__":
    main()
