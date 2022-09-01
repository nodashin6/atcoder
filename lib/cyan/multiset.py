import bisect

class SortedSet(list):
    def insort(self, v): bisect.insort(self, v)
    def bisect_left(self, v): return bisect.bisect_left(self, v)
    def bisect_right(self, v): return bisect.bisect_right(self, r)

class SortedMultiset():
    """
    Processing Time:
    ----------------
    n       time
    2*10^5  0.183 sec  (insert only, max_capacity=4096)
    """

    def __init__(self, max_capacity=4096):
        self.a = []
        self.MC = max_capacity

    def insert(self, v):
        i = self._bisect_row_index(v)
        if i == -1:
            if (not self.a) or len(self.a[0]) >= self.MC:
                self.a.insert(0, SortedSet([v]))
                return
        i = max(0, i)
        self.a[i].insort(v)
        if len(self.a[i]) > self.MC:
            m = self.MC//2
            self.a.insert(i+1, SortedSet(self.a[i][m:]))
            del self.a[i][m:]

    def _bisect_row_index(self, v):
        l, r = -1, len(self.a)
        if self.a:
            while r-l > 1:
                m = (l+r)//2
                if self.a[m][0] <= v:
                    l = m
                else:
                    r = m
        return l