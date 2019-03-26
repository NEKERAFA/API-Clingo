import argparse
import re

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

def main():
    parser = argparse.ArgumentParser(description='Minterm reduction with ASP')
    parser.add_argument('input_sample', metavar='I', type=str,
                        help='route for the minterm text file')
    args = parser.parse_args()

    # Turn minterms into ASP facts
    input_facts = input_to_asp(args.input_sample)

    print(input_facts)

if __name__ == "__main__":
    main()
