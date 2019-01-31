#script (python)
import clingo

def on_model(model):
    print(model)

def on_finish(res):
    print(res)

def main(prg):
    prg.add("p", [], "{a;b;c}.")
    prg.ground([("base", [])])
    with prg.solve(on_model=on_model, on_finish=on_finish, async=True) as handle:
        while not handle.wait(0):
            # do something asynchronously
            pass
        print(handle.get())

#end.
