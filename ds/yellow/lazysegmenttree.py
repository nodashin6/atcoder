from collections.abc import Sequence
import math
import bisect
class LazySegmentTree(Sequence):
    """
    lazysegmenttree
    """
    INF = 1<<62
    AGGFUNCS = {
        'min': lambda a, b: (a, b)[a>b],
        'max': lambda a, b: (a, b)[a<b],
        'sum': lambda a, b: a + b,
        'gcd': math.gcd,
        'xor': lambda a, b: a ^ b
        }

    def __init__(self, a=[], default_value=INF, agg='min', mod=998244353):

        n = len(a)
        self.bit_len = (n - 1).bit_length()
        self.m = (1 << self.bit_len) - 1
        self.n = self.m + n

        self.sagg = agg
        self.agg = self.AGGFUNCS[agg]
        self.mod = mod

        self.DV = default_value
        self.a = [default_value]*self.m + a
        self.b = [0]*self.n  # add_value
        self.x = [1]*self.n  # is_add
        self._build()

        self.forsetattr = self.ForSetAttr()
        return
        
    def _build(self):
        self.rangetable = [[i, i+1] for i in range(self.m*2+1)]
        self.nchild = [0]*self.m + [1]*(self.n-self.m)
        for i in reversed(range(self.m)):
            l = (i<<1) + 1
            r = (i<<1) + 2
            self.rangetable[i][0] = self.rangetable[l][0]
            self.rangetable[i][1] = self.rangetable[r][1]
            if r < self.n:
                self.a[i] = self.agg(self.a[l], self.a[r])
                self.nchild[i] = self.nchild[l] + self.nchild[r]
            elif l < self.n:
                self.a[i] = self.a[l]
                self.nchild[i] = self.nchild[l]
            if self.mod is not None:
                self.a[i] %= self.mod


    def value_query(self, l=0, r=None):
        l += self.m
        r += self.m
        v = self.DV
        nodes = []
        dq = [0]
        while dq:
            # print(f'dq: {dq}')
            i = dq.pop()
            cl = (i<<1) + 1
            cr = (i<<1) + 2
            self._lazyupdate(i)

            il, ir = self.rangetable[i]
            im = (il+ir)>>1
            # print(f'(il, ir)=({il}, {ir})')
            if l <= il and ir <= r:
                # print('use')
                v = self.agg(v, self.a[i])
                continue
            elif r<=il or ir<=l:
                # print('out')
                # out of range
                continue
            else:
                # print('foward')
                dq.append((i<<1)+1)
                dq.append((i<<1)+2)
        # print(f'nodes: {nodes}')
        return v

    def _lazyupdate(self, i):
        
        if self.n <= i:
            return
        self.y = 1
        if self.sagg == 'sum':
            self.y = self.nchild[i]
        # print(f'(i, y) = ({i}, {self.y})')
        # a = ax + by
        self.a[i] = self.a[i] * self.x[i] + self.b[i] * self.y
        if self.mod is not None:
            self.a[i] %= self.mod
        l = (i<<1) + 1
        # print(f'lazy_update: i={i} -> ({l}, {l+1})')
        for j in (l, l+1):
            if j < self.n:
                self.b[j] *= self.x[i]
                self.b[j] += self.b[i]
                self.x[j] *= self.x[i]
                if self.mod is not None:
                    self.b[j] %= self.mod
        self.b[i] = 0
        self.x[i] = 1
        return

    def replace(self, l=0, r=None, v=None):
        self._update(l, r, v, x=0)

    def add(self, l=0, r=None, v=None):
        self._update(l, r, v, x=1)    

    def _update(self, l=0, r=None, v=None, x=None):
        l += self.m
        r += self.m
        # print(f'(l, r)=({l}, {r})')
        nodes = []
        dq = [0]
        while dq:
            # print(f'dq: {dq}')
            i = dq.pop()
            self._lazyupdate(i)

            il, ir = self.rangetable[i]
            # print(f'(il, ir)=({il}, {ir})')
            im = (il+ir)>>1
            if l <= il and ir <= r:
                # print('use')
                self.b[i] *= x
                self.b[i] += v
                self.x[i] = x
                if self.mod is not None:
                    self.b[i] %= self.mod
                self._lazyupdate(i)
                nodes.append(i)
                continue
            elif r<=il or ir<=l:
                # print('out')
                # out of range
                continue
            else:
                # print('foward')
                dq.append((i<<1)+1)
                dq.append((i<<1)+2)

        nodes.sort()
        # print('nodes:', nodes)
        self.backward(nodes)
        return
            
    def backward(self, nodes):
        nodes = nodes
        while nodes:
            # print(f'[backward] nodes: {nodes}')
            i = nodes.pop()
            if i > 0:
                i = self.iagg((i-1)>>1)
                bisect.insort(nodes, i)
    
    def iagg(self, i):
        # print(f'backward: i={i}')
        l = (i<<1) + 1
        r = (i<<1) + 2
        if r < self.n:
            # print(f'backward: i={i} <- agg(l, r)')
            self.a[i] = self.agg(self.a[l], self.a[r])
        else:
            # print(f'backward: i={i} <- l')
            self.a[i] = self.a[l]
        if self.mod is not None:
            self.a[i] %= self.mod
        return i

    def __getitem__(self, index):
        if type(index) is int:
            return self.a[index+self.m]
        if type(index) is slice:
            return self.forsetattr
        return

    def __setitem__(self, index, value):
        if type(value) is int:
            v, x = value, 0
        elif type(value) is tuple:
            v, x = value
        else:
            raise TypeError

        if type(index) is int:
            self._update(index, index+1, v, x)
        elif type(index) is slice:
            if index.step is None:
                self._update(index.start, index.stop, v, x)
            else:
                raise AttributeError("slice.step must be None")
        else:
            raise TypeError

    def __iadd__(self, index, value):
        self._update(index, index+1, value, x=1)

    def __isub__(self, index, value):
        self._update(index, index+1, -value, x=1)

    def __call__(self, l=0, r=None):
        return self.value_query(l=l, r=r)

    def __contains__(self, value: object) -> bool:
        return value in self.a[self.m:]
    def __len__(self):
        return self.n - self.m
    def __str__(self) -> str:
        return str(self.a[self.m:])
    def __repr__(self) -> str:
        return str(self.a[self.m:])

    class ForSetAttr():
        def __iadd__(self, v):
            if type(v) is int:
                return v, 1
            elif type(v) is tuple:
                v, x = v
                return v, x
        def __isub__(self, v):
            if type(v) is int:
                return -v, 1
            elif type(v) is tuple:
                v, x = v
                return -v, x