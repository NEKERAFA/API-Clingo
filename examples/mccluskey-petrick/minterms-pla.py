import argparse
import clingo
import re
import sys
import subprocess
from pyeda.parsing import pla

def input_to_asp(input_dict):
    asp_facts = [""] * int(input_dict['noutputs'])
    for minterm, output in input_dict['cover']:
        for jdx, out_fun in enumerate(output):
            facts = ""
            if out_fun == 1:
                sign = "on"
            else:
                sign = "off"
            m = "".join(str(x-1) for x in minterm)
            i = int(m, 3)
            m = m.replace("2", "x")
            for idx, bit in enumerate(m):
                facts += "{0}({1}, {2}, {3}). ".format(sign, i,
                    input_dict['input_labels'][idx], bit)
            asp_facts[jdx] += facts + "\n"
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
            ret += str(impdict[k][kk]).replace('x', '-')
        ret += "\n"
    return ret

def output_dict_pla(odict, idict):
    ostr = ""
    ostr += ".i {0}\n".format(idict['ninputs'])
    ostr += ".o {0}\n".format(idict['noutputs'])
    ostr += ".ilb {0}\n".format(" ".join(idict['input_labels']))
    ostr += ".ob {0}\n".format(" ".join(idict['output_labels']))
    ostr += ".p {0}\n".format(len(odict.keys()))
    for k,v in odict.items():
        ostr += "{0} {1}\n".format(k, "".join(v))
    ostr += ".e"
    return ostr


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
    parser.add_argument('file', nargs='?', type=argparse.FileType('r'),
                        default=sys.stdin, help="PLA file (default: stdin)")
    parser.add_argument('-m','--minmode', default="terms",
                    choices=['atoms', 'terms'],
                    help='formulae minimization method')
    args = parser.parse_args()

    try:
        input_dict = pla.parse(args.file.read())
    except pla.Error as exc:
        print("error parsing file:", args.file.name)
        print(exc)
        return 1

    # Turn minterms into ASP facts
    input_facts = input_to_asp(input_dict)

    # Create the prime implicates
    outputs = []
    for outno in range(input_dict['noutputs']):
        primpl_syms = solve_iter("pair-maker-onoff", [input_facts[outno]])
        primpl_facts = symbols_to_facts(primpl_syms)

        # Perform minimal coverage for the prime implicates
        mincover_syms = solve_iter("min-cover", [primpl_facts])
        mincover_facts = symbols_to_facts(mincover_syms)

        essndict, finaldicts = {}, []
        essndict = implicates_to_dict(mincover_syms, "essn")
        # If the minimal coverage doesn't cover all minterms, petrick it
        if any(sym.name == "fullcover" for sym in mincover_syms):
            finaldicts += [ essndict ]
        else:
            petrick_solutions = solve("petrick", [mincover_facts], ["0"])
            for idx,petrick_syms in enumerate(petrick_solutions):
                petrick_facts = symbols_to_facts(petrick_syms)
                if any(sym.name == "selectimplid" for sym in petrick_syms):
                    secdict = implicates_to_dict(petrick_syms, "select")
                    finaldictasy = { **essndict, **secdict }
                    finaldicts += [ finaldictasy ]

        # If more than one possible solution, obtain minimal formulae
        # Depends on the specified minimization mode, some of them require an asprin call
        if len(finaldicts) == 1:
            outputs += [ essndict ]
        else:
            optmode, asprin, minimal_solutions = "", False, []
            if args.minmode == "atoms":
                optmode = "less-atoms"
            elif args.minmode == "terms":
                optmode = "less-terms"

            minimize_facts = ""
            for idx,impdict in enumerate(finaldicts):
                asp = "solution({0}). ".format(idx)
                for impl in impdict.keys():
                    for v in impdict[impl].keys():
                        asp += "sol(impl({0},{1},{2}), {3}). ".format(impl, v, impdict[impl][v], idx)
                minimize_facts += asp

            minimal_solutions = solve(optmode, [minimize_facts], [])
            mindict =  implicates_to_dict(minimal_solutions[0], "select")
            outputs += [mindict]

    pladict = {}
    for idx,o in enumerate(outputs):
        for k,v in o.items():
            val = ""
            for kk in sorted(o[k]):
                val += str(o[k][kk]).replace('x','-')
            print(val)
            if not val in pladict.keys():
                pladict.update({val: ["0"]*len(outputs)})
            pladict[val][idx] = "1"

    print(output_dict_pla(pladict, input_dict))

if __name__ == "__main__":
    sys.settrace
    main()
