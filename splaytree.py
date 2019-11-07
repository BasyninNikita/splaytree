import sys
from queue import Queue
from math import log2


def get_command(stree):
    for line in sys.stdin:
        if 'set' in line and line.split()[0] == 'set':
            if len(line.replace('set', '').strip().split(' ')) == 2:
                success = stree.set(int(line.split()[1]), line.split()[2])
                if not success:
                    print('error')
            else:
                print('error')
        elif 'add' in line and line.split()[0] == 'add':
            if len(line.replace('add', '').strip().split(' ')) == 2:  # maybe isdigit
                success = stree.add(int(line.split()[1]), line.split()[2])
                if not success:
                    print('error')
            else:
                print('error')
        elif 'search' in line and line.split()[0] == 'search':
            if len(line.replace('search', '').strip().split(' ')) == 1:
                succ = stree.search(int(line.split()[1]))
                if succ is None:
                    print('0')
                else:
                    print(str(succ[0]) + ' ' + succ[1]) #str(succ).split()[1])
            else:
                print('error')
        elif 'print' in line:
            if line.replace("print", '') != '\n':
                print('error')
            else:
                print(stree.print(), end='')
        elif 'delete' in line and line.split()[0] == 'delete':
            if len(line.replace('delete', '').strip().split(' ')) == 1:
                success = stree.delete(int(line.split()[1]))
                if not success:
                    print('error')
            else:
                print('error')
        elif 'min' in line:
            if line.replace("min", '') != '\n':
                print('error')
            else:
                succ = stree.findMin()
                print('error') if succ is None else print(str(succ[0]) + ' ' + succ[1])
        elif 'max' in line:
            if line.replace("max", '') != '\n':
                print('error')
            else:
                succ = stree.findMax()
                print('error') if succ is None else print(str(succ[0]) + ' ' + succ[1])
        elif line == '\n':
            continue
        else:
            print('error')


class Node:
    def __init__(self, key, val, parent):
        self.key = key
        self.val = val  # val is string
        self.left = self.right = None
        self.parent = parent


class SplayTree:
    def __init__(self):
        self.root = None
        self.num_of_nodes = 0

    def findMin(self):
        if self.root is None:
            return None
        x = self.root
        while x.left is not None:
            x = x.left
        self.splay(x)
        return x.key, x.val

    def findMax(self):
        if self.root is None:
            return None
        x = self.root
        while x.right is not None:
            x = x.right
        self.splay(x)
        return x.key, x.val

    def search(self, key):
        if self.root is None:
            return None
        x = self.root
        while 1:
            if x.key < key and x.right is not None:
                x = x.right
            elif x.key > key and x.left is not None:
                x = x.left
            elif x.key == key:
                self.splay(x)
                return 1, x.val
            else:
                self.splay(x)
                return None

    def add(self, key, val):
        if self.root is None:
            self.root = Node(key, val, None)
            self.num_of_nodes += 1
            return True
        x = self.root
        while 1:  # x is not None:
            if x.key > key:
                if x.left is None:
                    x.left = Node(key, val, x)
                    x.left.parent = x
                    self.splay(x.left)
                    self.num_of_nodes += 1
                    break
                else:
                    x = x.left
            elif x.key < key:
                if x.right is None:
                    x.right = Node(key, val, x)
                    x.right.parent = x
                    self.splay(x.right)
                    self.num_of_nodes += 1
                    break
                else:
                    x = x.right
            else:
                return False
        return True

    def delete(self, key):
        if self.root is None:
            return False
        x = self.root
        while 1:  # x is not None:
            if x is None:
                return False
            elif x.key > key:
                x = x.left
            elif x.key < key:
                x = x.right
            elif x.key == key:
                self.splay(x)
                break
            else:
                return False
        self.num_of_nodes -= 1
        left_tree = x.left
        right_tree = x.right
        if left_tree is not None:
            left_tree.parent = None
        if right_tree is not None:
            right_tree.parent = None

        if left_tree is None:
            self.root = right_tree
        elif right_tree is None:
            self.root = left_tree
        else:
            self.root = left_tree
            x = left_tree
            while x.right is not None:
                x = x.right
            self.splay(x)
            x.right = right_tree
            right_tree.parent = x
        return True

    def set(self, key, value):
        x = self.root
        while 1:
            if x is None:
                return False
            elif x.key < key and x.right is not None:
                x = x.right
            elif x.key > key and x.left is not None:
                x = x.left
            elif x.key == key:
                x.val = value
                self.splay(x)
                return True
            else:
                # self.splay(x)
                return False

    def Zig(self, x):
        if x.parent.right == x:
            x.parent.right = x.left
            if x.left is not None:
                x.left.parent = x.parent
            x.left = x.parent

        if x.parent.left == x:
            x.parent.left = x.right
            if x.right is not None:
                x.right.parent = x.parent
            x.right = x.parent

        grandpa = x.parent.parent
        if grandpa is not None and grandpa.right == x.parent:
            grandpa.right = x
        elif grandpa is not None and grandpa.left == x.parent:
            grandpa.left = x
        else:
            self.root = x
        x.parent.parent = x
        x.parent = grandpa

    def ZigZig(self, x):
        self.Zig(x.parent)
        self.Zig(x)

    def ZigZag(self, x):
        self.Zig(x)
        self.Zig(x)

    def splay(self, x):
        while x != self.root:
            if x.parent == self.root:
                self.Zig(x)
            else:
                if x.parent.left == x and x.parent.parent.left == x.parent:
                    self.ZigZig(x)
                elif x.parent.right == x and x.parent.parent.right == x.parent:
                    self.ZigZig(x)
                else:
                    self.ZigZag(x)

    def print(self):
        if self.root is None:
            return '_\n'
        q = Queue()
        s = '[' + str(self.root.key) + ' ' + self.root.val + ']' + '\n'
        n = self.num_of_nodes
        n -= 1
        if n == 0:
            return s

        if not self.root.left:
            q.put({None: 1})
        else:
            q.put(self.root.left)
        if not self.root.right:
            q.put({None: 1})
        else:
            q.put(self.root.right)

        count = 1  # счетчик уровня, отслеживает что нижний слой закончился
        step = 1
        stop = False
        out = ''
        i = 0

        while 1:
            x = q.get()
            if type(x) == dict:
                count += x[None]
                nones_counter = x[None] * 2
                q.put({None: nones_counter})
            else:
                n -= 1
                count += 1
                if not x.left:
                    q.put({None: 1})
                else:
                    q.put(x.left)
                if not x.right:
                    q.put({None: 1})
                else:
                    q.put(x.right)

            r = log2(count + 1)
            if n == 0 and r == int(r):
                stop = True

            if type(x) == dict:
                for k in range(x[None]):
                    out += '_ '
                    i += 1
            else:
                out += '[{} {} {}] '.format(x.key, x.val, x.parent.key)
                i += 1

            if i == 2 ** step:
                s += out[:-1] + '\n'
                out = ''
                i = 0
                step += 1

            if stop:
                break
        return s


st = SplayTree()
get_command(st)
