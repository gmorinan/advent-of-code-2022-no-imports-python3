# https://adventofcode.com/2022/day/9

# read and initial process
with open('input.txt','r') as f:
    data = f.read().strip().split('\n')
# we just want a list of the 4 possible directions 
moves = [(d, int(i)) for d,i in [r.split(' ') for r in data]]
moves = ''.join([char*n for char,n in moves])

# updates for a single positional move move
def update_pos(P, off):
    Py, Px = P
    Oy, Ox = off
    return (Oy+Py, Ox+Px)

# main tail logic
def update_tail(T, H):

    # compute offsets
    off_row = H[0] - T[0]
    off_col = H[1] - T[1]

    # tail is next to head
    if (abs(off_row)<=1) & (abs(off_col)<=1): return T

    # apply diag if both are non-zero
    elif (off_row!=0) and (off_col!=0):
        diag_move = 1 if off_row>0 else -1, 1 if off_col>0 else -1
        return update_pos(T, diag_move)

    # otherwise its just along a single axis
    else: 
        direction = (
            ('U' if off_row > 0 else 'D') # row needs to move
                if off_row!=0 else 
            ('R' if off_col > 0 else 'L') # column needs to move
            )
        return update_pos(T, dmap[direction])

# map directions to coordinates
dmap = {'L':(0,-1), 'R':(0,1), 'U':(1,0), 'D':(-1,0)}


#### ORIGINAL ANSWER TO PART 1 ####
# H, T = (0,0), (0,0)
# tail_history, head_history = [H], [T]
# for move in moves:
#     H = update_pos(H, dmap[move])
#     T = update_tail(T, H)
#     head_history.append(H)
#     tail_history.append(T)
# print(len(set(tail_history)))

#### SCALABLE ANSWER #####
def solver(n=2):
    # starting position 
    old_rope = tuple([(0,0) for _ in range(n)]) # (Head, Tail1, Tail2, ...)
    history = [old_rope] # track history

    for move in moves: 
        new_rope = [] # to store new rope position
        new_rope.append(update_pos(old_rope[0], dmap[move])) # new head
        for idx in range(1, n): # iteratively update each tail
            new_rope.append(update_tail(old_rope[idx], new_rope[idx-1]))
        history.append(tuple(new_rope)) # save history
        old_rope = new_rope # update pointer

    return len(set([t[-1] for t in history]))

# answer to part 1
print(solver(2))

# answer to part 2
print(solver(10))