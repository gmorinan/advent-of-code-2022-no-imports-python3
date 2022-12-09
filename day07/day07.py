# https://adventofcode.com/2022/day/7

# read it
with open('input.txt','r') as f:
    data = f.read()

# we want to split by list commands
data_split = data.split('$ ls')

# in row_split we have two elements
# first is the list of all files and dirs
# second is all the navigation commands that happen
row_split = []
for row in data_split:
    for idx, char in enumerate(row):
        if char=='$':
            row_split.append((row[:idx], row[idx:]))
            break
    else:
        row_split.append((row, []))
            
# note that the previous row_split is out of sync
# i.e. the list relates to the navigation of the previous line
# so we match up the two lines
dir_contents = []
for r0, r1 in zip(row_split[:-1], row_split[1:]):
    dir_contents.append((r0[1], r1[0]))

# given the output of the list command...
# this returns two elements, first is list of dirs, second is total filesize
def get_folder_contents(instr):
    objs = [i.split(' ') for i in instr.split('\n') if len(i)>0]
    dirs = []
    files = 0
    for o in objs:
        if o[0]=='dir': 
            dirs.append(o[1])
        else:
            files += int(o[0])
    return dirs, files

# given the long string containing 1+ navigation commands
# this returns list of individual navigation commands with the $ cd removed
def parse_file_nav(instr):
    cmds = [i for i in instr.split('\n') if len(i)>0]
    for cmd in cmds:
        assert cmd[:5] == '$ cd '
    return [c.replace('$ cd ','') for c in cmds]

# apply both thes functions
dir_parsed = [(parse_file_nav(nav), get_folder_contents(contents)) for nav,contents in dir_contents]

# apply the a nav commands to track folder we are in
def switch_dir(current, cmds):
    for cmd in cmds:
        if cmd == '/':
            current = '/'
            return current
        elif cmd == '..':
            current = '/'.join(current.split('/')[:-2]) + '/'
        else:
            current += cmd + '/'
    return current

# replace lists of commands with actual folder 
current = ''
dirs_full = {}
for cmd, content in dir_parsed:
    current = switch_dir(current, cmd)
    dirs_full[current] = content[1]

# we now have a dict with full file path and contents for each folder
# now we just want to sort into alphabetical order for ease of 
# examination and debugging
all_paths = list(dirs_full.keys())
all_paths.sort()
dirs_sorted = {p:dirs_full[p] for p in all_paths}

# now let's get the sum of contents with an O(n2) loop :(
dirs_sums = {}
for dir1, fsize1 in dirs_sorted.items():
    n = len(dir1)
    size = fsize1
    # for each dir we check all other dirts
    for dir2, fisze2 in dirs_sorted.items():
        # this conditional tells us if we're looking at a child dir
        if (dir2[:n] == dir1) & (len(dir2) > n):
            # if so add that filesize
            size += fisze2
    dirs_sums[dir1] = size

# now we sum up all the dirs which have <100000 size
total_fsize = 0
for dir, size in dirs_sums.items():
    if size <= 100000:
        total_fsize += size

# part 1 answer
print(total_fsize) 

# 70000000 total space
# 30000000 needed
# this is how much we need to remove:
target = int(3e7 - (7e7 - dirs_sums['/']))

# we want to find the dir that is greater than this
# by the smallest amount

# initiate huge value and best dir being the root
best_save = 1e12
best_dir = '/'

# now loop through all dirs
for dir, size in dirs_sums.items():
    # see what the delta is
    delta = size - target
    # only continue if this dir is greater than the size we need to delete
    if delta < 0: continue
    # we want the delta to be as close to zero while being positive
    if delta < best_save: 
        best_save = delta
        best_dir = dir

# part 2 answer
print(dirs_sums[best_dir])