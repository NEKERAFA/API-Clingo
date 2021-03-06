import argparse
import clingo
import re
import sys
import subprocess

def input_to_asp(input_file):
    asp_facts = ""
    onset = True
    with open(input_file) as input_text:
        for line in input_text:
            if re.match('^[01x-]+\s*$', line):
                m = line.strip().replace('-', 'x')
                i = int(m.replace('x', '2'), 3)
                if (not onset):
                    asp_facts += "dcid({0}). ".format(i)
                for idx,bit in enumerate(m):
                    asp_facts += "m({0}, {1}, {2}). ".format(i, "x"+str(idx), bit)
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
            ret += str(impdict[k][kk]).replace('x', '-')
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

    # Perform minimal coverage for the prime implicates
    mincover_syms = solve_iter("min-cover", [primpl_facts])
    mincover_facts = symbols_to_facts(mincover_syms)

    essndict, finaldicts = {}, []
    essndict = implicates_to_dict(mincover_syms, "essn")
    print("ESSENTIAL IMPLICATES")
    print(implicates_dict_str(essndict))
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
                print("OPTION #{0}".format(idx))
                print("SECONDARY IMPLICATES")
                print(implicates_dict_str(secdict))

    # If more than one possible solution, obtain minimal formulae
    # Depends on the specified minimization mode, some of them require an asprin call
    if len(finaldicts) == 1:
        print("MINIMIZED FORMULA")
        print(implicates_dict_formula(finaldicts[0]))
    else:
        optmode, asprin, minimal_solutions = "", False, []
        print(optmode)
        if args.minmode == "atoms":
            print("Minimizing formulae by shorter terms")
            optmode = "less-atoms"
        elif args.minmode == "terms":
            print("Minimizing formulae by less terms")
            optmode = "less-terms"
        elif args.minmode == "atoms-terms":
            print("Minimizing formulae by shorter terms and less atoms")
            optmode = "less-atoms-terms"
            asprin = True
        elif args.minmode == "subset":
            print("Minimizing formulae by subsets of terms")
            optmode = "less-subset"
            asprin = True
        elif args.minmode == "triplet":
            print("Minimizing formulae by subsets, shorter terms and less atoms")
            optmode = "less-atoms-terms-subset"
            asprin = True

        minimize_facts = ""
        for idx,impdict in enumerate(finaldicts):
            asp = "solution({0}). ".format(idx)
            for impl in impdict.keys():
                for v in impdict[impl].keys():
                    asp += "sol(impl({0},{1},{2}), {3}). ".format(impl, v, impdict[impl][v], idx)
            minimize_facts += asp

        if asprin:
            with open("./tmp/minfacts.lp", "w") as aspfile:
                aspfile.write(minimize_facts)
            if args.all:
                out = subprocess.check_output(["asprin", "asp/"+optmode+".lp", "tmp/minfacts.lp", "0"])
            else:
                out = subprocess.check_output(["asprin", "asp/"+optmode+".lp", "tmp/minfacts.lp"])
            strout = out.decode()
            answers = strout.split('Answer:')
            for ans in answers:
                if "OPTIMUM FOUND" in ans:
                    match = re.search(r'(\d)\n([\s\S]*)\nOPTIMUM FOUND', ans)
                    solno, preds = match.group(1), match.group(2)
                    preds = ". ".join(preds.split(" "))+"."
                    minimal_solutions += solve("", [preds], ["0"])
        else:
            if args.all:
                minimal_solutions = solve(optmode, [minimize_facts], ["--opt-mode=optN","-n0"])
                # The first solution appears two times, so drop it
                minimal_solutions = minimal_solutions[1:]
            else:
                minimal_solutions = solve(optmode, [minimize_facts], [])

        # Iterate and print minimized formulae
        for idx,sol in enumerate(minimal_solutions):
            seldict = implicates_to_dict(sol, "select")
            print("MINIMIZED FORMULA #{0}".format(idx))
            print(implicates_dict_formula(seldict) + "\n")

if __name__ == "__main__":
    sys.settrace
    main()
