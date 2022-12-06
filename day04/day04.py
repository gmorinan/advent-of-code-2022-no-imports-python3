# https://adventofcode.com/2022/day/4

# read and split
with open('input.txt','r') as f:
    data = f.read().split()
rows = [i.split(',') for i in data]

# start/end values for each row
rngs = []
for t1,t2 in rows:
    lo1, up1 = (int(i) for i in t1.split('-'))
    lo2, up2 = (int(i) for i in t2.split('-'))
    rngs.append(((lo1, up1), (lo2, up2)))

# function for part 1
def fully_contained(row):
    (lo1,up1), (lo2,up2) = row
    cond1 = (lo1>=lo2) & (up1<=up2)
    cond2 = (lo1<=lo2) & (up1>=up2)
    return cond1 | cond2

# apply function
contained = []
for idx, rng in enumerate(rngs):
    if fully_contained(rng):
        contained.append(idx)

# part 1 answer
print(len(contained))

# function for part 2
def not_overlap(row):
    cond1 = max(row[0]) < min(row[1])
    cond2 = max(row[1]) < min(row[0]) 
    return cond1 | cond2
    
# appl function
no_overlap = []
for idx, rng in enumerate(rngs):
    if not_overlap(rng):
        no_overlap.append(idx)

# part 2 answer
print(len(rngs) - len(no_overlap))