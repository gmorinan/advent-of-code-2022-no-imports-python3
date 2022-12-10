# https://adventofcode.com/2022/day/10

# read n split
with open('input.txt','r') as f:
    data = f.read().strip().split('\n')

# values start at 1
X = [1]
for row in data: # for each instruction
    X.append(X[-1]) # you always have 1 cycle repeating the last value
    if row != 'noop': # and if its an addx you add a new value
        X.append(X[-1] + int(row.split(' ')[-1]))

# compute signal strengths
strengths = [X[c-1] * c for c in range(20, 221, 40)]

# part 1 answer
print(sum(strengths))

# initiate the 6x40 resolution screen with dots
screen = [['.'] * 40 for _ in range(6)]

# for each value
for idx, val in enumerate(X):
    crt_row = idx // 40 # which row we are on
    crt_col = idx % 40 # which pixel on that row
    if abs(val - crt_col) <= 1: # only change if we are in range
        screen[crt_row][crt_col] = '#' 

# part 2 answer 
print('\n'.join([''.join(row) for row in screen]))