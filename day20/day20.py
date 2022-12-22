# https://adventofcode.com/2022/day/20

# read and split
with open('input.txt', 'r') as f:
    data = f.read().strip().split('\n')


class Node:
    #  nodes in linked list
    def __init__(self, data, order):
        self.data = data
        self.next = None
        self.prev = None
        self.order = order


class CircularDoublyLinkedList:
    # main double headed linked list class
    def __init__(self):
        self.first = None

    def get_node_by_idx(self, index):
        # given an index returns node at that index
        current = self.first
        for i in range(index):
            current = current.next
        return current

    def get_node_by_value(self, value):
        # given a value returns that node and its idx
        current = self.first
        idx = 0
        while True:
            if current.data == value:
                return current, idx
            else:
                current = current.next
                idx += 1

    def get_node_by_order(self, order):
        # get node by order (different to index)
        current = self.first
        while True:
            if current.order == order:
                return current
            else:
                current = current.next

    def insert_after(self, ref_node, new_node):
        # put node after an existing one
        new_node.prev = ref_node
        new_node.next = ref_node.next
        new_node.next.prev = new_node
        ref_node.next = new_node

    def insert_before(self, ref_node, new_node):
        # put node before an existing
        self.insert_after(ref_node.prev, new_node)

    def insert_at_end(self, new_node):
        # pop it on the end
        if self.first is None:
            self.first = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            self.insert_after(self.first.prev, new_node)

    def insert_at_beg(self, new_node):
        # at the start
        self.insert_at_end(new_node)
        self.first = new_node

    def remove(self, node):
        # get rid of it
        if self.first.next == self.first:
            self.first = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
            if self.first == node:
                self.first = node.next

    def jump(self, node, j):
        # jump a node j spaces in the list
        self.remove(node)
        next_node = node.next
        if j > 0:
            for _ in range(j):
                next_node = next_node.next
        elif j < 0:
            for _ in range(abs(j)):
                next_node = next_node.prev
        self.insert_before(next_node, node)


def create_circular_linked_list(data):
    # creates the initial list from data
    circ = CircularDoublyLinkedList()
    circ.insert_at_beg(Node(data[0], 0))
    for idx, val in enumerate(data[1:]):
        ref = circ.get_node_by_idx(idx)
        circ.insert_after(ref, Node(val, idx+1))
    return circ


def minimise_jump(x, n):
    # we don't want to cycle uncessarily...
    if x != 0:
        x_abs = abs(x)  # take abs to  help with %
        x_sign = x_abs/x  # record sign to preserve direction
        rem = x_abs % (n-1)  # every n-1 is a cycle, so we can remove
        x = int(rem * x_sign)  # this is how far we need to jump
    return x


def solver(data, n_loops):
    circ = create_circular_linked_list(data)
    # wrapper to apply all jumps
    for _ in range(n_loops):
        for order in range(n):  # swap nodes
            node = circ.get_node_by_order(order)
            jump = minimise_jump(node.data, n)
            circ.jump(node, jump)
    return circ


def final_score(circ):
    # compute final score
    znode, idx = circ.get_node_by_value(0)
    refs = [r+idx for r in [1000, 2000, 3000]]
    return sum([circ.get_node_by_idx(r).data for r in refs])


n = len(data)

# part 1 linked list
data1 = [int(x) for x in data]
circ1 = solver(data1, n_loops=1)
# part 1 answer
print(final_score(circ1))

# part 2 linked list
data2 = [int(x) * 811589153 for x in data]
circ2 = solver(data2, n_loops=10)
# part 2 answer
print(final_score(circ2))
