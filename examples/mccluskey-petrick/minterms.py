import argparse
import clingo
import re
import sys

def atom_name(idx, start):
    v = ord(start) + idx
    if v > ord('z'):
        v = ord('a') + (idx - (ord('z') - ord(start) + 1))
    return chr(v)

def input_to_asp(input_file):
    asp_facts = ""
    with open(input_file) as input_text:
        for line in input_text:
            if re.match('^[01]+\s*$', line):
                m = line.strip()
                i = int(m.replace('x','0'), 2)
                for idx,bit in enumerate(m):
                    asp_facts += "m({0}, {1}, {2}). ".format(i, atom_name(idx, 'p'), bit)
                asp_facts += "\n"
    return asp_facts

def symbols_to_facts(symbols):
    return " ".join(["{0}.".format(sym) for sym in symbols])

def implicates_to_dict(symbols, prefix):
    impdict = {}
    for s in symbols:
        if s.name == (prefix+"impl"):
            k, a, v = s.arguments[0], s.arguments[1], s.arguments[2]
            if not k in impdict.keys():
                impdict[k] = { a: v }
            else:
                impdict[k][a] = v
    return impdict

def implicates_dict_str(impdict):
    ret = ""
    for i,k in enumerate(impdict.keys()):
        ret += "[{0}] {1}: ".format(i,k)
        for kk in sorted(impdict[k]):
            ret += str(impdict[k][kk])
        ret += "\n"
    return ret

def implicates_dict_formula(impdict):
    terms = []
    for k in impdict.keys():
        term = []
        for kk in sorted(impdict[k]):
            ts = ""
            v = str(impdict[k][kk])
            if v == "0":
                ts += "not "
            if v != "x":
                ts += str(kk)
                term += [ts]
        terms += ["(" + " ^ ".join(term) + ")"]
    return " v ".join(terms)

def solve(asp_program, asp_facts):
    c = clingo.Control(["0"])
    c.load("./asp/"+asp_program+".lp")
    for facts in asp_facts:
        c.add("base", [], facts)
    c.ground([("base", [])])
    ret = []
    with c.solve(yield_=True) as handle:
        for m in handle:
            ret += [m.symbols(shown=True)]
    return ret

def solve_iter(asp_program, asp_facts):
    c = clingo.Control()
    c.add("check", ["k"], "#external query(k).")
    c.load("./asp/"+asp_program+".lp")
    for facts in asp_facts:
        c.add("base", [], facts)

    t, ret = 0, []
    c.ground([("base", [])])
    while True:
        c.ground([("step", [t])])
        c.ground([("check", [t])])
        c.release_external(clingo.Function("query", [t-1]))
        c.assign_external(clingo.Function("query", [t]), True)
        # TODO: First call produces irrelevant info messages, look how to mute this
        with c.solve(yield_=True) as handle:
            for m in handle:
                ret = m.symbols(shown=True)
            if (handle.get().satisfiable):
                break
        t += 1
    return ret


def main():
    parser = argparse.ArgumentParser(description='Minterm reduction with ASP')
    parser.add_argument('input_sample', metavar='I', type=str,
                        help='route for the minterm text file')
    args = parser.parse_args()

    # Turn minterms into ASP facts
    input_facts = input_to_asp(args.input_sample)
    # Create the prime implicates
    primpl_syms = solve_iter("pair-maker", [input_facts])
    primpl_facts = symbols_to_facts(primpl_syms)

    # Perform minimal coverage for the prime implicates
    mincover_syms = solve_iter("min-cover", [input_facts, primpl_facts])
    mincover_facts = symbols_to_facts(mincover_syms)

    essndict, finaldicts = {}, []
    # If the minimal coverage doesn't cover all minterms, petrick it
    if not any(sym.name == "fullcover" for sym in mincover_syms):
        print("SECONDARY IMPLICATES")
        petrick_solutions = solve("petrick", [mincover_facts])
        for idx,petrick_syms in enumerate(petrick_solutions):
            petrick_facts = symbols_to_facts(petrick_syms)
            if any(sym.name == "selectimplid" for sym in petrick_syms):
                secdict = implicates_to_dict(petrick_syms, "select")
                finaldictasy = { **essndict, **secdict }
                finaldicts += [ finaldictasy ]
                print("SOLUTION #{0}".format(idx))
                print(implicates_dict_str(finaldictasy))
                print(implicates_dict_formula(finaldictasy) + "\n")
            else:
                print("NO SECONDARY IMPLICATES")
    else:
        print("ESSENTIAL IMPLICATES")
        essndict = implicates_to_dict(mincover_syms, "essn")
        print(implicates_dict_str(essndict))
        print(implicates_dict_formula(essndict))


if __name__ == "__main__":
    sys.settrace
    main()
