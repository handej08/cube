"""Run this file to simulate all methods, Ctrl+C to abort"""
from lblsolver import *

def main():
    run_sim()

def single_sim(scramble: str):
    names = ["LBL", "CFOP", "CFOP-4LLL", "REVERSE"]
    steps = ["CROSS", "F2L", "LL", "FULL"]
    lst = [[[] for __ in range(4)] for _ in range(4)]
    cube = SmartCube()
    
    lbl_moves = lössekvens(scramble)
    for j in range(4):
        lst[0][j].append(lbl_moves[j])
    cube.sequence(scramble)
    res = cube.solve(verbose=False)
    if not res[0]:
        exit()
    for j in range(4):
        lst[1][j].append(res[2][j])
    
    cube = SmartCube()
    cube.sequence(scramble)
    res = cube.solve(verbose=False, do_4lll=True)
    if not res[0]:
        exit()
    for j in range(4):
        lst[2][j].append(res[2][j])
    
    #rev scramble
    lst[3][3].append(cube.count_turns(scramble))

    for j, stat in enumerate(lst):
        print(f"\n\n\n# {names[j]}")
        for k, s in enumerate(stat):
            try:
                print(f"\n{steps[k]}: {s[0]}")
            except IndexError:
                continue


def run_sim():
    names = ["LBL", "CFOP", "CFOP-4LLL", "REVERSE"]
    steps = ["CROSS", "F2L", "LL", "FULL"]
    lst = [[[] for __ in range(4)] for _ in range(4)]
    i = 1
    try:
        while True:
            cube = SmartCube()
            scramble = cube.scramble()

            lbl_moves = lössekvens(scramble)
            for j in range(4):
                lst[0][j].append(lbl_moves[j])
            res = cube.solve(verbose=False)
            if not res[0]:
                exit()
            for j in range(4):
                lst[1][j].append(res[2][j])
    
            cube = SmartCube()
            cube.sequence(scramble)
            res = cube.solve(verbose=False, do_4lll=True)
            if not res[0]:
                exit()
            for j in range(4):
                lst[2][j].append(res[2][j])
    
            #rev scramble
            lst[3][3].append(cube.count_turns(scramble))
    
    
            print(i, end="\r")
            i += 1
    
    
    except KeyboardInterrupt:
        print(f"Solves: {i}")
        for j, stat in enumerate(lst):
            print(f"\n\n\n# {names[j]}")
            for k, s in enumerate(stat):
                try:
                    print(f"\n## {steps[k]}:\nMedian: {statistics.median(s)}\nMean: {statistics.mean(s)}\nQ1: {np.percentile(s, 25)}\nQ3: {np.percentile(s, 75)}\nMin: {min(s)}\nMax: {max(s)}")
                except statistics.StatisticsError:
                    continue
if __name__ == "__main__":
    main()