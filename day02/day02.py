# https://adventofcode.com/2022/day/2

#FIRST CODE: A for Rock, B for Paper, and C for Scissors
#PART 1 SECOND CODE: X for Rock, Y for Paper, and Z for Scissors
#PART 2 SECOND CODE: X for lose, Y for draw, and Z for win

# map codes to outcome score
res_map1 = {
    'A': {'X':3, 'Y':6, 'Z':0},
    'B': {'X':0, 'Y':3, 'Z':6},
    'C': {'X':6, 'Y':0, 'Z':3},
} # part 1
res_map2 = {
    'A': {'A':3, 'B':6, 'C':0},
    'B': {'A':0, 'B':3, 'C':6},
    'C': {'A':6, 'B':0, 'C':3},
} # part 2

# map moves to base score
base_map1 = {'X':1, 'Y':2, 'Z':3} # part 1
base_map2 = {'A':1, 'B':2, 'C':3} # part 2

# use this in part 2 to translate second code to move
translation_map = {
    'A': {'X':'C', 'Y':'A', 'Z':'B'},
    'B': {'X':'A', 'Y':'B', 'Z':'C'},
    'C': {'X':'B', 'Y':'C', 'Z':'A'},
}

#### ACTUAL CODE ####

# read it
with open('input.txt','r') as f:
    data = f.read()

# last row is a dud
rows = data.split('\n')[:-1]

# mystery instructions
codes1 = [row.split(' ') for row in rows]

# base score uses only second code in each line  
base1 = [base_map1[j] for i,j in codes1]

# result 1 used both codes
res1 = [res_map1[i][j] for i,j in codes1]

# put it all together
score1 = [b+r for b,r in zip(base1,res1)]

# part 1 answer
print(sum(score1))

# map second code to corect move
codes2 = [(i,translation_map[i][j]) for i,j in codes1]

# base score uses only second code in each line  
base2 = [base_map2[j] for i,j in codes2]

# result 1 used both codes
res2 = [res_map2[i][j] for i,j in codes2]

# put it all together
score2 = [b+r for b,r in zip(base2,res2)]

# part 2 answer
print(sum(score2))