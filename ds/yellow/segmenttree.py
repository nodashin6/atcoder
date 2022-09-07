# https://github.com/nodashin6/atcoder/blob/main/ds/yellow/segmenttree.py
from collections.abc import Sequence
class SegmentTree(Sequence):

    INF = 1<<62
    def __init__(self, a=[], default_value=INF, agg=min):

        n = len(a)
        self.bit_len = (n - 1).bit_length()
        self.m = (1 << self.bit_len) - 1
        self.n = self.m + n

        self.agg = agg

        self.DV = default_value
        self.a = [default_value]*self.m + a
        self._build()
        return
        
    def _build(self):
        for i in reversed(range(self.m, self.n)):
            while i&1:
                j = i>>1
                if i+1 < self.n:
                    self.a[j] = self.a[i+1]
                self.a[j] = self.agg(self.a[i], self.a[j])
                i, j = j, j>>1

    def replace(self, i, v):
        i += self.m
        self.a[i] = v
        while i>0:
            j = (i-1)>>1
            if self.a[j] == self.a[i]:
                break
            if ~i&1:
                self.a[j] = self.agg(self.a[i-1], self.a[i])
            elif i+1 < self.n:
                self.a[j] = self.agg(self.a[i], self.a[i+1])
            else:
                self.a[j] = self.a[i]
            i, j = j, (j-1)>>1
        return

    def query(self, l, r):
        l += self.m
        r += self.m
        if l < 0 or self.n < r:
            raise IndexError("Sequence index out of range.")
        locs = []
        while r-l > 0:
            if ~l&1:
                locs.append(l)
            if ~r&1:
                locs.append(r-1)
            l = (l-1)>>1
            r = (r-1)>>1
        v = self.DV
        for i in locs:
            v = self.agg(v, self.a[i])
        return v

    def __getitem__(self, index):
        return self.a[index+self.m]
    def __setitem__(self, index, value):
        self.replace(index, value)
        return
    def __len__(self):
        return self.n - self.m
    def __str__(self) -> str:
        return str(self.a[self.m:])
    def __repr__(self) -> str:
        return str(self.a[self.m:])