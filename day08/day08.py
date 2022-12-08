# read and initial process
with open('input8.txt','r') as f:
    data = f.read().strip().split('\n')
trees = [[int(char) for char in row] for row in data]
n = len(data)

# initially set all to invisible
vmat = [[False for _ in range(n)] for _ in range(n)]

# for each row
for i, row in enumerate(trees):
    # for each tree in that row
    for j, tree in enumerate(row):

        # outer ring condition
        if (i in [0, n-1]) | (j in [0, n-1]):
            vmat[i][j] = True
            continue # no need to check any others

        # check if visible from left
        if tree > max(row[:j]):
            vmat[i][j] = True
            continue

        # check if visible from right
        if tree > max(row[j+1:]):
            vmat[i][j] = True
            continue

        # check if visible from above
        if tree > max([trees[x][j] for x in range(i)]):
            vmat[i][j] = True
            continue

        # check if visible from below
        if tree > max([trees[x][j] for x in range(i+1, n)]):
            vmat[i][j] = True
            continue

# part 1 answer
print(sum([sum(row) for row in vmat]))

# initially set all to zero visibility
smat = [[0 for _ in range(n)] for _ in range(n)]

# function that given a tree and a list of neighbours
# (ordered closest to farthest) 
# returns the number that are seen
def how_many_seen(tree, tree_lst):
    if len(tree_lst)==0: # no trees no problem
        return 0
    for idx, check in enumerate(tree_lst):
        if check >= tree: # too big time to stop
            return idx + 1
    # if we get to this point we were able to see them all
    return len(tree_lst) 

# for each row
for i, row in enumerate(trees):
    # for each tree in the row
    for j, tree in enumerate(row):

        # get trees to left (reverse so closest first)
        to_left = row[:j][::-1]
        # get trees to right 
        to_right = row[j+1:]
        # get trees above (reverse so closest first)
        to_above = [trees[x][j] for x in range(i)][::-1]
        # get trees below
        to_below = [trees[x][j] for x in range(i+1, n)]

        # final score
        smat[i][j] = (
            how_many_seen(tree, to_left) * 
            how_many_seen(tree, to_right) * 
            how_many_seen(tree, to_above) *
            how_many_seen(tree, to_below)
        )

# part 2 answer
print(max([max(row) for row in smat]))