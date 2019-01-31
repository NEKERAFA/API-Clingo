#script (python)
import clingo

def main(prg):
    prg.add("p", [], "{a;b;c}.")
    prg.ground([("p", [])])
    ret = prg.solve()
    print(ret)

#end.
