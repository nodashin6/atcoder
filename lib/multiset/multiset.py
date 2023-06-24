import math
from bisect import bisect_left, bisect_right, insort
from operator import __le__, __lt__
class SortedMultiset():
    """This is an sorted multiset using skip connection for index referencing.
    
    This Python program provides an implementation of a SortedMultiset, 
    which is an ordered collection (or multiset) of objects in which an object can 
    occur more than once. A multiset is similar to a set, but allows duplicate elements. 
    The SortedMultiset class maintains the elements in a sorted order, allowing efficient 
    operations like addition, removal, and searching of elements.

    Methods
    -------
    add(x)
        Adds an element x to the multiset.
    lower_bound(x)
        Returns the index of the first element which is not less than `x`.
    upper_bound(x)
        Returns the index of the first element which is greater than `x`.
    pop(index):
        Removes and returns the element at the specified index.
    discard(x):
        Removes the first item from the list which matches the specified value.
    count(x):
        Returns the number of times a specified item appears in the list.
    flatten():
        Converts a 2-D multiset into a 1-D list.
    """
    BUCKETSIZE = 256  # Never change this parameter
    K = (0, 3, 6)     # Never change this parameter. It means skip connection widths are 2^0, 2^3, 2^6.

    def __init__(self, a=None):
        """`a` must be 1-d list."""
        if a:
            self.size = len(a)
            self.a = self._build_buckets(a)
        else:
            self.size = 0
            self.a = []
        self._sizes = [[0], [0], [0]]
        self._calc_info()

    shape = property(doc="""return (num_bucket, bucket_size (avg))""")
    @shape.getter
    def shape(self):
        num_bucket = len(self.a)
        bucketsize = round(len(self)/len(self.a), 1) if self else 0.0
        return (num_bucket, bucketsize)

    def _build_buckets(self, a):
        for a0, a1 in zip(a[:-1], a[1:]):
            if a0 > a1:
                a = sorted(a)
                break
        k = max(self.BUCKETSIZE>>1, math.ceil(math.sqrt(self.size)*0.7))
        return [a[i*k:(i+1)*k] for i in range(-(-len(a)//k))]

    def _calc_info(self):
        """A Multiset is a collection where the size of elements 
        within a single bucket ideally falls between `_lo` and `_hi`. 
        A flag for uniformization (balancing) process is raised 
        when it exceeds `_excess`.
        """
        n = len(self.a)
        self._hi = max(self.BUCKETSIZE, n>>1)
        self._excess = self._hi << 1
        self._lo = self._hi >> 1

        if self:
            self._sizes[0] = list(map(len, self.a))
            self._sizes[1] = [sum(self._sizes[0][i:i+8]) for i in range(0, len(self.a), 8)]
            self._sizes[2] = [sum(self._sizes[1][i:i+8]) for i in range(0, len(self._sizes[1]), 8)]
            self._mins = [a[0] for a in self.a]
            self._maxs = [a[-1] for a in self.a]
        return

    def _balance(self):
        i = 0
        while i < len(self.a):
            if self._hi < len(self.a[i]):
                k = len(self.a[i])//self._lo + 1
                m = math.ceil(len(self.a[i]) / k) - 1
                for _ in range(k-1):
                    self.a.insert(i+1, self.a[i][~m:])
                    del self.a[i][~m:]
            elif 0 < i and (len(self.a[i-1]) + len(self.a[i])) < self._lo:
                self.a[i-1].extend(self.a.pop(i))
                continue
            i += 1
        return

    def _handle_empty_multiset(func):
        def inner_func(self, x):
            if self:
                func(self, x)
            else:
                self.a = [[x]]
                self.size = 1
                self._calc_info()
            return
        return inner_func
    
    def _update_min_max(self, i):
        if self.a[i]:
            self._mins[i] = self.a[i][0]
            self._maxs[i] = self.a[i][-1]

    @_handle_empty_multiset
    def add(self, x):
        """insert `x` regardless of existance of `x` in multiset. O(log N + N^0.5)"""
        i = max(0, bisect_left(self._mins, x) - 1)
        insort(self.a[i], x)
        self._update_min_max(i)
        self._countup(i)

    @_handle_empty_multiset
    def append(self, x):
        """append `x` regardless of existance of `x` in multiset. O(1)"""
        i = len(self.a) - 1
        self.a[i].append(x)
        self._update_min_max(i)
        self._countup(i)

    @_handle_empty_multiset
    def appendleft(self, x):
        """appendleft `x` regardless of existance of `x` in multiset. O(N^0.5)"""
        i = 0
        self.a[i].insert(0, x)
        self._update_min_max(i)
        self._countup(i)

    def _countup(self, i):
        self.size += 1
        for j in range(3):
            self._sizes[j][i>>self.K[j]] += 1
        if len(self.a[i]) > self._excess:
            self._balance()
            self._calc_info()
    
    def _countdown(self, i):
        self.size -= 1
        for j in range(3):
            self._sizes[j][i>>self.K[j]] -= 1
        if not len(self.a[i]):
            self.a.pop(i)
            self._calc_info()

    def pop(self, index=-1):
        """O(N^0.5)"""
        if not self: raise IndexError("pop from empty list")
        if index < 0:
            index += self.size
        if 0 <= index < len(self):
            if ~len(self.a[-1]) <= index - len(self):
                i = len(self.a) - 1
                j = index - len(self) + len(self.a[-1])
            elif index < len(self.a[0]):
                i = 0
                j = index
            else:
                i, j = self._loc(index)
            x = self.a[i].pop(j)
            self._update_min_max(i)
            self._countdown(i)
            return x
        else:
            raise IndexError

    def discard(self, x):
        """O(N^0.5)"""
        tmp = self._find(x)
        if tmp is not None:
            i, j = tmp
            self.a[i].pop(j)
            self._update_min_max(i)
            self._countdown(i)

    def lower_bound(self, x):
        """O(N^0.5)"""
        index = 0
        if self:
            i, index = self._iterate_row_index(x, __lt__)
            index += bisect_left(self.a[i], x)
        if index < len(self):
            return index
        else:
            return None

    def upper_bound(self, x):
        """O(log N)"""
        index = 0
        if self:
            i, index = self._iterate_row_index(x, __le__)
            index += bisect_right(self.a[i], x)
        if index < len(self):
            return index
        else:
            return None

    def count(self, x):
        """O(log N)"""
        hi = self.upper_bound(x)
        hi = hi if hi is not None else len(self)
        lo = self.lower_bound(x)
        lo = lo if lo is not None else len(self)
        return hi - lo

    def gt(self, x):
        """O(log N)"""
        if self:
            i = min(len(self.a)-1, bisect_right(self._maxs, x))
            if x < self.a[i][-1]:
                return self.a[i][bisect_right(self.a[i], x)]
        return None

    def ge(self, x):
        """O(log N)"""
        if self:
            i = min(len(self.a)-1, bisect_left(self._maxs, x))
            if x <= self.a[i][-1]:
                j = bisect_left(self.a[i], x)
                return self.a[i][j]
        return None

    def lt(self, x):
        """O(log N)"""
        if self:
            i = max(0, bisect_left(self._mins, x) - 1)
            if self.a[i][0] < x:
                return self.a[i][bisect_left(self.a[i], x) - 1]
        return None

    def le(self, x):
        """O(log N)"""
        if self:
            i = max(0, bisect_right(self._mins, x) - 1)
            if self.a[i][0] <= x:
                return self.a[i][bisect_right(self.a[i], x) - 1]
        return None
        
    def _loc(self, index):
        """O(N^0.5)"""
        i = 0
        for j in reversed(range(3)):
            k = self.K[j]
            _sizes = self._sizes[j]
            while i + (1<<k) < len(self.a) and index >= _sizes[i>>k]:
                index -= _sizes[i>>k]
                i += (1<<k)
        return i, index

    def _iterate_row_index(self, x, op):
        i, index = 0, 0
        for j in reversed(range(3)):
            k = self.K[j]
            _sizes = self._sizes[j]
            while i + (1<<k) < len(self.a) and op(self._mins[i + (1<<k)], x):
                index += _sizes[i>>k]
                i += (1<<k)
        return i, index
    
    def _find(self, x):
        """O(log N)"""
        if not self: return
        i = max(0, bisect_right(self._mins, x) - 1)
        j = bisect_left(self.a[i], x)
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
        """O(N^0.5)"""
        if index < 0:
            index += self.size
        if 0 <= index < len(self):
            i, j = self._loc(index)
            return self.a[i][j]
        raise IndexError

    def __setitem__(self, index, value):
        raise NotImplementedError("use pop(index) then add(value)")

    def __contains__(self, x):
        """O(log N)"""
        return False if self._find(x) is None else True

    def __str__(self):
        return self.flatten().__str__()

    def __repr__(self):
        return f"SortedMultiset({self.flatten()})"

    def __iter__(self):
        for bucket in self.a:
            for x in bucket:
                yield x

    def __reversed__(self):
        for bucket in reversed(self.a):
            for x in reversed(bucket):
                yield x
            
        
    # ----------------------------------------------------------------------
    # class methods
    @classmethod
    def count_inversion(cls, a=[], count_duplicate=False):
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
        sm = cls(a=[])
        sm.ope = sm.lower_bound if count_duplicate else sm.upper_bound
        cnt = 0
        for i, x in enumerate(a):
            v = sm.ope(x)
            v = v if v is not None else len(sm)
            cnt += len(sm) - v
            sm.add(x)
        return cnt
