from collections.abc import Sequence
class LazySegmentTree(Sequence):
    """
    lazysegmenttree
    """
    INF = 1<<62

    def __init__(self, a=[], e=None, ope=None, mapping=None, idfunc=None, compose=None):

        self.bit_len = (len(a) - 1).bit_length()
        self.m = (1 << self.bit_len) - 1
        self.n = self.m + len(a)

        self.a = [e] * (self.m*2 + 1)
        self.E = e
        self.ope = ope
        self.mapping = mapping
        
        self.b = [idfunc] * self.m
        self.idfunc = idfunc
        self.compose = compose
        
        self.a[self.m:self.m+len(a)] = a
        self._build()

        # self.forsetattr = self.ForSetAttr()
        return
        
    def _build(self):
        for i in reversed(range(self.m)):
            self.update(i)
        return

    def update(self, i):
        self.a[i] = self.ope(self.a[self._L(i)], self.a[self._R(i)])
        return

    def push(self, i):
        self._iapply(self._L(i), self.b[i])
        self._iapply(self._R(i), self.b[i])
        self.b[i] = self.idfunc

    def apply(self, l, r, f):
        l += self.m
        r += self.m
        dq = self._range_push(l, r)
        self._range_apply(l, r, f)
        for i in reversed(dq):
            self.update(i)

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

    def _iapply(self, i, f):
        # print(f'i={i}, a[i]={self.a[i]}, f={f}')
        self.a[i] = self.mapping(f, self.a[i])
        if i < self.m:
            self.b[i] = self.compose(f, self.b[i])

    def query(self, l, r):
        l += self.m
        r += self.m
        self._range_push(l, r)
        return self._range_query(l, r)

    def _range_query(self, l, r):
        v = self.E
        while l < r:
            if ~-l&1:
                v= self.ope(v, self.a[l])
                l += 1
                
            if ~-r&1:
                v= self.ope(v, self.a[r-1])
            l = self._U(l)
            r = self._U(r)
        return v

    def __getitem__(self, index):
        return self.a[index+self.m]

    def __len__(self):
        return self.n


    # ----------------------------------------------------------------------
    # About Location
    def _U(self, i): return (i-1) >> 1
    def _L(self, i): return (i<<1) + 1
    def _R(self, i): return (i<<1) + 2
    


def ope(x, y):
    return max(x, y)

def mapping(f, x):
    if f == 0:
        return x
    return f(x)

def compose(f, g):
    if f == 0:
        return g
    elif g == 0:
        return f
    else:
        v = list(f.v)
        v[0] *= g.v[0]
        v[1] = v[1]*g.v[0] + f.v[1]
        return AppliedFunc(v=(v[0], v[1]))

class AppliedFunc():
    def __init__(self, v=(1, 0)):
        self.v = v
    def __call__(self, x):
        s, t = self.v
        return s*x + t


