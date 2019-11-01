# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 08:13:32 2017

Formulates sudoku as a CSP, solving the riddle from
https://www.sudoku.ws/hard-1.htm as an example.

@author: stdm
@modif: tugg
"""

import sys
sys.path.append("./python-constraint-1.2")
import constraint as csp

# ------------------------------------------------------------------------------
# sudoku to solve (add "0" where no number is given)
# ------------------------------------------------------------------------------
riddle = [[0, 0, 0, 2, 0, 0, 0, 6, 3],
             [3, 0, 0, 0, 0, 5, 4, 0, 1],
             [0, 0, 1, 0, 0, 3, 9, 8, 0],
             [0, 0, 0, 0, 0, 0, 0, 9, 0],
             [0, 0, 0, 5, 3, 8, 0, 0, 0],
             [0, 3, 0, 0, 0, 0, 0, 0, 0],
             [0, 2, 6, 3, 0, 0, 5, 0, 0],
             [5, 0, 3, 7, 0, 0, 0, 0, 8],
             [4, 7, 0, 0, 0, 1, 0, 0, 0]]

# ------------------------------------------------------------------------------
# create helpful lists of variable names
# ------------------------------------------------------------------------------
rownames = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
colnames = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

rows = []
for i in rownames:
    row = []
    for j in colnames:
        row.append(i+j)
    rows.append(row)

cols = []
for j in colnames:
    col = []
    for i in rownames:
        col.append(i+j)
    cols.append(col)

boxes = []
for x in range(3):  # over rows of boxes
    for y in range(3):  # over columns of boxes
        box = []
        for i in range(3):  # over variables in rows (in a box)
            for j in range(3):  # over variables in cols (in a box)
                box.append(rownames[x*3 + i] + colnames[y*3 + j])
        boxes.append(box)

domains = [x for x in range(1, 10)]


print('rows: ', rows)
print('cols: ', cols)
print('boxes: ', boxes)
print('domains: ', domains)

# ------------------------------------------------------------------------------
# formulate sudoku as CSP
# ------------------------------------------------------------------------------
sudoku = csp.Problem()

# sudoku.addVariables(cols[1], domains)
# sudoku.addConstraint(csp.AllDifferentConstraint())
# sol = sudoku.getSolutions()
# print(sol)
# print("len: ", len(sol))

[sudoku.addVariables(col, domains) for col in cols]

for col in cols:
    sudoku.addConstraint(csp.AllDifferentConstraint(), col)

for row in rows:
    sudoku.addConstraint(csp.AllDifferentConstraint(), row)

for box in boxes:
    sudoku.addConstraint(csp.AllDifferentConstraint(), box)

length = range(len(riddle))

for i in length:
    for j in length:
        if riddle[i][j] != 0:
            sudoku.addConstraint(lambda var, value=riddle[i][j]:
                                 var == value, [rows[i][j]])

# ------------------------------------------------------------------------------
# solve CSP
# ------------------------------------------------------------------------------

solutions = sudoku.getSolutions()
if len(solutions) > 0:
    solution = solutions[0]
    for row in rows:
        print([solution[i] for i in row])



# solutions = sudoku.getSolutions()
# print(len(solutions))

# D = 7 # number of devices
# L = 3 # number of locations
#
# maxdev = [3,4,2]
# allowed = [[1,3,7],[1,3,4,5,6,7],[2,4,5,6]]
#
# problem = csp.Problem()
# problem.addVariables(["x_L%d_d%d" %(loc+1,d+1) for loc in range(L) for d in range(D) if d+1 in allowed[loc]],[0,1])
# for loc in range(L):
#     problem.addConstraint(csp.MaxSumConstraint(maxdev[loc]),["x_L%d_d%d" %(loc+1,d+1) for d in range(D) if d+1 in allowed[loc]])
# for d in range(D):
#     problem.addConstraint(csp.ExactSumConstraint(1),["x_L%d_d%d" %(loc+1,d+1) for loc in range(L) if d+1 in allowed[loc]])
#
# S = problem.getSolutions()
# print("sol: ", S)
# n = len(S)
# print("size: ", n)


# problem = csp.Problem()
# problem.addVariables([x for x in range(17)], [x for x in range(1, 17)])
# problem.addConstraint(csp.AllDifferentConstraint(), range(0, 16))
# problem.addConstraint(csp.ExactSumConstraint(34), [0,5,10,15])
# problem.addConstraint(csp.ExactSumConstraint(34), [3,6,9,12])
# for row in range(4):
#     problem.addConstraint(csp.ExactSumConstraint(34),
#                           [row*4+i for i in range(4)])
# for col in range(4):
#     problem.addConstraint(csp.ExactSumConstraint(34),
#                           [col+4*i for i in range(4)])
# solutions = problem.getSolutions()
# print(solutions)

# problem = csp.Problem()

# problem.addVariable('x', [1,2,3])
# problem.addVariable('y', [x for x in range(10)])
#
# def our_constraint(x, y):
#     if x + y >= 5:
#         return True
#
# problem.addConstraint(our_constraint, ['x','y'])
#
# solutions = problem.getSolutions()
#
# # Easier way to print and see all solutions
# # for solution in solutions:
# print(solutions)
#
# # Prettier way to print and see all solutions
# length = len(solutions)
# print("(x,y) ∈ {", end="")
# for index, solution in enumerate(solutions):
#     if index == length - 1:
#         print("({},{})".format(solution['x'], solution['y']), end="")
#     else:
#         print("({},{}),".format(solution['x'], solution['y']), end="")
# print("}")

# sudoku.addConstraint(csp.AllDifferentConstraint(), cols)
# sudoku.addConstraint(csp.AllDifferentConstraint(), rows)
# sudoku.addConstraint(csp.AllDifferentConstraint(), boxes)


# problem = csp.Problem()
# problem.addVariables(["a", "b"], [1, 2, 3])
# problem.addConstraint(csp.AllDifferentConstraint())
# print("---------------")
# print(problem.getSolutions())





