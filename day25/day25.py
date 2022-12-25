# https://adventofcode.com/2022/day/25

# read n split
with open('input25.txt', 'r') as f:
    data = f.read().strip().split('\n')

# for mapping to/from the snafu digits
snafu_decimal_map = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
decimal_snafu_map = {v: k for k, v in snafu_decimal_map.items()}


def pad_input(data):
    # pad leading zeroes
    n = max([len(d) for d in data])
    return ['0'*(n-len(d)) + d for d in data]


def mass_sum(data):
    # rearrange the input
    inputs = pad_input(data)
    n = len(inputs[0])
    sum_parts = {}
    for i in range(n):
        sum_parts[i] = [row[::-1][i] for row in inputs]
    return sum_parts


def sum_one_part(lst):
    # to sum up all parts
    return sum([snafu_decimal_map[d] for d in lst])


def resolve_snafu(indict):
    # main function to sum up snafu numbers
    ddict = indict.copy()
    for k in list(ddict.keys()):  # loop through each digit
        v = ddict[k]  # get latest amount
        if v != 0:
            sign = int(v / abs(v))  # record sign and apply later
            up = (abs(v) // 5)  # amount to send up to next
            rem = (abs(v) % 5)  # remainder to leave here
            if (rem == 3) | (rem == 4):  # 3/4 adds 1 to next but reduced here by 5
                rem -= 5
                up += 1
            ddict[k] = rem * sign  # record with sign
            up *= sign  # add with sign
            if (up > 0) | (up < 0):
                # needed in case we end up adding extra digits
                ddict[k+1] = up + ddict.get(k+1, 0)
    return {k: int(v) for k, v in ddict.items()}


# transform input
sum_parts = mass_sum(data)
decimal_sums = {k: sum_one_part(v) for k, v in sum_parts.items()}

# compute answer
snafu_resolved = resolve_snafu(decimal_sums)

# answer part 1
answer = ''.join([decimal_snafu_map[k]
                 for k in list(snafu_resolved.values())[::-1]])
print(answer)
# part 2 no further code needed!
