import sys
import numpy as np
from copy import deepcopy
from itertools import product
# from time import sleep


class sudoku:
    def __init__(self, size, a=None):
        self.size = size
        size = self.size
        if a is None:
            self.a = np.full((size, size), -1, dtype="int8")
        else:
            self.a = a
        self.row_sets = [set(range(1, size+1)) for i in range(size)]
        self.col_sets = [set(range(1, size+1)) for i in range(size)]
        self.box_sets = [set(range(1, size+1)) for i in range(size)]
        self.box_size = int(size**0.5)
        self.empty_boxes = 0
        self.box_starts = self.starting_of_boxes()
        self.all_numbers = frozenset(set(range(1, size+1)))
        self.rs_copy = []
        self.cs_copy = []
        self.bs_copy = []
        self.a_copy = []
        self.empty_boxes_copy = []

    def count_empty_boxes(self):
        a = self.a
        self.empty_boxes = np.sum(a == -1)
        return self.empty_boxes

    def starting_of_boxes(self):
        size = self.size
        box_size = self.box_size
        return tuple(product(range(0, size, box_size), range(0, size, box_size)))

    def get_sets(self):
        rs = self.row_sets
        cs = self.col_sets
        bs = self.box_sets
        a = self.a
        size = self.size
        box_size = self.box_size
        box_starts = self.box_starts

        for i in range(size):
            rs[i] -= set(a[i])
            cs[i] -= set(a[:, i])
            x, y = box_starts[i]
            bs[i] -= set(np.unique(a[x:x+box_size, y:y+box_size]))

    def is_correct(self):
        a = self.a
        size = self.size
        box_starts = self.box_starts
        box_size = self.box_size

        for i in range(size):
            if len(np.unique(a[i])) < size:
                return False
            if len(np.unique(a[:, i])) < size:
                return False
            x, y = box_starts[i]
            if len(np.unique(a[x:x+box_size, y:y+box_size])) < size:
                return False
        return True

    def show(self):
        size = self.size
        a = self.a
        for i in range(size):
            for j in range(size):
                print(end='|')
                x = a[i][j]
                if x == -1:
                    print(' ', end='|')
                else:
                    print(x, end='|')
            print()

    def box_number(self, i, j):
        box_size = self.box_size
        return box_size*(i//box_size)+(j//box_size)

    def update_sets(self, val, i, j):
        k = self.box_number(i, j)
        self.empty_boxes -= 1
        self.row_sets[i].remove(val)
        self.col_sets[j].remove(val)
        self.box_sets[k].remove(val)

    def update_numbers(self):
        rs = self.row_sets
        cs = self.col_sets
        bs = self.box_sets
        size = self.size
        a = self.a
        box_size = self.box_size
        mi = (self.all_numbers.copy(), 0, 0)

        for i in range(size):
            for j in range(size):
                if a[i][j] != -1:
                    continue
                k = self.box_number(i, j)
                intersection = rs[i] & cs[j] & bs[k]
                if len(intersection) == 0:
                    return 1  # wrong
                if len(intersection) < len(mi[0]):
                    mi = (intersection, i, j)
                if len(intersection) == 1:
                    val = list(intersection)[0]
                    a[i][j] = val
                    self.update_sets(val, i, j)
        return mi

    def attempt(self, mi):
        intersection, i, j = mi
        for possibility in intersection:
            self.a_copy.append(np.copy(self.a))
            self.rs_copy.append(deepcopy(self.row_sets))
            self.cs_copy.append(deepcopy(self.col_sets))
            self.bs_copy.append(deepcopy(self.box_sets))
            self.empty_boxes_copy.append(self.empty_boxes)
            self.a[i][j] = possibility
            self.update_sets(possibility, i, j)
            yield possibility, i, j

    def back_attempt(self):
        self.row_sets = deepcopy(self.rs_copy.pop())
        self.col_sets = deepcopy(self.cs_copy.pop())
        self.box_sets = deepcopy(self.bs_copy.pop())
        self.a = np.copy(self.a_copy.pop())
        self.empty_boxes = self.empty_boxes_copy.pop()


def main(sdk):
    sdk.show()
    print(f"\n{sdk.count_empty_boxes()} empty boxes ,",)
    attempted = False
    sdk.get_sets()
    earlier_empty_boxes = sdk.empty_boxes
    x = imain(sdk, earlier_empty_boxes, 0)
    sdk.show()
    print("\n-----correct is ", sdk.is_correct(), "------\n")
    # print(sdk.a)
    return sdk.a


sys.setrecursionlimit(1000)
# '''


def imain(sdk, earlier_empty_boxes, attempt):
    # print(sdk.a)
    # sleep(0.1)
    if sdk.empty_boxes == 0:
        return True
    x = 0
    while (x != 1):
        x = sdk.update_numbers()
        if sdk.empty_boxes == 0:
            return True
        if earlier_empty_boxes == sdk.empty_boxes:
            break
        earlier_empty_boxes = sdk.empty_boxes
    else:
        if sdk.empty_boxes == 0 and x != 1:
            return True
    attempt = sdk.attempt(x)
    while True:
        try:
            next(attempt)
        except:
            return False
        result = imain(sdk, earlier_empty_boxes, 0)
        if result:
            return True
        else:
            sdk.back_attempt()
# '''


def test_data1():
    sdk = sudoku(9)
    sdk.a[0] = [5, 3, -1, -1, 7, -1, -1, -1, -1]
    sdk.a[1] = [6, -1, -1, 1, 9, 5, -1, -1, -1]
    sdk.a[2] = [-1, 9, 8, -1, -1, -1, -1, 6, -1]
    sdk.a[3] = [8, -1, -1, -1, 6, -1, -1, -1, 3]
    sdk.a[4] = [4, -1, -1, 8, -1, 3, -1, -1, 1]
    sdk.a[5] = [7, -1, -1, -1, 2, -1, -1, -1, 6]
    sdk.a[6] = [-1, 6, -1, -1, -1, -1, 2, 8, -1]
    sdk.a[7] = [-1, -1, -1, 4, 1, 9, -1, -1, 5]
    sdk.a[8] = [-1, -1, -1, -1, 8, -1, -1, 7, 9]
    return sdk


def test_data2():
    sdk = sudoku(9)
    sdk.a[0] = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    sdk.a[1] = [-1, 1, 2, -1, 3, 4, 5, 6, 7]
    sdk.a[2] = [-1, 3, 4, 5, -1, 6, 1, 8, 2]
    sdk.a[3] = [-1, -1, 1, -1, 5, 8, 2, -1, 6]
    sdk.a[4] = [-1, -1, 8, 6, -1, -1, -1, -1, 1]
    sdk.a[5] = [-1, 2, -1, -1, -1, 7, -1, 5, -1]
    sdk.a[6] = [-1, -1, 3, 7, -1, 5, -1, 2, 8]
    sdk.a[7] = [-1, 8, -1, -1, 6, -1, 7, -1, -1]
    sdk.a[8] = [2, -1, 7, -1, 8, 3, 6, 1, 5]
    return sdk


def test_data3():
    sdk = sudoku(9)
    sdk.a[0] = [1, -1, -1, -1, -1, -1, -1, -1, -1]
    sdk.a[1] = [-1, 2, -1, -1, 6, 7, 8, 9, -1]
    sdk.a[2] = [3, -1, -1, -1, 4, -1, -1, -1, -1]
    sdk.a[3] = [-1, 4, -1, -1, 3, -1, -1, -1, -1]
    sdk.a[4] = [-1, -1, -1, -1, 2, 1, 6, 7, -1]
    sdk.a[5] = [-1, 6, -1, -1, -1, -1, -1, 8, -1]
    sdk.a[6] = [-1, -1, 7, -1, -1, -1, -1, 4, -1]
    sdk.a[7] = [-1, 8, -1, -1, 9, 3, 7, 2, -1]
    sdk.a[8] = [-1, -1, 9, -1, -1, -1, -1, -1, -1]
    return sdk


def test_data4():
    sdk = sudoku(9)
    sdk.a[0] = [-1, -1, -1, 1, -1, -1, 5, -1, 2]
    sdk.a[1] = [-1, -1, -1, -1, 9, -1, -1, -1, -1]
    sdk.a[2] = [-1, 9, 8, 5, -1, -1, -1, 7, -1]
    sdk.a[3] = [-1, -1, -1, -1, 6, 1, -1, -1, -1]
    sdk.a[4] = [-1, -1, 5, -1, -1, -1, -1, 4, -1]
    sdk.a[5] = [9, 2, -1, -1, 5, -1, -1, 3, -1]
    sdk.a[6] = [-1, -1, -1, 7, -1, 4, -1, -1, 8]
    sdk.a[7] = [-1, -1, -1, -1, -1, -1, 7, -1, 9]
    sdk.a[8] = [3, 5, -1, -1, -1, -1, -1, -1, 6]
    return sdk


def test_data5():
    sdk = sudoku(9)
    sdk.a[0] = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    sdk.a[1] = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    sdk.a[2] = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    sdk.a[3] = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    sdk.a[4] = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    sdk.a[5] = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    sdk.a[6] = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    sdk.a[7] = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    sdk.a[8] = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
    return sdk


def test_data6():
    sdk = sudoku(9)
    sdk.a = np.array([[5, 3, 4, 6, 7, 8, 9, 1, 2], [6, 7, 2, 1, 9, 5, 3, 4, 8],
                      [1, 9, 8, 3, 4, 2, 5, 6, 7], [8, 5, 9, 7, 6,
                                                    1, 4, 2, 3], [4, 2, 6, 8, 5, 3, 7, 9, 1],
                      [7, 1, 3, 9, 2, 4, 8, 5, 6], [9, 6, 1, 5, 3,
                                                    7, 2, 8, 4], [2, 8, 7, 4, 1, 9, 6, 3, 5],
                      [3, 4, 5, 2, 8, 6, 1, 7, 9]])
    return sdk


def test_data7():
    s = 4**2
    sdk = sudoku(s)
    sdk.a = np.full((s, s), -1, dtype='int8')
    return sdk


if __name__ == "__main__":
    main(test_data1())
    main(test_data2())
    main(test_data3())
    main(test_data4())
    main(test_data5())
    main(test_data6())
    main(test_data7())
