from kaksolve import kaksolve
from kakcommon import *

convert_to_constraint('board.txt', 'test.txt')
answer = kaksolve('test.txt')
print(answer)
