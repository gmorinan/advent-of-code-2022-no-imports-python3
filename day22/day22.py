# https://adventofcode.com/2022/day/22

with open('input.txt', 'r') as f:
    data = f.read().split('\n')

# manually parse input (who needs regex!)
turns = [idx for idx, char in enumerate(data[-2]) if char in ['L', 'R']]
pointer = 0
route = []
while turns:
    next_turn = turns.pop(0)
    route.append(data[-2][pointer:next_turn])
    route.append(data[-2][next_turn])
    pointer = next_turn + 1
route.append(data[-2][pointer:])

# pad board so every row has same width
board = data[:-3]
width = max([len(i) for i in board])
height = len(board)
board = [i + ' '*(width-len(i)) for i in board]

# map directions and turns
turning = {'R': {'E': 'S', 'S': 'W', 'W': 'N', 'N': 'E'},
           'L': {'E': 'N', 'S': 'E', 'W': 'S', 'N': 'W'}}
yx_map = {'E': (0, 1), 'S': (1, 0), 'W': (0, -1), 'N': (-1, 0)}
direction_value = {'E': 0, 'S': 1, 'W': 2, 'N': 3}


def starting_state():
    # creates initial state
    y0, x0 = (0, 50)
    direction = 'E'
    return y0, x0, direction


# these dict tells us how to wrap around the board
ywrap = {height: 0, -1: height-1}
xwrap = {width: 0, -1: width-1}


def next_pos_safe(y0, x0, yd, xd):
    # makes a single step, wrapping round if necessary
    y1, x1 = y0 + yd, x0 + xd
    y1 = ywrap.get(y1, y1)
    x1 = xwrap.get(x1, x1)
    return y1, x1


def final_score(y0, x0, direction):
    return ((1000*(y0+1)) + (4 * (x0+1)) + direction_value[direction])


def wrap_around_basic(y1, x1, yd, xd, next):
    # part 1 wrap around function
    while next == ' ':
        y1, x1 = next_pos_safe(y1, x1, yd, xd)
        next = board[y1][x1]
    return y1, x1, next


def wrap_around_cube(y1, x1, direction0):
    # part 2 wrap around function (relies on hardcoded cube_map)
    # fine the position and direction we end up at
    y1, x1, direction1 = cube_map[y1, x1, direction0]
    # update the deltas and next space
    yd, xd = yx_map[direction1]
    next = board[y1][x1]
    if next == '.':  # only update if its a free space
        direction0 = direction1
    return y1, x1, yd, xd, next, direction0

###################################
####### HARD CODED CUBE MAP ######
###################################


fr, to = [], []
# [2,0] -> [1,1]
fr.extend([(99, x, 'N') for x in range(0, 50)])
to.extend([(y, 50, 'E') for y in range(50, 100)])
# [2,0] <- [1,1]
fr.extend([(y, 49, 'W') for y in range(50, 100)])
to.extend([(100, x, 'S') for x in range(0, 50)])
# [3,0] -> [2,1]
fr.extend([(y, 50, 'E') for y in range(150, 200)])
to.extend([(149, x, 'N') for x in range(50, 100)])
# [3,0] <- [2,1]
fr.extend([(150, x, 'S') for x in range(50, 100)])
to.extend([(y, 49, 'W') for y in range(150, 200)])
# [1,1] -> [0,2]
fr.extend([(y, 100, 'E') for y in range(50, 100)])
to.extend([(49, x, 'N') for x in range(100, 150)])
# [1,1] <- [0,2]
fr.extend([(50, x, 'S') for x in range(100, 150)])
to.extend([(y, 99, 'W') for y in range(50, 100)])
# [2,1] -> [0,2] (REVERSED)
fr.extend([(y, 100, 'E') for y in range(100, 150)])
to.extend([(y, 149, 'W') for y in range(49, -1, -1)])
# [2,2] <- [0,2]
fr.extend([(y, 0, 'E') for y in range(0, 50)])
to.extend([(y, 99, 'W') for y in range(149, 99, -1)])
# [2,0] -> [0,1] (REVERSED)
fr.extend([(y, 149, 'W') for y in range(100, 150)])
to.extend([(y, 50, 'E') for y in range(49, -1, -1)])
# [2,0] <- [0,1]
fr.extend([(y, 49, 'W') for y in range(0, 50)])
to.extend([(y, 0, 'E') for y in range(149, 99, -1)])
# [3,0] -> [0,1]
fr.extend([(y, 149, 'W') for y in range(150, 200)])
to.extend([(0, x, 'S') for x in range(50, 100)])
# [3,0] <- [0,1]
fr.extend([(199, x, 'N') for x in range(50, 100)])
to.extend([(y, 0, 'E') for y in range(150, 200)])
# [3,0] -> [0,2]
fr.extend([(0, x, 'S') for x in range(0, 50)])
to.extend([(0, x, 'S') for x in range(100, 150)])
# [3,0] <- [0,2]
fr.extend([(199, x, 'N') for x in range(100, 150)])
to.extend([(199, x, 'N') for x in range(0, 50)])
# make the final map
cube_map = {f: t for f, t in zip(fr, to)}


# MAIN TASK
def tread_path(method='basic'):

    # create starting state
    y0, x0, direction = starting_state()

    # loop through route
    for step in route:

        if step.isdigit():  # if we've moving...
            yd, xd = yx_map[direction]  # the direction we're moving

            for n in range(int(step)):
                # next pos avoid edge of board
                y1, x1 = next_pos_safe(y0, x0, yd, xd)
                next = board[y1][x1]  # next space

                # if we need to wrap around
                if next == ' ':
                    if method == 'basic':  # part 1 method
                        y1, x1, next = wrap_around_basic(y1, x1, yd, xd, next)
                    else:  # part 2 method
                        y1, x1, yd, xd, next, direction = wrap_around_cube(
                            y1, x1, direction)

                if next == '.':  # if free, then move forward
                    y0, x0 = y1, x1
                elif next == '#':  # else we have to stop walking
                    break

        else:  # if we're turning
            direction = turning[step][direction]

    return final_score(y0, x0, direction)


# part 1 answer
print(tread_path(method='basic'))
# part 2 answer
print(tread_path(method='cube'))
