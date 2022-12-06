# https://adventofcode.com/2022/day/6

# read it
with open('input.txt','r') as f:
    data = f.read()

# generic function to find unique char substring
def get_len(input, chars=4):
    for i in range(len(input)):
        if len(set(input[i-chars:i]))==chars:
            return i

# apply same function twice
print(get_len(data, 4))
print(get_len(data, 14))