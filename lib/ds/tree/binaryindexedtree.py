# -----------------------------------------------------------------------------
# Binary Indexed Tree
# https://github.com/nodashin6/atcoder/blob/main/ds/yellow/binaryindexedtree.py
# -----------------------------------------------------------------------------
class BIT():
    """
    Problems
    --------
    T90_10: https://atcoder.jp/contests/typical90/submissions/32480628

    See Also
    --------
    1. https://algo-logic.info/binary-indexed-tree/
    """
 
    def __init__(self, a=None, n=None, v=None):
        
        self.N = len(a) if a else n
        self.bit0 = BasicBIT(a=a) if a else BasicBIT(n=n, v=v)
        self.bit1 = BasicBIT(n=self.N, v=0)
 
    def __len__(self):
        return self.bit0.N
 
    def __getitem__(self, i):
        return self.sum(i+1) - self.sum(i)
 
    def sum(self, r):
        """
        Return:
        -------
        v : int
            v = a[0] + a[1] + ... + a[r-1]
        """
        a = self.bit0.sum(r)
        b = self.bit1.sum(r)
        v = a + b*r
        return v
 
    def rsum(self, l, r):
        return self.sum(r) - self.sum(l)
 
    def radd(self, r, v):
        """
        a[0:r] += v
        """
        if r < self.N:
            self.bit0.add(i=r, v=v*r)
            self.bit1.add(i=r, v=-v)
        self.bit1.add(i=0, v=v)
        
    def tolist(self):
        x = [self.sum(i) for i in range(self.N+1)]
        return [x1-x0 for x0, x1 in zip(x[:-1], x[1:])]
 
 
class BasicBIT():
 
    def __init__(self, a=None, n=None, v=None):
        if a is None:
            self.a = [v]*n
            self.N = n
            self.K = self.N.bit_length()+1
        else:
            self.a = a
            self.N = len(a)
            self.K = self.N.bit_length()+1
            self._build()
 
    def _build(self):
        for i in range(self.N):
            for k in range(self.K):
                if (i>>k)&1 == 0:
                    break
            j = i + (1<<k)
            if j < self.N:
                self.a[j] += self.a[i]
 
    def sum(self, r):
        """
        Return:
        -------
        v : int
            v = a[0] + a[1] + ... + a[r-1]
        """
        i = r-1
        v = 0
        for k in range(self.K):
            if i < 0:
                break
            if (i>>k)&1 == 0:
                v += self.a[i]
                i -= (1<<k)
        return v
 
    def add(self, i, v):
        for k in range(self.K):
            if (i>>k)&1 == 0:
                self.a[i] += v
                i += (1<<k)
            if i >= self.N:
                break


# -----------------------------------------
# Application
# -----------------------------------------
def count_inversion(a):
    """
    転倒数の計算

    Parameters:
    -----------
    a : list
        input integers
    """
    # 座標圧縮
    d = {k: v for v, k in enumerate(sorted(set(a)))}

    cnt = 0
    r_max = max(d.values())+1
    bit = BasicBIT(n=r_max, v=0)
    for i, ai in enumerate(a):
        cnt += i - bit.sum(r=d[ai]+1)
        bit.add(i=d[ai], v=1)
    return cnt