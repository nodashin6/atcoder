class Mask:
    """
    For converting list to int with bit mask.
    For examle [1, 1] is converted to 101 by twice left shit.
    """

    def __init__(self, n=30, w=2):
        """
        n : int
            [n=30] 1<<n = 2**30 > 10**9
        """
        self.n = n
        self.w = w
        self.b = 1 << self.n

    def toint(self, seq):
        v = 0
        for i, x in enumerate(seq):
            n = self.n * (self.w - i - 1)
            v += x << n
        return v

    def tolist(self, v):
        seq = []
        for i in range(self.w):
            seq.append(v%self.b)
            v >>= self.n
        return seq[::-1]

    @classmethod
    def for_sorted(cls, a, n=30, key=None, reverse=False):
        mask = cls(n=30, w=len(a[0]))
        b = [mask.toint(ai) for ai in a]
        b.sort(key=key, reverse=reverse)
        for bi in b:
            yield mask.tolist(bi)