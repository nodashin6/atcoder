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