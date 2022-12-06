# https://adventofcode.com/2022/day/1

# read it
with open('input.txt','r') as f: data = f.read()

# split it
data = data.split('\n\n')

# and split again 
rows = [row.split() for row in data]

# row totals
totals = [sum([int(i) for i in row]) for row in rows]

# part 1 answer
print(max(totals))

# part 2 answer
totals.sort()
print(sum(totals[-3:]))
