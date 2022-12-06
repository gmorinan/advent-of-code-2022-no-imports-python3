# https://adventofcode.com/2022/day/3

# read n split 
with open('input.txt','r') as f:
    data = f.read().split()

# f(letter) = value
def get_letter_val(x):
    offset = 38 if x.upper() == x else 96
    return ord(x) - offset

# process rucksacks
rucks = []
for row in data:
    n = int(len(row)/2)
    rucks.append([row[:n], row[n:]])

# advanced set theory
same = []
for r1, r2 in rucks:
    the_same = list(set(r1).intersection(r2))
    same.append(the_same[0])

# part 1 answer
print(sum([get_letter_val(i) for i in same]))

# some "group" theory
badges = []
n_groups = int(len(data)/3) 
for i in range(n_groups): # for each group
    group = data[(i*3):(i+1)*3]
    a,b,c = group # say hi to the group
    badge = list(set(a).intersection(set(b)).intersection(set(c)))
    badges.append(badge[0]) # should always be exactly 1 intersection

# part 2 answer 
print(sum([get_letter_val(i) for i in badges]))