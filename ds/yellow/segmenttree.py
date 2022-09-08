# https://github.com/nodashin6/atcoder/blob/main/ds/yellow/segmenttree.py
from collections.abc import Sequence
import math
class SegmentTree(Sequence):
    """
    segment tree

    Methods
    -------
    replece(i, v)
        replace value at specified position.
    value_query(l=0, r=None, nodes=[])
        query in range of [l, r) and return aggregated value.
    index_query(l=0, r=None, nodes=[])
        query in range of [l, r) and return index of the values.

    Problems
    --------
    [RMQ]
    ABC267E: https://atcoder.jp/contests/abc267/submissions/34691372
    """
    INF = 1<<62
    AGGFUNCS = {
        'min': lambda a, b: (a, b)[a>b],
        'max': lambda a, b: (a, b)[a<b],
        'sum': lambda a, b: a + b,
        'gcd': math.gcd,
        'xor': lambda a, b: a ^ b
        }

    def __init__(self, a=[], default_value=INF, agg='min'):

        n = len(a)
        self.bit_len = (n - 1).bit_length()
        self.m = (1 << self.bit_len) - 1
        self.n = self.m + n

        self.agg = self.AGGFUNCS[agg]

        self.DV = default_value
        self.a = [self.DV]*self.m + a
        self._build()
        return
        
    def _build(self):
        for i in reversed(range(self.m, self.n)):
            while i&1:
                j = i>>1
                if i+1 < self.n:
                    self.a[j] = self.agg(self.a[i], self.a[i+1])
                else:
                    self.a[j] = self.a[i]
                i, j = j, j>>1

    def replace(self, i, v):
        i += self.m
        self.a[i] = v
        while i>0:
            j = (i-1)>>1
            # calculate
            if ~i&1:
                v = self.agg(self.a[i-1], self.a[i])
            elif i+1 < self.n:
                v = self.agg(self.a[i], self.a[i+1])
            else:
                v = self.a[i]
            # update
            if self.a[j] == self.a[i]:
                break
            else:
                self.a[j] = v
            i, j = j, (j-1)>>1
        return

    def value_query(self, l=0, r=None, nodes=[]):
        nodes = self._get_index(l, r) if not nodes else nodes
        v = self.DV
        for i in nodes:
            if self.a[i] == self.agg(v, self.a[i]):
                v = self.a[i]
        return v

    def index_query(self, l=0, r=None, nodes=[]):
        nodes = self._get_index(l, r) if not nodes else nodes
        index = None
        v = self.DV
        for i in reversed(nodes):
            if self.a[i] == self.agg(v, self.a[i]):
                index = i
                v = self.a[i]
            
        while index < self.m:
            r = (index<<1) + 2
            if r < self.n and self.a[r] == v:
                index = r
            else:
                index = r - 1
        return index - self.m

    def _get_index(self, l=0, r=None):
        l = l + self.m
        r = self.n if r is None else r + self.m
        if l < 0 or self.n < r:
            raise IndexError("Sequence index out of range.")
        nodes = []
        while r-l > 0:
            if ~l&1:
                nodes.append(l)
                l += 1
            if ~r&1:
                nodes.append(r-1)
            l = (l-1)>>1
            r = (r-1)>>1
        return nodes

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