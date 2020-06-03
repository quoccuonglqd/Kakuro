from shlex import shlex

def Load_matrix(path):
   with open(path) as f:
      lines = f.read()
      lines = lines.split('\n')
      for i in range(len(lines)):
         lines[i] = lines[i].split(' ')
         for j in range(len(lines[i])):
            if(',' in lines[i][j]):
               lines[i][j] = lines[i][j].split(',')
            else:
               lines[i][j] = int(lines[i][j])
   return lines


def getSolution(b, fileName):
   b1 = treecopy(b)
   mat = Load_matrix(fileName)
   print(mat)
   for cell in b1:
      i, j, val = cell
      mat[i][j] = val
   return mat

def convert_to_constraint(filename,newfile):
   mat = Load_matrix(filename)
   row = []
   col = []

   writefile = open(newfile,'w')

   m,n = len(mat),len(mat[0])
   for i in range(m):
      tmp = []
      for j in range (n):
         if type(mat[i][j])!=int:
            tmp.append(j)
      tmp.append(n)
      row.append(tmp)

   has_col = False

   for i in range(n):
      tmp = []
      for j in range (m):
         if type(mat[j][i])!=int:
            tmp.append(j)
      tmp.append(m)
      col.append(tmp)

   for i in range(m):
      if len(row[i])!=1:
         has_col = True
         for j in range(len(row[i])-1):
            if int(mat[i][row[i][j]][1])>0:
               writefile.write('r{} '.format(i+1))
               writefile.write('{} '.format(mat[i][row[i][j]][1]))
               writefile.write('{}:{}'.format(row[i][j]+2,row[i][j+1]))
               writefile.write('\n')

   for i in range(n):
      if len(col[i])!=1:
         for j in range(len(col[i])-1):
            if int(mat[col[i][j]][i][0])>0:
               writefile.write('c{} '.format(i+1))
               writefile.write('{} '.format(mat[col[i][j]][i][0]))
               writefile.write('{}:{}'.format(col[i][j]+2,col[i][j+1]))
               writefile.write('\n')
   writefile.write('.')
   writefile.close()

def Change_format(mat,newfile):
   row = []
   col = []

   writefile = open(newfile,'w')

   m,n = len(mat),len(mat[0])
   for i in range(m):
      tmp = []
      for j in range (n):
         if type(mat[i][j])!=int:
            tmp.append(j)
      tmp.append(n)
      row.append(tmp)

   has_col = False

   for i in range(n):
      tmp = []
      for j in range (m):
         if type(mat[j][i])!=int:
            tmp.append(j)
      tmp.append(m)
      col.append(tmp)

   for i in range(m):
      if len(row[i])!=1:
         has_col = True
         for j in range(len(row[i])-1):
            if int(mat[i][row[i][j]][1])>0:
               writefile.write('r{} '.format(i+1))
               writefile.write('{} '.format(mat[i][row[i][j]][1]))
               writefile.write('{}:{}'.format(row[i][j]+2,row[i][j+1]))
               writefile.write('\n')

   for i in range(n):
      if len(col[i])!=1:
         for j in range(len(col[i])-1):
            if int(mat[col[i][j]][i][0])>0:
               writefile.write('c{} '.format(i+1))
               writefile.write('{} '.format(mat[col[i][j]][i][0]))
               writefile.write('{}:{}'.format(col[i][j]+2,col[i][j+1]))
               writefile.write('\n')
   writefile.write('.')
   writefile.close()

def inputkakuro(filename):
   rowc,colc,board,evens = [],[],[],[]
# the variable 'evens' is used to collect "even" cells for
# solving parity kakuro puzzles.

   f = open(filename, 'r')
   while True:
      line = f.readline()
      if line[0] == '.':
         break
      tokens = list(shlex(line))
      if tokens == []: continue
      kind = tokens[0]
      if kind[0] == 'r':
         if len(kind) == 2:
            rowc.append(getcond(tokens, int(kind[1])))
         else:
            rowc.append(getcond(tokens, int(kind[1]+kind[2])))
      elif kind[0] == 'c':
         if len(kind) == 2:
            colc.append(getcond(tokens, int(kind[1])))
         else:
            colc.append(getcond(tokens, int(kind[1] + kind[2])))
      elif kind == 'b':
         cell = getcell(tokens)
         board.append(cell)
         (rowc,colc) = adjustconds(rowc,colc,cell)
      else: raise Exception('Input error')
   f.close()
   global m, n
   (m, n) = dimensions(rowc, colc, board, evens)
   return ([rowc,colc], board, evens)

def getcond(tokens, j):
   sum = int(tokens[1])
   d = int(tokens[2])
   cells = [d]
   if len(tokens) > 3:
      if tokens[3] == ':':
         for n in range(d+1, int(tokens[4])+1): cells.append(n)
      else:
         for ic in range(3, len(tokens)): 
            cells.append(int(tokens[ic]))
   return [j, sum, cells, []]

def getcell(token):
   if not (len(token) == 4): raise Exception('Input error')
   ri, rj, val = int(token[1]), int(token[2]), int(token[3])
   return [ri, rj, val]

def adjustconds(rowc, colc, cell): 
   i, j, val = cell[0], cell[1], cell[2]
   ci = locate(lambda l: l[0] == i and  j in l[2], rowc)
   if ci >= 0:
      i, sum, cells, constraints = unpac4(rowc[ci])
      cells.remove(j)
      rowc[ci] = [i, sum-val, cells, constraints+[val]]
   cj = locate(lambda l: l[0] == j and  i in l[2], colc)
   if cj >= 0:
      j, sum, cells, constraints = unpac4(colc[cj])
      cells.remove(i)
      colc[cj] = [j, sum-val, cells, constraints+[val]]
   return (rowc, colc)

# Functions used for output ------------------------------------------

def soutboard(b):
   b1 = treecopy(b)
   b1.sort()
   print("Solution:")
   i0, j0 = 0, 0
   for cell in b1:
      i, j, d = cell[0], cell[1], cell[2]
      if not i == i0: 
         print(' ', end='\n')
         print(i, ': ', end=' ')
         i0, j0 = i, 0
      for n in range(1,j-j0): print('  -', end=' ')
      print(' ',d, end=' ')
      j0 = j
   print(' ', end='\n')


def dimensions(rowc,colc,board,evens):
   mc = reduce(max, [cond[0] for cond in rowc], 0)
   nc = reduce(max, [cond[0] for cond in colc], 0)
   if board == []: mb,nb = 0,0
   else: 
      mb = reduce(max, [b[0] for b in board], 0)
      nb = reduce(max, [b[1] for b in board], 0)
   me = reduce(max, [e // 10 for e in evens], 0)
   ne = reduce(max, [e % 10 for e in evens], 0)
   return (max(mc,max(mb,me)), max(nc,max(nb,ne)))
         
def locatebest(conds):
   if conds == []: return (-1, 99)
   index, length = 0, len(conds[0][2])
   for i in range(1, len(conds)):
      if len(conds[i][2]) < length: 
         index, length = i, len(conds[i][2])
   return (index, length)
        
def okfill(val, cell, i1, kind, conds, board):
   if kind == 'row': 
      board = cappend(board, [i1, cell, val])
      pconds = conds[1]  # perpendicular conds
   else: 
      board = cappend(board, [cell, i1, val])
      pconds = conds[0]
   j = locate(lambda l: (l[0] == cell) and (i1 in l[2]), pconds)
   if j < 0: return (True, conds, board)
   (res, pconds) = adjustcond(j, pconds, val, i1)
   if not res: return (False, conds,board)
   if kind == 'row': conds[1] = pconds
   else:             conds[0] = pconds
   return (True, conds,board)

def adjustcond(j, pconds, val, i1):
   i2, sum, list, clist = unpac4(pconds[j]) 
   if val > sum or val in clist: return (False, pconds)
   if len(list)==1:   # no more cells in this condition
      (skip,pconds) = extract(j, pconds)
   else: 
      list.remove(i1)
      pconds[j] = [i2, sum-val, list, clist+[val]]
   return (True,pconds)


def find(e, list):
   for j in range(len(list)):
      if e == list[j]: return j
   return -1


def locate(p, list):
   for j in range(len(list)):
      if p(list[j]): return j
   return -1


def extract(j, l):
   return (l[j], l[:j] + l[j + 1:])


def unpac4(l): return (l[0], l[1], l[2], l[3])


def difflist(la, lb):
   for b in lb:
      la.remove(b)
   return la


def treecopy(t):
   if t == [] or not isinstance(t, list):
      return t
   else:
      return list(map(treecopy, t[:]))


def cappend(l, e):
   return l[:] + [e]


from functools import reduce


def ins(a, l):
   return ins1(a, [], l)


def ins1(a, pre, post):
   if post == []:
      return [pre + [a]]
   else:
      x, post1 = post[0], post[1:]
      return [pre + [a] + post] + ins1(a, pre + [x], post1)


def cat(x, y): return x + y


def perm(l):
   if len(l) == 1:
      return [l]
   else:
      x, l1 = l[0], l[1:]
      return reduce(cat, map(lambda p: ins(x, p), perm(l1)))


def permexpand(l):
   if len(l) == 0:
      return []
   else:
      x, l1 = l[0], l[1:]
      return perm(x) + permexpand(l1)

def prefixa(a, l):
   if len(l) == 0:
      return []
   else:
      x, l1 = l[0], l[1:]
      return [[a] + x] + prefixa(a, l1)

def singleton(l):
   if len(l) == 0:
      return []
   else:
      return [[l[0]]] + singleton(l[1:])

def sublists(l, n):
   m = len(l)
   if m == n:
      return [l]
   if n == 1:
      return singleton(l)
   else:
      x, l1 = l[0], l[1:]
      return prefixa(x, sublists(l1, n - 1)) + sublists(l1, n)

def splitint(s, n, termlist):
   return list(filter(lambda l: sum(l) == s, sublists(termlist, n)))