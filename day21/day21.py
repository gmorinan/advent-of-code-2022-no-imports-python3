# https://adventofcode.com/2022/day/21

with open('input.txt', 'r') as f:
    data = f.read().strip().split('\n')


def parse_input(data):  # parse data
    rows = [r.split(': ') for r in data]
    return {a: b.split() for a, b in rows}


def eval_cell(x):  # recursive eval
    # x is either a str or a list
    if type(x) == list:
        # if single length list, call this function on the first element
        if len(x) == 1:
            return eval_cell(x[0])
        # if longer list, call this function on each element
        else:
            return [eval_cell(y) for y in x]
    # if a str digit or arithmetic operator, just leave it as is
    elif x.isdigit() | (x in ('*', '+', '/', '-', '=')):
        return x
    # else it is a str references another monkey, so we
    # get the words of that monkey from the dict and
    # eval each item
    else:
        monkeval[x] = [eval_cell(y) for y in monkeval[x]]
        return monkeval[x]


def convert_eq_to_str(mystr):
    # we end up with lists of lists, so we can convert to round
    # bracked and remove uncessary , and ` so we can eval it
    return (str(mystr)
            .replace('[', '(')
            .replace(']', ')')
            .replace(',', '')
            .replace("'", ''))


def full_eval(mystr):  # we eval a properly formatted equation string
    return eval(convert_eq_to_str(mystr))


# make input dict
monkeval = parse_input(data)
# run recursive eval
monkeval = {k: eval_cell(v) for k, v in monkeval.items()}
# part 1 answer
print(int(full_eval(monkeval['root'])))


# reset input dict
monkeval = parse_input(data)
dummy = '44444444'  # first trick: replace human with a number that doens't appear elsewhere
monkeval['humn'] = [dummy]
# run recursive eval (we know our dummy number will remain)
monkeval = {k: eval_cell(v) for k, v in monkeval.items()}

# second trick: replace dummy number with a complex number
eq1 = convert_eq_to_str(monkeval['root'][0]).replace('44444444', '-1j')
eq2 = convert_eq_to_str(monkeval['root'][2])

# now we evaluate
eq = eq1 + ' - ' + eq2
c = eval(eq)

# part 2 answer
print(int(round(c.real / c.imag, 0)))
