import stuff
def copy(board):
    b=[]
    for i in board:
        b.append(i[:])
    return b
def abs(n):
    return n if n>=0 else -n
def find(board, lead):
    for x_index, row in enumerate(board):
        for y_index, col in enumerate(row):
            if col==lead:
                return x_index, y_index
    raise ValueError
def reverse(move):
    if move=='R':
        return 'L'
    if move=='L':
        return 'R'
    if move=='U':
        return 'D'
    if move=='D':
        return 'U'
class node:
    def __init__(self, state, parent=None, move="", lead_x=None, lead_y=None):
        self.parent=parent
        self.state=state
        self.g=0
        self.h=0
        self.f=0
        if lead_x==None:
            self.lead_x, self.lead_y=find(self.state, len(self.state)**2)
        else:
            self.lead_x, self.lead_y=lead_x, lead_y
        self.move=move
    def eq(self, other, pieces):
        size=len(self.state)
        for i in range(size):
            for j in range(size):
                if self.state[i][j] in pieces and self.state[i][j]!=other.state[i][j]:
                    return False
        return True
    def __str__(self):
        return self.move
    def distance(self, pieces):
        size=len(self.state)
        dist=0
        for x, i in enumerate(self.state):
            for y, j in enumerate(i):
                if j not in pieces:
                    continue
                cor_x=(j-1)//size
                cor_y=(j-1)%size
                dist+=abs(cor_x-x)+abs(cor_y-y)
        return dist
    def check_move(self, move):
        if self.parent is not None or self.parent.move==reverse(move):
            return False
        size=len(self.state)
        if move=='R':
            return self.lead_y!=size-1
        elif move=='L':
            return self.lead_y!=0
        elif move=='U':
            return self.lead_x!=0
        elif move=='D':
            return self.lead_x!=size-1
        else:
            raise ValueError
    def apply_move(self, move):
        board=copy(self.state)
        x, y=self.lead_x, self.lead_y
        if move=='R':
            board[x][y], board[x][y+1]=board[x][y+1], board[x][y]
            return board, x, y+1
        elif move=='L':
            board[x][y], board[x][y-1]=board[x][y-1], board[x][y]
            return board, x, y-1
        elif move=='U':
            board[x][y], board[x-1][y]=board[x-1][y], board[x][y]
            return board, x-1, y
        elif move=='D':
            board[x][y], board[x+1][y]=board[x+1][y], board[x][y]
            return board, x+1, y
        else:
            raise ValueError
# def output(current_node):
#     path=[]
#     current=current_node
#     while current is not None:
#         path.append(current.move)
#         last=current
#         current=current.parent
#     return ' '.join(path[::-1][1:]), last.state
def search(board, target):
    print('target:', target)
    size=len(board)
    start_node=node(board, None)
    start_node.g=start_node.h=start_node.f=0
    end_node=node(stuff.create(size, clean=True), None)
    end_node.g=end_node.h=end_node.f=0
    open_list=[]
    closed_list=[]
    open_list.append(start_node)

    while len(open_list)>0:
        current_node=open_list[0]
        current_index=0
        for index, item in enumerate(open_list):
            if item.f<current_node.f:
                current_node=item
                current_index=index
        open_list.pop(current_index)
        closed_list.append(current_node)
        if current_node.eq(end_node, pieces=target):
            path=[]
            current=current_node
            while current is not None:
                path.append(current.move)
                current=current.parent

            return ' '.join(path[::-1][1:]), current_node.state
        
        children=[]
        for nextmove in ['R', 'U', 'L', 'D']:
            if not current_node.check_move(nextmove):
                continue
            new_state, new_x, new_y=current_node.apply_move(nextmove)
            new_node=node(new_state, current_node, nextmove, new_x, new_y)
            for closed_child in closed_list:
                if closed_child==new_node:
                    break
            else:
                children.append(new_node)

            for child in children:
                child.g=current_node.g+1
                child.h=child.distance(pieces=target)
                child.f=child.h+child.g

                for open_node in open_list:
                    if child==open_node and child.g>open_node.g:
                        break
                else:
                    open_list.append(child)

if __name__=='__main__':
    print('phase0')
    try:
        sol, board=search(stuff.from_file('8p.txt'), target=[1,2,3])
    except KeyboardInterrupt:
        sol, board=search(stuff.from_file('8p.txt'), target=[1,4,7])
    print(sol)
    print('phase1')
    sol1, board1=search(board, target=[1,2,3,4,7])
    print(sol1)
    print('phase2')
    sol2, board2=search(board1, target=[1,2,3,4,5,6,7,8])
    print(sol2)