class LoopDetector:

    def __init__(self, fn, init_value):
        self.a = [init_value]
        self.seen = set([init_value])
        self.fn = fn
        self.done_setup = False

    def setup(self):
        x = self.a[-1]
        while True:
            y = self.fn(x)
            if y not in self.seen:
                self.a.append(y)
                self.seen.add(y)
            else:
                self.y = y
                self.l = self.a.index(y)
                self.r = len(self.a)-1
                self.length = self.r - self.l + 1
                break
            x = y
        self.done_setup = True

    def __getitem__(self, index):
        if not self.done_setup:
            self.setup()
        if index < 0:
            raise IndexError
        elif index < len(self.a):
            return self.a[index]
        else:
            index -= self.l
            index %= self.length
            index += self.l
            return self.a[index]


# bit iteration
from itertools import product
for seq in product([0, 1], repeat=3):
    print(seq)
    # (0, 0, 0)
    # (0, 0, 1)
    # (0, 1, 0)
    # (0, 1, 1)
    # (1, 0, 0)
    # (1, 0, 1)
    # (1, 1, 0)
    # (1, 1, 1)


from itertools import permutations
for seq in permutations(range(3), r=2):
    print(seq)
    # (0, 1)
    # (0, 2)
    # (1, 0)
    # (1, 2)
    # (2, 0)
    # (2, 1)


from itertools import combinations
for seq in combinations(range(3), r=2):
    print(seq)
    # (0, 1)
    # (0, 2)
    # (1, 2)

