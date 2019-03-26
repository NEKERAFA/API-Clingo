import argparse
import clingo
import re
import sys
import subprocess

def atom_name(idx, start):
    v = ord(start) + idx
    if v > ord('z'):
        v = ord('a') + (idx - (ord('z') - ord(start) + 1))
    return chr(v)

def input_to_asp(input_file):
    asp_facts = ""
    onset = True
    with open(input_file) as input_text:
        for line in input_text:
            if re.match('^[01x]+\s*$', line):
                m = line.strip()
                i = int(m.replace('x', '0'), 2)
                if (not onset):
                    asp_facts += "dcid({0}). ".format(i)
                for idx,bit in enumerate(m):
                    asp_facts += "m({0}, {1}, {2}). ".format(i, atom_name(idx, 'p'), bit)
                asp_facts += "\n"
            elif re.match('^d\s*$', line):
                onset = False
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

def solve(asp_program, asp_facts, clingo_args):
    c = clingo.Control(clingo_args)
    if asp_program != "":
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
    prg = clingo.Control([])
    prg.add("check", ["k"], "#external query(k).")
    prg.load("./asp/"+asp_program+".lp")
    for f in asp_facts:
        prg.add("base", [], f)

    step, handle, ret = 0, None, []
    while ( step == 0 or not handle.get().satisfiable ):
        parts = []
        parts.append(("check", [step]))
        if step > 0:
            prg.release_external(clingo.Function("query", [step-1]))
            parts.append(("step", [step]))
            prg.cleanup()
        else:
            parts.append(("base", []))
        prg.ground(parts)
        prg.assign_external(clingo.Function("query", [step]), True)
        step += 1
        handle = prg.solve(yield_=True)
        for m in handle:
            ret = m.symbols(shown=True)
    return ret


def main():
    parser = argparse.ArgumentParser(description='Minterm reduction with ASP')
    parser.add_argument('input_sample', metavar='I', type=str,
                        help='route for the minterm text file')
    parser.add_argument('-m','--minmode', default="triplet",
                    choices=['atoms', 'terms', 'atoms-terms', 'subset', 'triplet'],
                    help='formulae minimization method')
    parser.add_argument('-a', '--all', action='store_true', default=False,
                    help='enumerate all optimal models')
    args = parser.parse_args()

    # Turn minterms into ASP facts
    input_facts = input_to_asp(args.input_sample)

    # Create the prime implicates
    primpl_syms = solve_iter("pair-maker", [input_facts])
    primpl_facts = symbols_to_facts(primpl_syms)

    print(primpl_facts)

    #essndict = {}
    #essndict = implicates_to_dict(primpl_syms, "upr")
    #print("PRIME IMPLICATES")
    #print(implicates_dict_str(essndict))

if __name__ == "__main__":
    sys.settrace
    main()
