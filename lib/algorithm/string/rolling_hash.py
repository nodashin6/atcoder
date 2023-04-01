import random
class RollingHash:

    N_MAX = 10**6
    BASE = random.randint(2, 10**5)
    BASS = [1] + [BASE]*(N_MAX)
    MOD = (1<<31) - 1
    for i in range(N_MAX):
        BASS[i+1] *= BASS[i]
        BASS[i+1] %= MOD

    def __init__(self, string):
        self.n = len(string)
        self.a = [0] + list(map(ord, string))
        for i in range(self.n):
            self.a[i+1] = (self.a[i+1] + self.a[i] * self.BASE) % self.MOD

    def __len__(self):
        return self.n

    def get(self, l, r):
        return (self.a[r] - self.BASS[r-l] * self.a[l]) % self.MOD

    def set(self, l, r):
        return (self, l, r)

    @classmethod
    def lcp(cls, s0, s1) -> int:
        rh0, l0, r0 = s0
        rh1, l1, r1 = s1
        l = 0
        r = min(r0-l0, r1-l1) + 1
        while r-l > 1:
            m = (r + l) >> 1
            if rh0.get(l0, l0+m) == rh1.get(l1, l1+m):
                l = m
            else:
                r = m
        return l

    @classmethod
    def concat(cls, iterable) -> int:
        """
        concat([rh.set(l, r), rh.set(l, r), ..., rh.set(l, r)])
        """
        value = 0
        r = 0
        for rh, l, r in iterable:
            value = (value * cls.BASS[r-l] + rh.get(l, r)) % cls.MOD
        return value