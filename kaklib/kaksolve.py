from kaklib.kakcommon import *
bo = 1
def kaksolve(file):
   (conds, board, dummy) = inputkakuro(file)
   kakuro(conds, board)
   return bo


def kakuro(conds, board):
   rowc, colc = conds[0], conds[1]
   if rowc == [] and colc == []:
      #soutboard(board)
      global bo
      bo = board
      return

   (ri,rl) = locatebest(rowc)
   (cj,cl) = locatebest(colc)
   if rl <= cl: 
      (cond,conds[0]) = extract(ri, rowc)
      kind = 'row'
   else:
      (cond,conds[1]) = extract(cj, colc)
      kind = 'col'

   i1, sum, cells, constraints = unpac4(cond)
   nc = len(cells)
   alts = permexpand(splitint(sum, nc, 
             difflist(list(range(1,10)), constraints)))

   for alt in alts:
      tryalt(alt, nc, cells, i1, kind, 
             treecopy(conds), treecopy(board))
   return

def tryalt(alt, nc, cells, i1, kind, conds, board):
   ok = True
   for ii in range(nc):
      (ok, conds, board) = okfill(alt[ii], cells[ii], 
                                  i1, kind, conds, board)
      if not ok: break
   if ok:
      kakuro(conds, board)
   return
 