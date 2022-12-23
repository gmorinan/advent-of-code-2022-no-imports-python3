# https://adventofcode.com/2022/day/23

with open('input.txt', 'r') as f:
    data = f.read().strip().split('\n')

# which directions to look at
directions = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'W': (0, -1),
              'NE': (-1, 1), 'SE': (1, 1), 'NW': (-1, -1), 'SW': (1, -1)}
# they look in the 3 directions before moving
consider_trio = {'N': ('NW', 'N', 'NE'),
                 'S': ('SW', 'S', 'SE'),
                 'E': ('SE', 'E', 'NE'),
                 'W': ('SW', 'W', 'NW'), }


def propose_move(elf, consider):
    # checks where elf could move
    y, x = elf
    possible = {direction: (y+yd, x+xd)
                for direction, (yd, xd)
                in directions.items()
                if (y+yd, x+xd) not in elves
                }
    # no borders, just stay still
    if len(possible) == 8:
        return elf
    else:  # check our corder
        for to in consider:
            trio = consider_trio[to]
            if len(set(trio).intersection(possible)) == 3:
                return possible[to]
        else:  # none of them possible so stay still
            return elf


def validate_possible_moves(elves_consider):
    # set of all proposed move
    pos_count = {}
    for v in elves_consider.values():
        pos_count[v] = pos_count.get(v, 0) + 1
    return {k: (v if pos_count[v] == 1 else k) for (k, v) in elves_consider.items()}


def get_bounding_box(elves):
    # computes final space
    yvals = [y for y, x in elves]
    xvals = [x for y, x in elves]
    y_min, y_max = min(yvals), max(yvals)
    x_min, x_max = min(xvals), max(xvals)
    area = (y_max - y_min + 1) * (x_max - x_min + 1)
    n_elves = len(elves)
    return area, n_elves, area - n_elves, (y_min, y_max), (x_min, x_max)


def starting_state():
    # starting position
    elves = set()
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == '#':
                elves.add((y, x))
    # this rotates each round
    consider = ['N', 'S', 'W', 'E']
    return elves, consider


def single_round(elves, consider):
    # executes 1 round of movement
    elves_consider = {elf: propose_move(elf, consider) for elf in elves}
    elves_next = validate_possible_moves(elves_consider)
    elves = set(elves_next.values())
    consider = consider[1:] + [consider[0]]
    return elves, consider


# part 1 we initiate and do 10 loops, then count area
elves, consider = starting_state()
for _ in range(10):
    elves, consider = single_round(elves, consider)
# part 1 answer
print(get_bounding_box(elves)[2])


# part 2 we initiate and do a lot of loops, until state doens't change
elves, consider = starting_state()
for idx in range(10000):  # i chose 10000 because it takes < 1 min to run and if we don't find the answer in that time, probably best to try something else :D
    elves_next, consider = single_round(elves, consider)
    # if we've reached no changes report answer
    if len(elves_next.intersection(elves)) == len(elves):
        # part 2 answer
        print(idx+1)
        break
    else:  # else continue
        elves = elves_next
