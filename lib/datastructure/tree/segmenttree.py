from collections.abc import Sequence
class SegmentTree(Sequence):
    """
    segment tree

    Methods
    -------
    set(i, v)
        replace value at specified position.
    prod(l=0, r=None)
        query in range of [l, r) and return aggregated value.
    iprod(l=0, r=None)
        query in range of [l, r) and return index of the values.
    """

    def __init__(self, n, e, op):
        self.bit_len = (n - 1).bit_length()
        self.m = (1 << self.bit_len) - 1
        self.n = self.m + n
        self.op = op
        self.e = e
        self.a = [self.e]*self.n
        return

    def set(self, i, v):
        i += self.m
        self.a[i] = v
        while i > 0:
            i = self._U(i)
            l = self._L(i)
            r = self._R(i)
            if r < self.n:
                self.a[i] = self.op(self.a[l], self.a[r])
            else:
                self.a[i] = self.a[l]
        return

    def all_prod(self):
        return self.a[0]

    def prod(self, l=0, r=None):
        i, v = self._prod(l, r)
        return v

    def _prod(self, l=0, r=None):
        nodes = self._get_nodes(l, r)
        i = None
        v = self.e
        for node in nodes:
            tmp = self.op(v, self.a[node])
            if v != tmp:
                i = node
                v = tmp
        return i, v

    def iprod(self, l=0, r=None):
        i, v = self._prod(l, r)
        while i < self.m:
            r = self._R(i)
            if r < self.n and self.a[r] == v:
                i = r
            else:
                i = r - 1
        return i - self.m

    def max_right(self, l, f):
        l += self.m
        r = self._R(self.m - 1)
        v = self.e
        while True:
            if ~l&1:
                if not f(self.op(v, self.a[l])):
                    while l < self.m:
                        l = self._L(l)
                        if f(self.op(v, self.a[l])):
                            v = self.op(v, self.a[l])
                            l += 1
                    break
                v = self.op(v, self.a[l])
                if l == r:
                    l = self.n
                    break
                l += 1
            if l == r:
                l = self.n
                break
            l = self._U(l)
            r = self._U(r)
        return l - self.m


    def _get_nodes(self, l=0, r=None):
        l = l + self.m
        r = self.n if r is None else r + self.m
        if l < 0 or self.n < r:
            raise IndexError("Sequence index out of range.")
        lnodes = []
        rnodes = []
        while r-l > 0:
            if ~l&1:
                lnodes.append(l)
                l += 1
            if ~r&1:
                rnodes.append(r-1)
                r -= 1
            l = (l-1)>>1
            r = (r-1)>>1
        return lnodes + rnodes[::-1]
    
    def _U(self, i): return (i-1) >> 1
    def _L(self, i): return (i<<1) + 1
    def _R(self, i): return (i<<1) + 2

    def dprint(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def __getitem__(self, index):
        if index < 0:
            index += len(self)
        if index < 0:
            raise ValueError("Sequence index out of range.")
        return self.a[index+self.m]
    def __setitem__(self, index, value):
        self.replace(index, value)
        return
    def __contains__(self, value: object) -> bool:
        return value in self.a[self.m:]
    def __len__(self):
        return self.n - self.m
    def __str__(self) -> str:
        return str(self.a[self.m:])
    def __repr__(self) -> str:
        return str(self.a[self.m:])