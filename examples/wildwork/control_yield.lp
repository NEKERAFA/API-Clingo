#script (python)
import clingo

def main(prg):
    prg.add("p", [], "{a;b;c}.")
    prg.ground([("p", [])])
    with prg.solve(yield_=True) as handle:
        for m in handle: print(m)
        print(handle.get())

#end.
