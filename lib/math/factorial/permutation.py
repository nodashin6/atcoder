def permutation(n, k, mod=1_000_000_007):
    v = 1
    for i in reversed(range(n-k+1, n+1)):
        v *= i
        v %= mod
    return v