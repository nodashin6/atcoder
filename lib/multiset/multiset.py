import math
import bisect
class SortedMultiset():
    """
    Methods
    -------
    insert(x)
        insert value with allowing duplicates.
    add(x)
        Insert value if `x` is not in set.
        Checking the exsit of `x` makes `add` more costly than `insert`.
    lower_bound(x)
        Returns an index of the first element in the range which does not 
        compare less than `x`.
    upper_bound(x)
        Returns an index of the first element in the range which
        compare greater than `x`.
    pop(index):
        Removes and returns the element at the specified index.
    discard(x):
        Removes the first item from the list which matches the specified value.
    count(x):
        Returns the number of times the specified item appears in the list.
    flatten():
        Convert 2-d multiset to 1-d list. It's like np.arrray.ravel() or sum(seq, []).

    Processing Time
    ---------------
    condition: 
        insert random integers
    N       Time
    2*10^5  <0.2 sec
    5*10^5  <0.5 sec
    1*10^6  <1.0 sec
    ***with PyPy3 on AtCoder***

    Problems
    --------
    [1] SortedMultiset
    - ABC217D: https://atcoder.jp/contests/abc217/submissions/36182242
    - ABC245E: https://atcoder.jp/contests/abc245/submissions/36198523
    [2] count_inversion
    - ABC261F: https://atcoder.jp/contests/abc261/submissions/36182408
    [3] using as variable heap deque
    - ABC267E: https://atcoder.jp/contests/abc267/submissions/36182517
    """

    def __init__(self, a=[]):
        """
        `a` must be 1-D list.
        """
        if a:
            self._build(a)
        else:
            self.a = []
            self.size = 0
            self.sizes = [0]
            self._calc_parameter()
        # stats
        self.cnt_rebuild = 0
        self.cnt_merge = 0
        self.cnt_average = 0

    shape = property(doc="""return (num_bucket, bucktsize (avg))""")
    @shape.getter
    def shape(self):
        num_bucket = len(self.a)
        bucketsize = round(len(self)/len(self.a), 1) if self else 0.0
        return (num_bucket, bucketsize)

    def _calc_parameter(self):
        n = len(self.a)
        self.Wb = n.bit_length()>>1
        self.W = 1 << self.Wb
        self.H = max(1, math.ceil(n/self.W))
        self.m2 = max(256, n>>1)
        self.m4 = self.m2 << 1
        self.m1 = self.m2 >> 1
        return 

    def _build(self, a):
        for a0, a1 in zip(a[:-1], a[1:]):
            if a0 <= a1:
                continue
            else:
                a = sorted(a)
                break
        self.size = len(a)
        K = max(128, math.ceil(math.sqrt(self.size)*0.7))
        self.a = [a[i*K:(i+1)*K] for i in range(-(-len(a)//K))]
        self._calc_parameter()
        self.sizes = self._calc_sizes()
        return

    def _rebuild(self):
        self.cnt_rebuild += 1
        if self.cnt_rebuild % 100 == 0:
            self._merge()
        self._calc_parameter()
        self.sizes = self._calc_sizes()
        return

    def _calc_sizes(self):
        sizes = [0] * self.H
        for i, length in enumerate(map(len, self.a)):
            sizes[i>>self.Wb] += length
        return sizes

    def _merge(self):
        i = 0
        while i+1 < len(self.a):
            if len(self.a[i]) + len(self.a[i+1]) < self.m1:
                self.a[i].extend(self.a.pop(i+1))
                self.cnt_merge += 1
                continue
            i += 1
        return 

    def _average(self):
        i = 0
        while i < len(self.a):
            if len(self.a[i]) > self.m2:
                self.a.insert(i+1, self.a[i][self.m1:])
                del self.a[i][self.m1:]
            i += 1
        return

    def add(self, x):
        """insert `x` if `x` doesn't exist in multiset. O(log N + N^0.5)"""
        if self:
            i = self._bisect_row_index(lambda bucket: bucket[0] <= x)
            j = bisect.bisect_left(self.a[i], x)
        else:
            self.a = [[]]
            i = 0
            j = 0
        if j < len(self.a[i]) and self.a[i][j] == x:
            return
        self.a[i].insert(j, x)
        self._countup_size(i)
        return

    def insert(self, x):
        """insert `x` regardless of existance of `x` in multiset. O(log N + N^0.5)"""
        if self:
            i = self._bisect_row_index(lambda bucket: bucket[0] <= x)
        else:
            self.a = [[]]
            i = 0
        bisect.insort(self.a[i], x)
        self._countup_size(i)
        return

    def append(self, x):
        """append `x` regardless of existance of `x` in multiset. O(1)"""
        if self:
            i = len(self.a) - 1
        else:
            self.a = [[]]
            i = 0
        self.a[i].append(x)
        self._countup_size(i)

    def appendleft(self, x):
        """appendleft `x` regardless of existance of `x` in multiset. O(N^0.5)"""
        if not self:
            self.a = [[]]
        i = 0
        self.a[i].insert(0, x)
        self._countup_size(i)

    def _countup_size(self, i):
        self.size += 1
        self.sizes[i>>self.Wb] += 1
        if len(self.a[i]) > self.m4:
            self._average()
            self._rebuild()
    
    def _countdown_size(self, i):
        self.size -= 1
        self.sizes[i>>self.Wb] -= 1
        if not len(self.a[i]):
            self.a.pop(i)
            self._rebuild()

    def pop(self, index=-1):
        """O(N^0.5)"""
        if not self: raise IndexError("pop from empty list")
        if index < 0:
            index += self.size
        i, j = self._loc(index)
        if j < len(self.a[i]):
            x = self.a[i].pop(j)
            self._countdown_size(i)
            return x
        raise IndexError

    def popleft(self):
        """O(N^0.5)"""
        if not self: raise IndexError("pop from empty list")
        x = self.a[0].pop(0)
        self._countdown_size(0)
        return x

    def discard(self, x):
        """O(log N + N^0.5)"""
        tmp = self._find(x)
        if tmp is not None:
            i, j = tmp
            self.a[i].pop(j)
            self._countdown_size(i)

    def lower_bound(self, x):
        """O(log N + N^0.25)"""
        if self: return self._lower_bound(x)

    def _lower_bound(self, x):
        i, index = self._iterate_row_index(lambda bucket: bucket[0] < x)
        return index + bisect.bisect_left(self.a[i], x)

    def upper_bound(self, x):
        """O(log N + N^0.25)"""
        if self: return self._upper_bound(x)

    def _upper_bound(self, x):
        i, index = self._iterate_row_index(lambda bucket: bucket[0] <= x)
        return index + bisect.bisect_right(self.a[i], x)

    def count(self, x):
        """O(log N + N^0.25)"""
        if self:
            return self._upper_bound(x) - self._lower_bound(x)
        else:
            return 0

    def gt(self, x):
        """O(log N)"""
        if not self: return
        i = self._bisect_row_index(lambda bucket: bucket[-1] <= x)
        if self.a[i][-1] <= x:
            i = min(i+1, len(self.a)-1)
        if x < self.a[i][-1]:
            return self.a[i][bisect.bisect_right(self.a[i], x)]

    def ge(self, x):
        """O(log N)"""
        if not self: return
        i = self._bisect_row_index(lambda bucket: bucket[-1] < x)
        if self.a[i][-1] < x:
            i = min(i+1, len(self.a)-1)
        if x <= self.a[i][-1]:
            return self.a[i][bisect.bisect_left(self.a[i], x)]

    def lt(self, x):
        """O(log N)"""
        if not self: return
        i = self._bisect_row_index(lambda bucket: bucket[0] < x)
        if self.a[i][0] < x:
            return self.a[i][bisect.bisect_left(self.a[i], x) - 1]

    def le(self, x):
        """O(log N)"""
        if not self: return
        i = self._bisect_row_index(lambda bucket: bucket[0] <= x)
        if self.a[i][0] <= x:
            return self.a[i][bisect.bisect_right(self.a[i], x) - 1]

    def _loc(self, index):
        """O(N^0.25)"""
        i = 0
        j = index
        while i + self.W < len(self.a) and j >= self.sizes[i>>self.Wb]:
            j -= self.sizes[i>>self.Wb]
            i += self.W
        while i + 1 < len(self.a) and j >= len(self.a[i]):
            j -= len(self.a[i])
            i += 1
        return i, j

    def _bisect_row_index(self, func):
        l, r = 0, len(self.a)
        while r-l > 1:
            m = (r+l)//2
            if func(self.a[m]):
                l = m
            else:
                r = m
        return l

    def _iterate_row_index(self, func):
        i, index = 0, 0
        while i + self.W < len(self.a) and func(self.a[i+self.W]):
            index += self.sizes[i>>self.Wb]
            i += self.W
        while i + 1 < len(self.a) and func(self.a[i+1]):
            index += len(self.a[i])
            i += 1            
        return i, index
    
    def _find(self, x):
        """O(log N)"""
        if not self: return
        i = self._bisect_row_index(lambda bucket: bucket[0] <= x)
        j = bisect.bisect_left(self.a[i], x)
        if j < len(self.a[i]) and self.a[i][j] == x:
            return i, j

    def flatten(self):
        a = []
        for ai in self.a:
            a.extend(ai)
        return a

    def tolist(self):
        return [bucket.copy() for bucket in self.a]

    def min(self):
        return self.a[0][0] if self else None

    def max(self):
        return self.a[-1][-1] if self else None

    def __len__(self):
        return self.size

    def __getitem__(self, index):
        return self._getitem(index)

    def _getitem(self, index):
        if index < 0:
            index += self.size
        if 0 <= index < len(self):
            i, j = self._loc(index)
            return self.a[i][j]
        raise IndexError

    def __setitem__(self, *args):
        raise NotImplementedError("use pop(index) then insert(value)")

    def __contains__(self, x):
        return self._contains(x)

    def _contains(self, x):
        return False if self._find(x) is None else True

    def __str__(self):
        a = self.flatten()
        if len(a) > 10:
            a = f'{str(a[:3])[:-1]}, ... , {str(a[-3:])[1:]}'
        return f"{a}"

    def __repr__(self):
        return f"SortedMultiset({self.flatten()})"
        
    # ----------------------------------------------------------------------
    # class methods
    @classmethod
    def count_inversion(cls, a, count_duplicate=False, inf=1<<62):
        """
        count inversion in numbers.

        Example
        -------
        >>>a = [3, 2, 2, 1]
        >>>SortedMultiset.count_inversion(a)
        5

          3    a[0] > (a[1], a[2], a[3])
        + 1    a[1] > (a[3])
        + 1    a[2] > (a[3])
        -------------------
        = 5

        >>>a = [3, 2, 2, 1]
        >>>SortedMultiset.count_inversion(a, count_duplicate=True)
        6

          3    a[0] >= (a[1], a[2], a[3])
        + 2    a[1] >= (a[2], a[3])
        + 1    a[2] >= (a[3])
        -------------------
        = 6

        Processing Time
        ---------------
        conditions
        N       Time
        1*10^5  <0.2 sec
        2*10^5  <0.3 sec
        5*10^5  <0.8 sec
        1*10^6  ~1.6 sec
        ***with PyPy3 on AtCoder***
        """
        sm = cls(a=[-inf])
        sm.ope = sm.lower_bound if count_duplicate else sm.upper_bound
        cnt = 0
        for i, x in enumerate(a):
            cnt += len(sm) - sm.ope(x)
            sm.insert(x)
        return cnt

    @classmethod
    def with_bitmask(cls, a=[], base=30):

        def wrap_input(self, class_func):
            def inner_func(x):
                x = (x[0]<<base) + x[1]
                v = class_func(x)
                return v
            return inner_func
        
        def wrap_output(self, class_func):
            def inner_func(*args):
                v = class_func(*args)
                x = [v>>base, v-((v>>base)<<base)]
                return x
            return inner_func

        b = [None]*len(a)
        for i in range(len(a)):
            b[i] = (a[i][0]<<base) + a[i][1]
        sm = SortedMultiset(a=b)
        sm.wrap_input = wrap_input
        sm.wrap_output = wrap_output
        input_funcs = [
            'add', 'insert', 'discard', '_contains', 'count', 
            'ge', 'gt', 'le', 'lt', 'lower_bound', 'upper_bound']
        for input_func in input_funcs:
            exec(f"sm.{input_func} = sm.wrap_input(sm, sm.{input_func})")
        output_funcs = [
            'pop', 'popleft', '_getitem']
        for output_func in output_funcs:
            exec(f"sm.{output_func} = sm.wrap_output(sm, sm.{output_func})")
        return sm