# https://adventofcode.com/2022/day/5

# read and split
with open('input.txt','r') as f:
    data = f.read().split('\n')

# from manual inspection we know the input is of two halves, with an empty link indicating the breakpoint
for idx, line in enumerate(data):
    if line=='':
        break_line = idx
        break

# top input indicating cargos
start = data[:break_line-1]
start = [row[1::4] for row in start] # we know key info is every 4 chars
# transpose your matrix - who needs numpy :D 
startT = [[start[j][i] for j in range(len(start))] for i in range(len(start[0]))]
# put it back together in a clean format, remove and trailing whitespace
start_clean = [''.join(row).strip() for row in startT]

# main dict to use for part 1
cargo_dict1 = {i+1:list(row) for i,row in enumerate(start_clean)}

# bottom input indicating instructions
moves = [[int(i) for i in row.split()[1::2]] for row in data[break_line+1:-1]]

# this does one row of instructions using single moving crane
def crane_single(input_dict, n, fr, to):
    for _ in range(n):
        box = input_dict[fr].pop(0)
        input_dict[to].insert(0, box) 

# apply single moves
[crane_single(cargo_dict1, n, fr, to) for n,fr,to in moves]

# part 1 answer
print(''.join([r[0] for r in cargo_dict1.values()]))

# start again from a new dict
cargo_dict2 = {i+1:list(row) for i,row in enumerate(start_clean)}

# this does one row of instructions using multi moving crane
def crane_multi(input_dict, n, fr, to):
    pick = input_dict[fr][:n] # pick up top n
    input_dict[fr] = input_dict[fr][n:] # what's left 
    input_dict[to] = pick + cargo_dict2[to] # add on

# apply multi moves
[crane_multi(cargo_dict2, n, fr, to) for n,fr,to in moves]

# part 2 answer
print(''.join([r[0] for r in cargo_dict2.values()]))