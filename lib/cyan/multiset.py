import bisect
class SortedMultiset():
    """

    Processing Time:
    ----------------
    n       time
    2*10^5  0.183 sec  (insert only, max_capacity=4096)
    """

    # ---------------------------------------------------
    # for debug
    # ---------------------------------------------------
    @classmethod
    def generate_sample(cls, v0, v1, n, rs=0):
        import random
        random.seed(rs)
        a = [random.randint(v0, v1) for _ in range(n)]
        return a
    # ---------------------------------------------------

    def __init__(self, max_capacity=4096):
        self.a = []
        self.MC = max_capacity

    def insert(self, v):
        i = self._bisect_row_index(v)
        if i == -1:
            if (not self.a) or len(self.a[0]) >= self.MC:
                self.a.insert(0, [v])
                return
        i = max(0, i)
        bisect.insort(self.a[i], v)
        if len(self.a[i]) > self.MC:
            m = self.MC//2
            self.a.insert(i+1, self.a[i][m:])
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

    def lower_bound(self, v):
        index = 0
        for i in range(len(self.a)):
            if self.a[i][0] > v:
                i -= 1
                break
            else:
                index += len(self.a[i])
        index -= len(self.a[i])
        index += bisect.bisect_left(self.a[i], v)
        return index

    def __getitem__(self, index):
        inner_index = 0
        for i in range(len(self.a)):
            if index < inner_index + len(self.a[i]):
                return self.a[i][index-inner_index]
            else:
                inner_index += len(self.a[i])
        return None