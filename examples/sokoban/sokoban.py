import argparse
import clingo
import re

solution = {}
solution["boards"] = {0: {"boxes": [], "walls": [], "start": [], "goals": []} }
solution["movements"] = []

def onmodel(m):
    for sym in m.symbols(shown=True):
        if sym.name == "height":
            solution["height"] = sym.arguments[0].number
        elif sym.name == "width":
            solution["width"] = sym.arguments[0].number
        elif sym.name == "box_start":
            solution["boards"][0]["boxes"] += [(sym.arguments[1].number, sym.arguments[2].number)]
        elif sym.name == "wall":
            solution["boards"][0]["walls"] += [(sym.arguments[0].number, sym.arguments[1].number)]
        elif sym.name == "start":
            solution["boards"][0]["start"] += [(sym.arguments[0].number, sym.arguments[1].number)]
        elif sym.name == "goal":
            solution["boards"][0]["goals"] += [(sym.arguments[0].number, sym.arguments[1].number)]
        elif sym.name == "move_dir":
            solution["movements"] += [(str(sym.arguments[0].name), sym.arguments[1].number)]
        elif sym.name == "player_on":
            solution["boards"][sym.arguments[2]]
    solution["movements"].sort(key=lambda y: y[1])
    solution["movements"] = [x[0] for x in solution["movements"]]


def solve(file_route, clingo_args):
    cc = clingo.Control(clingo_args)
    cc.load(file_route)
    cc.load("./sokoban.lp")
    cc.ground([("base", [])])
    cc.solve(on_model=onmodel)

def main():
    parser = argparse.ArgumentParser(description='Solve some sokobanes')
    parser.add_argument('input_program', metavar='I', type=str,
                        help='route for the sokoban instance')
    parser.add_argument('-S', '--steps', metavar='S', type=int,
                        help='maximum number of steps, defaults to the value specified on the instance')
    args = parser.parse_args()

    clingo_args = ["1"]

    if args.steps != None:
        clingo_args += ["-c", "max=" + str(args.steps)]

    solve(args.input_program, clingo_args)

    if len(solution["movements"]) > 0:
        board = [["·" for x in range(solution["width"]+1)] for y in range(solution["height"]+1)]

        for box in solution["boards"][0]["boxes"]:
            board[box[0]][box[1]] = "#"

        for wall in solution["boards"][0]["walls"]:
            board[wall[0]][wall[1]] = "X"

        for start in solution["boards"][0]["start"]:
            board[start[0]][start[1]] = "O"

        for goal in solution["boards"][0]["goals"]:
            board[goal[0]][goal[1]] = "*"

        board_str = ""
        for row in board:
            for cell in row:
                board_str += cell + " "
            board_str += "\n"

        print (board_str)
        print ("SOLUTION:")
        print (" -> ".join(solution["movements"]))
    else:
        print ("NO SOLUTION, MAYBE MORE MAX STEPS?")


if __name__ == "__main__":
    main()
