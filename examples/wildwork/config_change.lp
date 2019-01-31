#script (python)
import clingo

def main(prg):
    prg.configuration.solve.models = 0
    prg.ground([("base", [])])
    prg.solve()

#end.

{a; c}.
