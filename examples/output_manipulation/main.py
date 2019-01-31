import clingo

cc = clingo.Control([])
cc.load("./simple.lp")
solution = cc.solve()

print(str(solution))
