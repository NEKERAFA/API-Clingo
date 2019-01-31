import clingo as cln

def print_tree(ast):
    print(str(ast))

program =   """
                p :- not p.
            """

cln.parse_program(program, print_tree)
