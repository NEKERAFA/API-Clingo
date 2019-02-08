#script (python)
import clingo

def input_to_asp(input_file):
    asp_facts = ""
    with open(input_file) as input_text:
        line_list = list(input_text)
        head, body = line_list[:1], line_list[1:]
        size = int(head[0])
        asp_facts += "size({0}).\n".format(size)
        for idx,line in enumerate(body):
            if re.match('^[.01]+\s*$', line):
                m = line.strip()
                for jdx,bit in enumerate(m):
                    if bit == "0":
                        bitname = "w"
                    elif bit == "1":
                        bitname = "b"
                    if bit != ".":
                        asp_facts += "tile({0}, {1}, {2}). ".format(idx+1, jdx+1, bitname)
                asp_facts += "\n"
    return size, asp_facts

def main(prg):
    size,facts = input_to_asp("")
    cc.add("base", [], facts)
    cc.ground([("base", [])])
    with prg.solve(yield_=True) as handle:
        for m in handle: print(m)
        print(handle.get())

#end.
