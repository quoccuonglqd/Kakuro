from __future__ import print_function
from ortools.linear_solver import pywraplp
from kakcommon import inputkakuro, Load_matrix

index = {}
inv_index = {}
cnt = 0

def make_index(mat):
	global cnt
	for i in range(len(mat)):
		for j in range(len(mat[i])):
			if (type(mat[i][j])==int):
				index[(i+1,j+1)] = cnt
				inv_index[cnt] = (i+1,j+1)
				cnt += 1

def solve_with_CBC(fileConstraint, fileBoard):
	(row_constraints, col_constraints), board, _ = inputkakuro(fileConstraint)
	matr = Load_matrix(fileBoard)
	print(matr)
	make_index(matr)
	solver = pywraplp.Solver('simple_mip_program',
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
	x = {}
	for i in range(cnt):
		for j in range(1,10):
			x[i*9+j] = solver.BoolVar('x[{}][{}][{}]'.format(inv_index[i][0],inv_index[i][1],j))
	print(index)
	for constraint in row_constraints:
		constraint_expr1 = []
		#---------------------
		for ind in constraint[2]:
			constraint_expr3 = []
			for j in range(1,10):
				constraint_expr1.append(j*x[index[(constraint[0],ind)]*9+j])
				constraint_expr3.append(x[index[(constraint[0],ind)]*9+j])
			solver.Add(sum(constraint_expr3) == 1)
		solver.Add(sum(constraint_expr1) == constraint[1])
		#----------------------
		for j in range(1,10):
			constraint_expr2 = []
			for ind in constraint[2]:
				constraint_expr2.append(x[index[(constraint[0],ind)]*9+j])
			solver.Add(sum(constraint_expr2) <= 1)
		

	for constraint in col_constraints:
		constraint_expr1 = []
		#---------------------
		for ind in constraint[2]:
			constraint_expr3 = []
			for j in range(1,10):
				constraint_expr1.append(j*x[index[(ind,constraint[0])]*9+j])
				constraint_expr3.append(x[index[(ind,constraint[0])]*9+j])
			solver.Add(sum(constraint_expr3) == 1)
		solver.Add(sum(constraint_expr1) == constraint[1])
		#----------------------
		for j in range(1,10):
			constraint_expr2 = []
			for ind in constraint[2]:
				constraint_expr2.append(x[index[(ind,constraint[0])]*9+j])
			solver.Add(sum(constraint_expr2) <= 1)

	objective = solver.Objective()
	for constraint in col_constraints:
		for ind in constraint[2]:
			for j in range(1,10):
				objective.SetCoefficient(x[index[(ind,constraint[0])]*9+j], 1)
	objective.SetMinimization()

	status = solver.Solve()
	if status == pywraplp.Solver.OPTIMAL:
		for i in range(cnt):
			for j in range(1,10):
				if x[i*9+j].solution_value() == 1.0:
					board.append([inv_index[i][0], inv_index[i][1], j])
	return board
