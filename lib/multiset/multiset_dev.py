import operator
import bisect
class SortedMultisetDev():
    """
    No Docstring
    """

    BUCKETSIZE = 200
    def __init__(self, a=[], counter=True, bitmask=None):
        """
        Parameters:
        a : list
        counter : bool, default=True
        bitmask : None, int
        """
        # setting functions
        self.wrap_funcs = {
            'get': {
                'input_value': [],
                'output_value': []
            },
            'set': {
                'input_value': [],
                'input_bucket': [],
                'output_value': [],
                'output_bucket': []
            }
        }
        self._set_counter() if counter else None
        self._set_bitmask(bitmask) if bitmask is not None else None
        
        if a:
            self._build(a)
        else:
            self.a = [[]]
            self.size = 0
        self._calc_parameter()
        self._calc_sizes()
        self.stats = {'rebuild': 0, 'merge': 0, 'smooth': 0}

    shape = property(doc="""return (num_bucket, bucket_size (avg))""")
    @shape.getter
    def shape(self):
        num_bucket = len(self.a)
        bucket_size = round(len(self)/len(self.a)) if self else 0
        return (num_bucket, bucket_size)

    def _calc_parameter(self):
        n = len(self.a)
        self.skip_bit = n.bit_length()>>1
        self.skip_len = 1 << self.skip_bit
        self.m2 = max(self.BUCKETSIZE, n>>1)
        self.m4 = self.m2 << 1
        self.m1 = self.m2 >> 1
        return 

    def flatten(self):
        return [self.__get_output_value(x) for x in sum(self.a, [])]
    def __len__(self):
        return self.size
    def __repr__(self):
        return f"SortedMultiset({self.flatten().__repr__()})"
    def __str__(self):
        a = self.flatten()
        if len(a) > 10:
            a = f'{str(a[:3])[:-1]}, ... , {str(a[-3:])[1:]}'
        return f"SortedMultiset({a})"

    # ----------------------------------------------------------------------
    # bucket operations
    def _build(self, a):
        a = [self.__set_input_value(x) for x in a]
        if not all([a0 <= a1 for a0, a1 in zip(a[:-1], a[1:])]):
            a = sorted(a)
        K = max(self.BUCKETSIZE, int((len(a)**0.5)*0.667))
        self.a = [a[i*K:(i+1)*K] for i in range(-(-len(a)//K))]
        self.size = len(a)
        for i, bucket in enumerate(self.a):
            for x in bucket:
                self.__set_input_bucket(i, x)
        return

    def _rebuild(self):
        self.stats['rebuild'] += 1
        if self.stats['rebuild'] % 100 == 0:
            self._merge()
        self._calc_parameter()
        self._calc_sizes()
        return

    def _calc_sizes(self):
        self.sizes = [0] * max(1, -(-len(self.a)//self.skip_len))
        for i, length in enumerate(map(len, self.a)):
            self.sizes[i>>self.skip_bit] += length
        return

    def _merge(self):
        i = 1
        while i < len(self.a):
            if len(self.a[i-1]) + len(self.a[i]) < self.m1:
                self._imerge(i)
                i -= 1
            i += 1
        return 

    def _imerge(self, i):
        self.a[i-1].extend(self.a.pop(i))
        self.stats['merge'] += 1
        return 

    def _smooth(self):
        i = 0
        while i < len(self.a):
            if len(self.a[i]) > self.m2:
                self._ismooth(i)
            i += 1
        return

    def _ismooth(self, i):
        self.a.insert(i+1, self.a[i][self.m1:])
        del self.a[i][self.m1:]
        self.stats['smooth'] += 1
        return

    def _countup_bucketsize(self, i, v=1):
        self.size += v
        self.sizes[i>>self.skip_bit] += v
        if v > 0:
            if len(self.a[i]) > self.m4:
                self._smooth()
                self._rebuild()
        else:
            if not len(self.a[i]):
                self._pop_bucket(i)
                self._rebuild()

    def _pop_bucket(self, i):
        if self:
            self.a.pop(i)

    # ----------------------------------------------------------------------
    # element operations
    def __get_input_value(self, x):
        for func in self.wrap_funcs['get']['input_value']:
            x = func(x)
        return x
    def __set_input_value(self, x):
        for func in self.wrap_funcs['set']['input_value']:
            x = func(x)
        return x
    def __set_input_bucket(self, i, x):
        for func in self.wrap_funcs['set']['input_bucket']:
            i, x = func(i, x)
        return i, x
    def __get_output_value(self, x):
        for func in self.wrap_funcs['get']['output_value']:
            x = func(x)
        return x
    def __set_output_value(self, x):
        for func in self.wrap_funcs['set']['output_value']:
            x = func(x)
        return x
    def __set_output_bucket(self, i, x):
        for func in self.wrap_funcs['set']['output_bucket']:
            i, x = func(i, x)
        return i, x

    def _insert(self, i, j, x):
        i, x = self.__set_input_bucket(i, x)
        self.a[i].insert(j, x)
        return

    def _pop(self, i, j):
        x = self.a[i].pop(j)
        i, x = self.__set_output_bucket(i, x)
        return x

    def add(self, x):
        """bisect insert `x` regardless of existance of `x` in multiset. O(log N + N^0.5)"""
        x = self.__set_input_value(x)
        i = self._bisect_row_index(lambda bucket: bucket[0] <= x)
        j = bisect.bisect_right(self.a[i], x)
        self._insert(i, j, x)
        self._countup_bucketsize(i)
        return

    def append(self, x):
        """append `x` regardless of existance of `x` in multiset. O(1)"""
        x = self.__set_input_value(x)
        i = len(self.a) - 1
        j = len(self.a[i])
        self._insert(i, j, x)
        self._countup_bucketsize(i)
        return

    def appendleft(self, x):
        """appendleft `x` regardless of existance of `x` in multiset. O(N^0.5)"""
        x = self.__set_input_value(x)
        i = 0
        j = 0
        self._insert(i, j, x)
        self._countup_bucketsize(i)
        return

    def check_index(self, index):
        if not self:
            raise IndexError
        if index < 0:
            index += len(self)
        if 0 <= index < len(self):
            return index
        raise IndexError

    def pop(self, index=-1):
        """O(N^0.5)"""
        index = self.check_index(index)
        i, j = self._loc(index)
        x = self._pop(i, j)
        x = self.__set_output_value(x)
        self._countup_bucketsize(i, v=-1)
        return x

    def popleft(self):
        """O(N^0.5)"""
        i = 0
        j = 0
        x = self._pop(i, j)
        x = self.__set_output_value(x)
        self._countup_bucketsize(0, v=-1)
        return x

    def popright(self):
        """O(N^0.5)"""
        i = len(self.a)-1
        j = -1
        x = self._pop(i, j)
        x = self.__set_output_value(x)
        self._countup_bucketsize(i, v=-1)
        return x

    def discard(self, x):
        """O(log N + N^0.5)"""
        tmp = self._findloc(x)
        if tmp is not None:
            i, j = tmp
            x = self._pop(i, j)
            x = self.__set_output_value(x)
            self._countup_bucketsize(i, v=-1)

    def _bound_func(ope, not_found=None):
        def inner_func(self, x):
            """O(log N + N^0.25)"""
            x = self.__get_input_value(x)
            i, index = self._iterate_row_index(lambda bucket: ope(bucket[0], x))
            index += bisect.bisect_left(self.a[i], x)
            if index < len(self):
                return index
            else:
                if not_found is None:
                    return None
                elif not_found is int:
                    return index
        return inner_func
    lower_bound = _bound_func(ope=operator.lt)
    _lower_bound = _bound_func(ope=operator.lt, not_found=int)
    upper_bound = _bound_func(ope=operator.le)
    _upper_bound = _bound_func(ope=operator.le, not_found=int)

    def count(self, x):
        """O(log N + N^0.25)"""
        return self._upper_bound(x) - self._lower_bound(x)

    def gt(self, x):
        """O(log N)"""
        if not self: return
        x = self.__get_input_value(x)
        i = self._bisect_row_index(lambda bucket: bucket[-1] <= x)
        if self.a[i][-1] <= x:
            i = min(i+1, len(self.a)-1)
        if x < self.a[i][-1]:
            x = self.a[i][bisect.bisect_right(self.a[i], x)]
            return self.__get_output_value(x)

    def ge(self, x):
        """O(log N)"""
        if not self: return
        x = self.__get_input_value(x)
        i = self._bisect_row_index(lambda bucket: bucket[-1] < x)
        if self.a[i][-1] < x:
            i = min(i+1, len(self.a)-1)
        if x <= self.a[i][-1]:
            x = self.a[i][bisect.bisect_left(self.a[i], x)]
            return self.__get_output_value(x)

    def lt(self, x):
        """O(log N)"""
        if not self: return
        x = self.__get_input_value(x)
        i = self._bisect_row_index(lambda bucket: bucket[0] < x)
        if self.a[i][0] < x:
            x = self.a[i][bisect.bisect_left(self.a[i], x) - 1]
            return self.__get_output_value(x)

    def le(self, x):
        """O(log N)"""
        if not self: return
        x = self.__get_input_value(x)
        i = self._bisect_row_index(lambda bucket: bucket[0] <= x)
        if self.a[i][0] <= x:
            x = self.a[i][bisect.bisect_right(self.a[i], x) - 1]
            return self.__get_output_value(x)
        
    def _loc(self, index):
        """O(N^0.25)"""
        i = 0
        j = index
        while i + self.skip_len < len(self.a) and j >= self.sizes[i>>self.skip_bit]:
            j -= self.sizes[i>>self.skip_bit]
            i += self.skip_len
        while i + 1 < len(self.a) and j >= len(self.a[i]):
            j -= len(self.a[i])
            i += 1
        return i, j

    def _bisect_row_index(self, func, l=0):
        l, r = l, len(self.a)
        while r-l > 1:
            m = (r+l)>>1
            if func(self.a[m]):
                l = m
            else:
                r = m
        return l

    def _iterate_row_index(self, func):
        i, index = 0, 0
        while i + self.skip_len < len(self.a) and func(self.a[i+self.skip_len]):
            index += self.sizes[i>>self.skip_bit]
            i += self.skip_len
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
            return True

    def _findloc(self, x):
        """O(log N)"""
        if not self: return
        i = self._bisect_row_index(lambda bucket: bucket[0] <= x)
        j = bisect.bisect_left(self.a[i], x)
        if j < len(self.a[i]) and self.a[i][j] == x:
            return i, j

    def __getitem__(self, index):
        index = self.check_index(index)
        i, j = self._loc(index)
        return self.__get_output_value(self.a[i][j])

    def __contains__(self, x):
        x = self.__get_input_value(x)
        return False if self._find(x) is None else True

    def __iter__(self):
        for bucket in self.a:
            for x in bucket:
                yield self.__get_output_value(x)
    def min(self): return self.__get_output_value(self.a[0][0]) if self else None
    def max(self): return self.__get_output_value(self.a[-1][-1]) if self else None

    def __setitem__(self, *args):
        raise NotImplementedError("use pop(index) then insert(value)")

    # ----------------------------------------------------------------------
    # counter
    def _set_counter(self):
        self.counter = {}
        self.wrap_funcs['set']['input_value'].append(self.countup_counter)
        self.wrap_funcs['set']['output_value'].append(self.countdown_counter)
        self._wrap_existancefuncs_for_counter()
        return

    def countup_counter(self, x):
        if x in self.counter:
            self.counter[x] += 1
        else:
            self.counter[x] = 1
        return x

    def countdown_counter(self, x):
        if x in self.counter:
            self.counter[x] -= 1
        else:
            raise ValueError
        return x

    def _wrap_existancefuncs_for_counter(self):
        def _find(x):
            """O(1)"""
            return self.counter.get(x, 0) > 0
        def count(x):
            """O(1)"""
            self.__get_input_value(x)
            return self.counter.get(x, 0)
        self._find = _find
        self.count = count
        return

    # ----------------------------------------------------------------------
    # bitmask
    def _set_bitmask(self, base):
        self.base = base
        self.wrap_funcs['get']['input_value'].insert(0, self.toint)
        self.wrap_funcs['set']['input_value'].insert(0, self.toint)
        self.wrap_funcs['get']['output_value'].append(self.totuple)
        self.wrap_funcs['set']['output_value'].append(self.totuple)
        return
    def toint(self, x):
        v = (x[0]<<self.base) + x[1]
        return v
    def totuple(self, v):
        x = (v>>self.base, v-((v>>self.base)<<self.base))
        return x

    # ----------------------------------------------------------------------
    # class methods
    @classmethod
    def count_inversion(cls, a=[], count_duplicate=False, bitmask=None):
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
        sm = cls(a=[], counter=False, bitmask=bitmask)
        sm.ope = sm._lower_bound if count_duplicate else sm._upper_bound
        cnt = 0
        for i, x in enumerate(a):
            cnt += len(sm) - sm.ope(x)
            sm.add(x)
        return cnt
