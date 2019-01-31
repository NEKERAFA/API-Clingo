import argparse
import clingo
import re

def input_to_asp(input_file):
    asp_facts = ""
    with open(input_file) as input_text:
        line_list = list(input_text)
        head, body = line_list[:1], line_list[1:]
        size = int(head[0])
        asp_facts += "size({0}).\n".format(size)
        for idx,line in enumerate(body):
            if re.match('^[.01]+\s*$', line):
                m = line.strip()
                for jdx,bit in enumerate(m):
                    if bit == "0":
                        bitname = "w"
                    elif bit == "1":
                        bitname = "b"
                    if bit != ".":
                        asp_facts += "tile({0}, {1}, {2}). ".format(idx+1, jdx+1, bitname)
                asp_facts += "\n"
    return size, asp_facts

def solution_to_array(m, size):
    solution = [[-1 for i in range(size)] for j in range(size)]
    for sym in m.symbols(shown=True):
        if sym.name == "tile":
            x,y,c = sym.arguments[0].number, sym.arguments[1].number, str(sym.arguments[2])
            if c == "w":
                solution[x-1][y-1] = 0
            elif c == "b":
                solution[x-1][y-1] = 1
    return solution

def pretty_board(board):
    retstr = ""
    for row in board:
        for tile in row:
            if tile == 0:
                retstr += u"\u25C7" + " "
            else:
                retstr += u"\u25C6" + " "
        retstr += "\n"
    return retstr

def main():
    parser = argparse.ArgumentParser(description='Solve some binarios')
    parser.add_argument('input_program', metavar='I', type=str,
                        help='route for the binario puzzle instance')
    parser.add_argument('-n','--num_sols', metavar='N', type=int, default=1,
                        help='number of solutions requested, only one is provided by default. 0 means "all the solutions"')
    parser.add_argument('-s','--stats', action='store_true',
                        help='print solver stats')

    args = parser.parse_args()

    size,facts = input_to_asp(args.input_program)
    cc = clingo.Control([args.num_sols])
    cc.load("./asp/takuzu.lp")
    cc.add("base", [], facts)
    cc.ground([("base", [])])
    solutions = []
    with cc.solve(yield_=True) as handle:
        for m in handle:
            board = solution_to_array(m, size)
            solutions += [board]
            print("SOLUTION #{0}:".format(m.number))
            print(pretty_board(board))

    if args.stats:
        print("STATISTICS")
        print("----------")
        stats = cc.statistics
        sm = stats['summary']
        models = sm['models']
        lp = stats["problem"]["lp"]
        print("MODELS: {0}".format(int(models['enumerated'])))
        print("GROUND:")
        print("  ATOMS: {0}".format(int(lp["atoms"])))
        print("  RULES: {0}".format(int(lp["rules"])))
        print("  BODIES: {0}".format(int(lp["bodies"])))
        print("  EQUIVALENCES: {0}".format(int(lp["eqs"])))
        print("    EQ ATOM: {0}".format(int(lp["eqs_atom"])))
        print("    EQ BODY: {0}".format(int(lp["eqs_body"])))
        print("    EQ OTHER: {0}".format(int(lp["eqs_other"])))
        print("TIMES:")
        times = sm['times']
        print("  TOTAL: {0} / CPU: {1} / SOLVE: {2} \n  UNSAT: {3} / SAT: {4} ".format(
            times['total'], times['cpu'], times['solve'], times['unsat'], times['sat']))

if __name__ == "__main__":
    main()
