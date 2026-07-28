
from cube import RubiksCube, EP, CP, Turn

def main():
    cube: SmartCube = SmartCube()
    cube.sequence("U2 F' B2 U2 R2 D2 R2 D R2 D B2 D' R2 F2 B' L D R2 F R' F")

    cube.show()
    cube.cross()
    cube.show()

class SmartCube(RubiksCube):
    def __init__(self: SmartCube):
        super().__init__()
        self.color_order = ["W", "Y", "G", "B", "R", "O"]
        self.color_opposites = {"W": "Y", "Y": "W", "G": "B", "B": "G", "R": "O", "O": "R"}

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



if __name__ == "__main__":
    main()
