import argparse
import clingo
import re

steps = []
prime_implicants = {}
has_finished = False
mincover_total_coverage = False
essential_impls = []
petrick_impls = []
secondary_impls = []
petrick_total_coverage = False

def atom_name(idx, start):
    v = ord(start) + idx
    if v > ord('z'):
        v = ord('a') + (idx - (ord('z') - ord(start) + 1))
    return chr(v)

def parse_impl_id(impl):
    match = re.match('.*impl\((\d+)+,', impl)
    return match.group(1)

def implicants_to_asp(impls):
    asp_facts = ""
    for idx,imp in enumerate(impls.keys()):
        for m in imp.split(','):
            asp_facts += "impl({0}, {1}). ".format(idx, m)
    return asp_facts

def implicant_to_formula(impl):
    f_terms = []
    for term in impl:
        ft = ""
        a = term[0]
        v = term[1]
        if v == '0':
            ft += "not "
        if v != 'x':
            ft += a
            f_terms += [ ft ]
    return "(" + " ^ ".join(f_terms) + ")"

def input_to_asp(input_file):
    asp_facts = ""
    with open(input_file) as input_text:
        for line in input_text:
            if re.match('^[01x]+\s*$', line):
                m = line.strip()
                i = int(m, 2)
                for idx,bit in enumerate(m):
                    asp_facts += "m({0}, {1}, {2}). ".format(i, atom_name(idx, 'p'), bit)
                asp_facts += "\n"
    return asp_facts

def solve_mccluskey(asp_facts, clingo_args):
    cc = clingo.Control(clingo_args)
    cc.add("base", [], asp_facts)
    cc.load("./asp/pair-maker.lp")
    cc.ground([("base", [])])
    cc.solve(on_model=onmodel_mccluskey)

def solve_mincover(asp_facts, clingo_args):
    cc = clingo.Control(clingo_args)
    cc.add("base", [], asp_facts)
    cc.load("./asp/min-cover.lp")
    cc.ground([("base", [])])
    cc.solve(on_model=onmodel_mincover)

def solve_petrick(asp_facts, clingo_args):
    cc = clingo.Control(clingo_args)
    cc.add("base", [], asp_facts)
    cc.load("./asp/petrick.lp")
    cc.ground([("base", [])])
    cc.solve(on_model=onmodel_petrick)

def onmodel_mccluskey(m):
    global steps
    global has_finished
    global prime_implicants

    sol_facts = ""
    fin = False
    pr_impl = []
    for sym in m.symbols(shown=True):
        if sym.name == "nm":
            sol_facts += (str(sym).replace('nm', 'm') + '. ')
        elif sym.name == "pr_impl":
            sol_facts += (str(sym) + '. ')
            pr_impl += [ sym ]
        elif sym.name == "finished":
            fin = True
    steps += [ sol_facts ]
    if fin:
        has_finished = True
        for p in pr_impl:
            pid = str(p.arguments[0])
            pid_nums = list(map(int, re.findall(r'\d+', pid)))
            pid_nums.sort()
            pid = ",".join(list(map(str, pid_nums)))
            pnm = p.arguments[1].name
            pvl = str(p.arguments[2])
            if pid not in prime_implicants.keys():
                prime_implicants[pid] = []
            if (pnm, pvl) not in prime_implicants[pid]:
                prime_implicants[pid] += [(pnm, pvl)]

def onmodel_mincover(m):
    global mincover_total_coverage
    global petrick_impls
    global essential_impls

    for sym in m.symbols(shown=True):
        if sym.name == "total_coverage":
            mincover_total_coverage = True
        elif sym.name == "essn_impl":
            id = str(sym.arguments[0])
            im = str(sym.arguments[1])
            essential_impls += [ "impl({0}, {1}).".format(id, im) ]
        elif sym.name == "left_impl":
            id = str(sym.arguments[0])
            im = str(sym.arguments[1])
            petrick_impls += [ "impl({0}, {1}).".format(id, im) ]

def onmodel_petrick(m):
    global secondary_impls
    global petrick_total_coverage

    m_id = m.number-1
    secondary_impls += [[]]

    for sym in m.symbols(shown=True):
        if sym.name == "total_coverage":
            petrick_total_coverage = True
        elif sym.name == "selected_impl":
            id = str(sym.arguments[0])
            im = str(sym.arguments[1])
            secondary_impls[m_id] += [ "impl({0}, {1}).".format(id, im) ]

def prime_implicants_str(pm):
    res = ""
    for i,k in enumerate(pm.keys()):
        res += "[{0}] ".format(i)
        sm = pm[k]
        res += implicant_str(k, sm) + "\n"
    return res

def implicant_str(im, sm):
    res = im + ": "
    sm.sort()
    res += "".join([m[1] for m in sm])
    return res


def main():
    global steps
    global has_finished
    global prime_implicants
    global mincover_total_coverage
    global petrick_impls
    global essential_impls

    parser = argparse.ArgumentParser(description='Minterm reduction with ASP')
    parser.add_argument('input_sample', metavar='I', type=str,
                        help='route for the minterm text file')
    args = parser.parse_args()

    steps += [input_to_asp(args.input_sample)]
    current_step = 0
    while not has_finished:
        solve_mccluskey(steps[current_step], ["0"])
        current_step += 1

    print("PRIME IMPLICANTS:")
    print(prime_implicants_str(prime_implicants))

    solve_mincover(implicants_to_asp(prime_implicants), ["0"])

    essn_ids = []
    if len(essential_impls) > 0:
        print("ESSENTIAL IMPLICANTS:")
        for impl in essential_impls:
            id = parse_impl_id(impl)
            if int(id) not in essn_ids:
                essn_ids += [ int(id) ]
                keys = list(prime_implicants.keys())
                key = keys[int(id)]
                print("["+id+"] "+implicant_str(key, prime_implicants[key]))
    else:
        print("NO ESSENTIAL IMPLICANTS")

    if not mincover_total_coverage:
        print("\nSECONDARY IMPLICANTS:")
        solve_petrick(" ".join(petrick_impls), ["0"])
        print("There are {0} option(s) for the secondary implicants".format(len(secondary_impls)))
        for idx,sec in enumerate(secondary_impls):
            sec_ids = []
            print("OPTION {0}:".format(idx))
            for impl in sec:
                id = parse_impl_id(impl)
                if int(id) not in sec_ids:
                    sec_ids += [ int(id) ]
                    keys = list(prime_implicants.keys())
                    key = keys[int(id)]
                    print("["+id+"] "+implicant_str(key, prime_implicants[key]))

            formula_ids = essn_ids + sec_ids
            formula_ids.sort()
            min_formula_terms = []
            for fi in formula_ids:
                impkey = list(prime_implicants.keys())[int(fi)]
                min_formula_terms += [implicant_to_formula(prime_implicants[impkey])]
            print("\nF{0} = ".format(idx) + " v ".join(min_formula_terms) + "\n")
    else:
        formula_ids = essn_ids
        formula_ids.sort()
        min_formula_terms = []
        for fi in formula_ids:
            impkey = list(prime_implicants.keys())[int(fi)]
            min_formula_terms += [implicant_to_formula(prime_implicants[impkey])]
        print("\nF0 = " + " v ".join(min_formula_terms)+ "\n")




if __name__ == "__main__":
    main()
