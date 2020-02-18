import random
import numpy as np
def chunk(l, n):
    return list(map(np.ndarray.tolist, np.array_split(l, n)))
def find(board, target):
    for x, i in enumerate(board):
        for y, j in enumerate(i):
            if j==target:
                return x, y
def check(board, size=0, target=None, checked=[], even=True):
    if size==0:
        size=len(board)
    if target is None:
        for x, i in enumerate(board):
            for y, j in enumerate(i):
                if j not in checked:
                    even=check(board, size, board[x][y], checked, even=not even)
        # if even:
            # board[0][0]=board[0][1]
        return even
    else:
        if target in checked:
            return even
        x, y=find(board, target)
        checked.append(target)
        check(board, size, board[x][y], checked, even=not even)
def create(size, clean=False):
    board=list(range(1,size**2+1))
    if not clean:
        random.shuffle(board)
    board=chunk(board, size)
    # check(board)
    return board
def print_board(board):
    zeros=len(str(len(board)**2))
    for i in board:
        for j in i:
            current=str(j)
            print(' '*(zeros-len(current))+current, end=' ')
        print()
def from_file(filename):
    with open(filename, 'r') as f:
        l=[]
        for i in f.readlines():
            l.append(list(map(int, i.split())))
        return l
if __name__=='__main__':
    print_board(from_file('8p.txt'))