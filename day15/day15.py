# https://adventofcode.com/2022/day/15

# read n split
with open('input.txt', 'r') as f:
    data = f.read().strip().split('\n')

# manually parse the strings to get x,y coords


def get_coords(row):
    str_sensor, str_beacon = row.split(':')
    x_idx_sensor = str_sensor.find('x=')
    y_idx_sensor = str_sensor.find('y=')
    x_idx_beacon = str_beacon.find('x=')
    y_idx_beacon = str_beacon.find('y=')
    x_sensor = int(str_sensor[x_idx_sensor+2:y_idx_sensor-2])
    y_sensor = int(str_sensor[y_idx_sensor+2:])
    x_beacon = int(str_beacon[x_idx_beacon+2:y_idx_beacon-2])
    y_beacon = int(str_beacon[y_idx_beacon+2:])
    return (x_sensor, y_sensor), (x_beacon, y_beacon)

# manhattan distnace function


def manhat_d(c1, c2):
    x1, y1 = c1
    x2, y2 = c2
    return abs(x1-x2) + abs(y1-y2)

# function checks to see if no beacons are possible on this space


def test_no_beacon(test, sensors, beacons, distances):
    if test in beacons:
        return False
    for sensor, dist in zip(sensors, distances):
        if manhat_d(test, sensor) <= dist:
            return True
    return False


# apply co-ord function and get the sensors and beacons
pairs = [get_coords(row) for row in data]
sensors = [p[0] for p in pairs]
beacons = set([p[1] for p in pairs])
distances = [manhat_d(c1, c2) for c1, c2 in pairs]

# compute bounds of what we need
min_x = min([x for x, _ in sensors])
max_x = max([x for x, _ in sensors])
min_y = min([y for _, y in sensors])
max_y = max([y for _, y in sensors])
max_d = max(distances)
start_x = min_x - max_d - 1
end_x = max_x + max_d + 1

# we check for every possible x value where y=2000000
flags = []
for idx, test_x in enumerate(range(start_x, end_x+1)):
    # flag is a boolean where True indicates no beacon
    flag = test_no_beacon((test_x, 2000000), sensors, beacons, distances)
    flags.append(flag)  #  append bool

# part 1 answer is just number of Trues
print(sum(flags))

# gets x interval, given x value, distance and y_offset


def get_x_interval(x, d, y_offset):
    return x - (d-y_offset), x + (d-y_offset)

# are two intervals overlapping - used to merge lists


def is_overlaping(a, b):
    if b[0] >= a[0] and b[0] <= a[1]:
        return True
    else:
        return False

# used to merge several intervals


def merge(arr):
    arr.sort()  # always sort first
    merged_list = []
    merged_list.append(arr[0])
    for i in range(1, len(arr)):
        pop_element = merged_list.pop()
        if is_overlaping(pop_element, arr[i]):  #  if overalpping we merge
            new_element = pop_element[0], max(pop_element[1], arr[i][1])
            merged_list.append(new_element)
        else:  # otherwise we just add the new element
            merged_list.append(pop_element)
            merged_list.append(arr[i])
    return merged_list

# gets interval(s) of possible x values for a given y row


def get_x_intervals(sensors, distances, yrow):
    x_intervals = []  # store x_intervals that are possibly overlappying
    for (x, y), dist in zip(sensors, distances):
        y_offset = abs(yrow - y)
        if y_offset <= dist:  # if y_offset > dist the interval is empty
            x_intervals.append(get_x_interval(x, dist, y_offset))

    # merge all the intervals, along with the start/end bounds
    x_intervals = merge([(0, 0)] + x_intervals + [(4000000, 4000000)])
    return x_intervals


# loop through all possible y_rows
res = []
for yrow in range(0, 4000000):
    # get x_interval interval(s) for this row
    x_ints = get_x_intervals(sensors, distances, yrow)
    # if it has gaps (i.e. more than 1 element) save it
    if len(x_ints) > 1:
        res.append((yrow, x_ints))

# we know the answer is for the 1 row where there's more than 1 x_interval
# i.e. there must be a gap inbewteen the two intervals, which is our result
y = res[0][0]  # yrow we found
x = res[0][1][1][0] - 1  # start of the last x_interval, minus 1
# part 2 answer
print(y+(x*4000000))
