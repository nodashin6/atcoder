from collections.abc import Sequence
class LazySegmentTree(Sequence):
    """
    LazySegmentTree

    composition(f, g) -> f(g(x))
    """
    def __init__(
            self, 
            a=[], 
            e=None, 
            op=None, 
            mapping=None, 
            composition=None, 
            id=None, 
            range_query=True):

        self.n = len(a)
        self.bit_len = (len(a) - 1).bit_length()
        self.m = (1 << self.bit_len)

        self.a = [e] * (2*self.m)
        self.a[self.m:self.m+len(a)] = a
        self.e = e
        self.op = op
        self.mapping = mapping
        
        self.b = [id] * self.m
        self.id = id
        self.composition = composition

        self.range_query = range_query
        self._build()
        return
        
    def _build(self):
        for i in reversed(range(1, self.m)):
            self.__aggregate(i)
        return

    def __aggregate(self, i):
        self.a[i] = self.op(self.a[2*i], self.a[2*i+1])
        return

    def __propagate(self, i):
        self.__iapply(2*i, self.b[i])
        self.__iapply(2*i+1, self.b[i])
        self.b[i] = self.id

    def __bit_propagate(self, i, dx=0):
        for k in reversed(range(self.bit_len+1)):
            if ((i>>k)<<k) != i:
                self.__propagate((i+dx)>>k)

    def __bit_aggregate(self, i, dx=0):
        for k in range(self.bit_len+1):
            if ((i>>k)<<k) != i:
                self.__aggregate((i+dx)>>k)

    def apply(self, l, r, f):
        l += self.m
        r += self.m
        tmp = (l, r)
        self.__bit_propagate(l, 0)
        self.__bit_propagate(r, -1)
        while l < r:
            if l&1:
                self.__iapply(l, f)
                l += 1
            if r&1:
                self.__iapply(r-1, f)
            l >>= 1
            r >>= 1
        l, r = tmp
        self.__bit_aggregate(l, 0)
        self.__bit_aggregate(r, -1)
        return

    def __iapply(self, i, f):
        self.a[i] = self.mapping(f, self.a[i])
        if i < self.m:
            self.b[i] = self.composition(f, self.b[i])

    def prod(self, l, r=None):
        if r is None:
            return self[l]
        else:
            l += self.m
            r += self.m
            self.__bit_propagate(l, 0)
            self.__bit_propagate(r, -1)
            v = self.e
            dq = []
            while l < r:
                if l&1:
                    v= self.op(v, self.a[l])
                    dq.append(l)
                    l += 1
                if r&1:
                    v= self.op(v, self.a[r-1])
                    dq.append(r-1)
                l >>= 1
                r >>= 1
        return v

    def all_prod(self):
        return self.a[1]

    def __len__(self):
        return self.n

    def tolist(self):
        for i in range(1, self.m+1):
            self.__propagate(i)
        return self.a[self.m:]

    def __getitem__(self, i):
        # not yet
        return 



def op(x, y):
    return min(x, y)

def mapping(f, x):
    if f is None:
        return x
    return min(f, x)

def composition(f, g):
    if f is None:
        return g
    elif g is None:
        return f
    else:
        return min(f, g)
        