class Mask:
    """
    For converting list to int with bit mask.
    For examle [1, 1] is converted to 101 by twice left shit.
    """

    def __init__(self, n=30):
        """
        n : int
            [n=30] 1<<n = 2**30 > 10**9
        """
        self.n = n
        self.b = 1<<n

    def toint(self, seq):
        x, y = seq
        return (x<<self.n) + y

    def tolist(self, v):
        return (v>>self.n, v%self.b)
        
    @classmethod
    def sorted(cls, a, reverse=False):
        mask = cls(n=len(a).bit_length())
        data = [None]*len(a)
        obj = []
        for i, (ai, *other) in enumerate(a):
            data[i] = other
            obj.append(mask.toint([ai, i]))
        obj.sort(reverse=reverse)
        a_sorted = []
        for ai_masked in obj:
            ai, i = mask.tolist(ai_masked)
            a_sorted.append([ai] + data[i])
        return a_sorted
