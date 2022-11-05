from collections.abc import Sequence
class LazyList(Sequence):
    """
    lazysegmenttree without monoid
    """
    INF = 1<<62

    def __init__(self, a=[], e=None, mapping=None, idfunc=None, compose=None):

        self.bit_len = (len(a) - 1).bit_length()
        self.m = (1 << self.bit_len) - 1
        self.n = self.m

        self.a = [e] * (self.m+1)
        self.a[:len(a)] = a
        self.E = e
        self.mapping = mapping
        
        self.b = [idfunc] * self.m
        self.idfunc = idfunc
        self.compose = compose

        # self.forsetattr = self.ForSetAttr()
        return


    def push(self, i):
        self._iapply(self._L(i), self.b[i])
        self._iapply(self._R(i), self.b[i])
        self.b[i] = self.idfunc

    def push_all(self):
        for i in range(self.m):
            self.push(i)

    def apply(self, l, r, f):
        l += self.m
        r += self.m
        self._range_push(l, r)
        self._range_apply(l, r, f)

    def _iapply(self, i, f):
        # print(f'i={i}, a[i]={self.a[i]}, f={f}')
        if i < self.m:
            self.b[i] = self.compose(f, self.b[i])
        else:
            self.a[i-self.m] = self.mapping(f, self.a[i-self.m])

    def _range_push(self, l, r):
        # applying old updating.
        dq = set([])
        while l&1:
            l = self._U(l)
        while l>0:
            l = self._U(l)
            dq.add(l)
        while r&1:
            r = self._U(r)
        while r>0:
            r = self._U(r)
            dq.add(r)
        dq = sorted(dq)
        for i in dq:
            self.push(i)
        return dq

    def _range_apply(self, l, r, f):
        # print(f'[range_apply(l={l}, r={r})]')
        while l < r:
            if ~-l&1:
                # print(f'[apply]: l={l}')
                self._iapply(l, f)
                l += 1
            if ~-r&1:
                # print(f'[apply]: r={r-1}')
                self._iapply(r-1, f)
            l = self._U(l)
            r = self._U(r)

    def __getitem__(self, index):
        return self.a[index]

    def __len__(self):
        return len(self.a)

    # ----------------------------------------------------------------------
    # About Location
    def _U(self, i): return (i-1) >> 1
    def _L(self, i): return (i<<1) + 1
    def _R(self, i): return (i<<1) + 2
    

def mapping(f, x):
    if f is None:
        return x
    return min(f, x)

def compose(f, g):
    if f is None:
        return g
    if g is None:
        return f
    return min(f, g)