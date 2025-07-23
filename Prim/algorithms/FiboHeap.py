import math

class FibonacciHeap:
    class Node:
        def __init__(self, key, value=None):
            self.key = key
            self.value = value
            self.parent = self.child = self.left = self.right = None
            self.degree = 0
            self.mark = False

    def __init__(self):
        self.root_list = None
        self.min_node = None
        self.total_nodes = 0

    def iterate(self, head):
        node = stop = head
        flag = False
        while True:
            if node == stop and flag:
                break
            flag = True
            yield node
            node = node.right

    def find_min(self):
        return self.min_node

    def insert(self, key, value=None):
        node = self.Node(key, value)
        node.left = node.right = node
        self.merge_with_root_list(node)
        if self.min_node is None or node.key < self.min_node.key:
            self.min_node = node
        self.total_nodes += 1
        return node

    def merge_with_root_list(self, node):
        if self.root_list is None:
            self.root_list = node
            node.left = node.right = node
        else:
            node.right = self.root_list.right
            node.left = self.root_list
            self.root_list.right.left = node
            self.root_list.right = node

    def extract_min(self):
        z = self.min_node
        if z is not None:
            if z.child is not None:
                children = [x for x in self.iterate(z.child)]
                for child in children:
                    self.merge_with_root_list(child)
                    child.parent = None
            self.remove_from_root_list(z)
            if z == z.right:
                self.root_list = self.min_node = None
            else:
                self.root_list = self.min_node = z.right
                self.consolidate()
            self.total_nodes -= 1
        return z

    def remove_from_root_list(self, node):
        if node == node.right:
            self.root_list = None
        else:
            node.left.right = node.right
            node.right.left = node.left
            if self.root_list == node:
                self.root_list = node.right

    def consolidate(self):
        A = [None] * (int(math.log(self.total_nodes or 1, 2)) + 1)
        nodes = [w for w in self.iterate(self.root_list)]
        for w in nodes:
            x = w
            d = x.degree
            while A[d] is not None:
                y = A[d]
                if x.key > y.key:
                    x, y = y, x
                self.heap_link(y, x)
                A[d] = None
                d += 1
            A[d] = x
        self.min_node = None
        for i in range(len(A)):
            if A[i] is not None:
                if self.min_node is None or A[i].key < self.min_node.key:
                    self.min_node = A[i]

    def heap_link(self, y, x):
        self.remove_from_root_list(y)
        y.left = y.right = y
        self.merge_with_child_list(x, y)
        y.parent = x
        x.degree += 1
        y.mark = False

    def merge_with_child_list(self, parent, node):
        if parent.child is None:
            parent.child = node
            node.left = node.right = node
        else:
            node.right = parent.child.right
            node.left = parent.child
            parent.child.right.left = node
            parent.child.right = node

    def decrease_key(self, x, k):
        if k > x.key:
            raise ValueError("new key is greater than current key")
        x.key = k
        y = x.parent
        if y is not None and x.key < y.key:
            self.cut(x, y)
            self.cascading_cut(y)
        if x.key < self.min_node.key:
            self.min_node = x

    def cut(self, x, y):
        self.remove_from_child_list(y, x)
        y.degree -= 1
        self.merge_with_root_list(x)
        x.parent = None
        x.mark = False

    def cascading_cut(self, y):
        z = y.parent
        if z is not None:
            if not y.mark:
                y.mark = True
            else:
                self.cut(y, z)
                self.cascading_cut(z)

    def remove_from_child_list(self, parent, node):
        if node.right == node:
            parent.child = None
        else:
            node.left.right = node.right
            node.right.left = node.left
            if parent.child == node:
                parent.child = node.right
        node.left = node.right = node
    
    def is_empty(self):
        return self.total_nodes == 0