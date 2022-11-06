## Binary Indexed Tree
## https://github.com/nodashin6/atcoder/blob/main/ds/tree/binaryindexedtree.py
class BinaryIndexedTree():
    """
    Problems
    --------
    T90_10: https://atcoder.jp/contests/typical90/submissions/36276290

    See Also
    --------
    1. https://algo-logic.info/binary-indexed-tree/
    """
 
    def __init__(self, a=None, n=None, init_v=None, ruq=True):
        """
        Parameters
        ----------
        a : list
            input data
        n : int
            size of bit
        init_v : int, float
            init_value
        ruq : bool
            `ruq` means Range Update Query (RUQ).
            If `ruq` is True, BIT can use range_add function 
            with 1.1~1.4 times cost.
        """
        if a:
            self.N = len(a)
            self.a = self._build(a.copy())
        else:
            self.N = n
            self.a = [init_v]*self.N
        if ruq:
            self.b = [0]*self.N
        else:
            self.sum = self._asum
            self.range_add = self._range_add

    def _build(self, a):
        for i in range(self.N): 
            j = i + (~i & -~i)
            if j < self.N:
                a[j] += a[i]
        return a

    def __len__(self):
        return self.N
 
    def __getitem__(self, i):
        return self.sum(i+1) - self.sum(i)

    def __setitem__(self, i, v):
        return self.add(i, v-self[i])
 
    def sum(self, r):
        """
        Return:
        -------
        v : int
            v = a[0] + a[1] + ... + a[r-1]
        """
        return self._sum(self.a, r) + r * self._sum(self.b, r)

    def _sum(self, bit, r):
        v = 0
        i = r-1
        while 0 <= i:
            v += bit[i]
            i -= (~i & -~i)
        return v

    def range_add(self, r, v):
        """a[0:r] += v"""
        if r < self.N:
            self._add(self.a, i=r, v=v*r)
            self._add(self.b, i=r, v=-v)
        self._add(self.b, i=0, v=v)

    def add(self, i, v):
        """a[i] += v"""
        self._add(self.a, i, v)

    def _add(self, bit, i, v):
        while i < self.N:
            bit[i] += v
            i += ~i & -~i
        
    def tolist(self):
        x = [self.sum(i) for i in range(self.N+1)]
        return [x1-x0 for x0, x1 in zip(x[:-1], x[1:])]

    # ------------------------------------------------------------------------
    # Use these methods when BIT doesn't require Range Update Query (RUQ)
    def _asum(self, r):
        """sum of a[0] + a[1] + ... + a[r-1] when `ruq` is False."""
        return self._sum(self.a, r)

    def _range_add(self, *args):
        raise NotImplementedError(
            "`range_add()` is not defined when `ruq` is False.")


# -----------------------------------------
# Application
# -----------------------------------------
def count_inversion(a):
    """
    転倒数の計算

    Parameters:
    -----------
    a : list[int]
        input integers
    """
    # 座標圧縮
    d = {k: v for v, k in enumerate(sorted(set(a)))}

    cnt = 0
    r_max = max(d.values())+1
    bit = BinaryIndexedTree(n=r_max, v=0, ruq=False)
    for i, ai in enumerate(a):
        cnt += i - bit.sum(r=d[ai]+1)
        bit.add(i=d[ai], v=1)
    return cnt