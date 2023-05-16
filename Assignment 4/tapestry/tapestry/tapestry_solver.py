from clause import *

"""
For the tapestry problem, the only code you have to do is in this file.

You should replace

# your code here

by a code generating a list of clauses modeling the queen problem
for the input file.

You should build clauses using the Clause class defined in clause.py

Read the comment on top of clause.py to see how this works.
"""


def get_expression(size, fixed_cells=None):

    expression = []

    # Create a clause for each fixed cell
    if fixed_cells:
        for (i, j), (k, l) in fixed_cells.items():
            clause = Clause(size)
            for s in range(size):
                for c in range(size):
                    if (s, c) == (k, l):
                        clause.add_positive(i, j, s, c)
                    else:
                        clause.add_negative(i, j, s, c)
            expression.append(clause)

    # Create a clause for each cell that cannot have a specific shape and color
    for i in range(size):
        for j in range(size):
            for s in range(size):
                for c in range(size):
                    if fixed_cells and (i, j) in fixed_cells and (s, c) == fixed_cells[(i, j)]:
                        # skip fixed cells
                        continue
                    clause = Clause(size)
                    clause.add_negative(i, j, s, c)
                    expression.append(clause)

    # Create a clause for each row that must contain all shapes and colors
    for i in range(size):
        for s in range(size):
            clause = Clause(size)
            for j in range(size):
                for c in range(size):
                    if (j, c) == (i, s):
                        clause.add_positive(j, c, s, c)
                    else:
                        clause.add_negative(j, c, s, c)
            expression.append(clause)

    # Create a clause for each column that must contain all shapes and colors
    for j in range(size):
        for c in range(size):
            clause = Clause(size)
            for i in range(size):
                for s in range(size):
                    if (i, s) == (j, c):
                        clause.add_positive(i, s, c, s)
                    else:
                        clause.add_negative(i, s, c, s)
            expression.append(clause)

    return expression



if __name__ == '__main__':
    expression = get_expression(3)
    for clause in expression:
        print(clause)
