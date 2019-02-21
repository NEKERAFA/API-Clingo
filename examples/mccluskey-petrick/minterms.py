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

def solve(asp_program, asp_facts):
    c = clingo.Control()
    c.load("./asp/"+asp_program+".lp")
    for facts in asp_facts:
        c.add("base", [], facts)
    c.ground([("base", [])])
    ret = []
    with c.solve(yield_=True) as handle:
        for m in handle:
            ret = m.symbols(shown=True)
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

    # If the minimal coverage doesn't cover all minterms, petrick it
    if not any(sym.name == "fullcover" for sym in mincover_syms):
        petrick_syms = solve("petrick", [mincover_facts])
        petrick_facts = symbols_to_facts(petrick_syms)

    print(mincover_facts)
    print(petrick_facts)
    print("FINISHED")




if __name__ == "__main__":
    sys.settrace
    main()
