import bisect
class SortedMultiset():
    """
    Methods
    -------
    insert(x)
        insert value with allowing duplicates.
    add(x)
        Insert value if value is not in set.
        Checking the exsit of `x` makes `add` more costly than `insert`.
    lower_bound(x)
        Returns an 2d index of the first element in the range which does not 
        compare less than `x`.
    pop(i, j):
        Removes and returns the element at the specified index.
    popright():
        Removes and returns the last element.
    remove(x):
        Removes the first item from the list which matches the specified value.
    count(x):
        Returns the number of times the specified item appears in the list.
    flatten():
        Conver 2-d multiset to 1-d list, like np.arrray.ravel() or sum(seq, []).

    Operators
    ---------
    self < x
        count the numbers in the range which compares less than `x`.
    self <= x
        count the numbers in the range which does not compare greater than `x`
    self > x
        count the numbers in the range which compares greater than `x`.
    self >= x
        count the numbers in the range which does not compare less than `x`

    Processing Time
    ---------------
    condition: 
        insert only, max_capacity=4096
    N       Time
    1*10^5  ~0.1 sec
    2*10^5  <0.2 sec
    5*10^5  <0.5 sec
    1*10^6  <1.0 sec
    ***with PyPy3 on AtCoder***

    Problems
    --------
    [1] SortedMultiset
    - ABC217D: https://atcoder.jp/contests/abc217/submissions/34520676
    
    [2] count_inversion
    - ABC261F: https://atcoder.jp/contests/abc261/submissions/34520554

    [3] using as heapq
    Use push(value * -1) and popright().
    - ABC267E: https://atcoder.jp/contests/abc267/submissions/34655850
    """

    def __init__(self, a=[], max_capacity=4096):

        self.MC = max_capacity
        self.size = len(a)
        self.a = []
        if a:
            n_iter = self.size//self.MC + min(1, self.size%self.MC)
            for i in range(n_iter):
                l = i * self.MC
                r = l + self.MC
                self.a.append(a[l:r])

    def _bisect_row_index(self, v):
        l, r = 0, len(self.a)
        while r-l > 1:
            m = (l+r)//2
            if self.a[m][0] >= v:
                r = m
            else:
                l = m
        return l

    def _split(self, i):
        if len(self.a[i]) > self.MC:
            m = self.MC//2
            self.a.insert(i+1, self.a[i][m:])
            del self.a[i][m:]

    def insert(self, v):
        if not self.a:
            i = 0
            obj = self.a
            v = [v]
        else:
            i = self._bisect_row_index(v)
            obj = self.a[i]
        bisect.insort(obj, v)
        self.size += 1
        self._split(i)

    def add(self, x):
        if x not in self:
            self.insert(x)

    def lower_bound(self, x):
        i, j = 0, 0
        if self.a:
            i = self._bisect_row_index(x)
            j = bisect.bisect_left(self.a[i], x)
        return i, j

    def pop(self, i, j):
        i, j = self._reindex(i, j)
        x = self.a[i].pop(j)
        self.size -= 1
        if not self.a[i]:
            del self.a[i]
        return x

    def popright(self):
        x = self.a[-1].pop()
        self.size -= 1
        if not self.a[-1]:
            del self.a[-1]
        return x

    def remove(self, x):
        i, j = self.lower_bound(x)
        if j == len(self.a[i]):
            j = 0
            i += 1
        if self.iloc(i, j) == x:
            self.pop(i, j)
        else:
            raise ValueError("list.remove(x): x not in list")

    def replace(self, x, y):
        if not self.a:
            raise ValueError("list.replace(x): x not in list")
        i, j = self.lower_bound(x)
        if self.iloc(i, j) == x:
            self.a[i].pop(j)
            self.size -= 1
            if not self.a[i]:
                del self.a[i]
            self.insert(y)
        else:
            raise ValueError("list.remove(x): x not in list")

    def count(self, x):
        il, jl = self.lower_bound(x)
        ir, jr = self.lower_bound(x+1)
        cnt = 0
        while ir > il:
            cnt += jr
            ir -= 1
            jr = len(self.a[ir])
        cnt += jr - jl
        return cnt

    def flatten(self):
        fa = []
        for a in self.a:
            fa.extend(a)
        return fa


    # ----------------------------------------------------------------------
    # about location
    def __getitem__(self, key):
        if type(key) is tuple:
            i, j = key
            if i < 0: 
                raise IndexError("row index `i` must not be negative integer.")
            return self._get_value(*key)
        elif type(key) is int:
            if key < 0:
                key += self.size
            return self._get_value(0, key)
        elif type(key) is slice:
            raise IndexError("cannot use slice directly. Use `flatten` before slicing.")
        else:
            raise IndexError

    def _get_value(self, i, j):
        i, j = self._reindex(i, j)
        if j<0 or j>=len(self.a[i]):
            return None
        else:
            return self.a[i][j]

    def _reindex(self, i, j):
        if not self.a:
            return None, -1
        while j < 0 and i > 0:
            i, j = i-1, j+len(self.a[i-1])
        while j >= len(self.a[i]) and i+1 < len(self.a):
            i, j = i+1, j-len(self.a[i])
        return i, j

    def __len__(self):
        return self.size

    def __contains__(self, v):
        i, j = self.lower_bound(v)
        return self[i, j] == v

    def __le__(self, x):
        cnt = 0
        for a in self.a:
            if a[-1] <= x:
                cnt += len(a)
            else:
                cnt += bisect.bisect_right(a, x)
                break
        return cnt

    def __lt__(self, x):
        cnt = 0
        for a in self.a:
            if a[-1] < x:
                cnt += len(a)
            else:
                cnt += bisect.bisect_left(a, x)
                break
        return cnt

    def __ge__(self, x):
        return self.size - self.__lt__(x)

    def __gt__(self, x):
        return self.size - self.__le__(x)

    def iloc(self, i, j):
        """get value without reindex."""
        return self.a[i][j]
        
    # ----------------------------------------------------------------------
    # class methods
    @classmethod
    def count_inversion(cls, a, count_duplicate=False):
        """
        Processing Time
        ---------------
        conditions
            max_capacity=4096
        N       Time
        1*10^5  <0.2 sec
        2*10^5  <0.3 sec
        5*10^5  <0.8 sec
        1*10^6  ~1.6 sec
        ***with PyPy3 on AtCoder***
        """
        cls.ope = cls.__ge__ if count_duplicate else cls.__gt__
        sm = cls()
        cnt = 0
        for i, x in enumerate(a):
            cnt += sm.ope(x)
            sm.insert(x)
        return cnt