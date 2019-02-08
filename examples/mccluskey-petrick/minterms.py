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

def solve_prime_implicates(asp_facts):
    current_step = 1
    mccluskey_sat = False
    while not mccluskey_sat:
        # Start with step = 1 and increment until we find a solution
        cc = clingo.Control(["-c", "maxsteps=" + str(current_step)])
        cc.load("./asp/pair-maker.lp")
        cc.add("base", [], asp_facts)
        cc.ground([("base", [])])
        with cc.solve(yield_=True) as handle:
            for m in handle:
                prime_implicates = m.symbols(shown=True)
            mccluskey_sat = (str(handle.get()) == "SAT")
            current_step += 1
    return prime_implicates

def main():
    parser = argparse.ArgumentParser(description='Minterm reduction with ASP')
    parser.add_argument('input_sample', metavar='I', type=str,
                        help='route for the minterm text file')
    args = parser.parse_args()

    # Turn minterms into ASP facts
    facts = input_to_asp(args.input_sample)
    primpl_syms = solve_prime_implicates(facts)

    # At this point we have the prime implicates under pr_impl_unique
    # and the minterms they cover under pr_impl_covers
    cc = clingo.Control(["0"])
    cc.load("./asp/rename.lp")
    for s in primpl_syms:
        cc.add("base", [], s)
    cc.ground([("base", [])])
    with cc.solve(yield_=True) as handle:
        for m in handle:
            print(m)

if __name__ == "__main__":
    sys.settrace
    main()
