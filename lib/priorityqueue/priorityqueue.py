class VariablePriorityQueue():
    """
    The elements in heapq can be rewritten.

    Methods
    -------
    push(v, index)
        push the element.
    pop()
        pop an element.
    pushpop(v, index)
        push the element, then pop an element.

    Problems
    --------
    ABC267E: https://atcoder.jp/contests/abc267/submissions/34644562

    Notes
    -----
    [1] see about heapq algorithm
        https://github.com/python/cpython/blob/3.10/Lib/heapq.py
    """

    def __init__(self, n, a=None, INF=1<<62, has_already_heapified=False):
        """
        a : list[list[int, int]]
            a must be following 2-D list. 
            ----------------------------
            a = [[value_0, index_0],
                 [value_1, index_1],
                 ...,
                 [value_-1, index_-1]]
            -----------------------------
        """
        self.n = n
        self.INF = INF
        self.vals = [self.INF]*self.n
        self.locs = [None]*self.n
        self.hq = []
        if a:
            for i, (v, index) in enumerate(a):
                self.vals[index] = v
                self.locs[index] = i
                self.hq.append(index)
            if not has_already_heapified:
                self.heapify()

    def heapify(self):
        for i in reversed(range(len(self)//2)):
            self.forward(self.hq[i])

    def push(self, v, index):
        if self.locs[index] is None:
            self.vals[index], self.locs[index] = v, len(self.hq)
            self.hq.append(index)
            self.backward(0, index)
        else:
            # `index` already exsit in heapq. 
            if self.vals[index] < v:
                self.vals[index] = v
                self.forward(index)
            elif self.vals[index] > v:
                self.vals[index] = v
                self.backward(0, index)

    def pushpop(self, v, index):
        """
        Returns
        -------
        tuple
            (v, index)
        """
        if self.locs[index] is None:
            if self.hq and self.vals[self.hq[0]] < v:
                self.locs[index] = 0
                self.vals[index] = v
                index, self.hq[0] = self.hq[0], index
                v = self.vals[index]
                self.forward(self.hq[0])
            self.locs[index] = None
            self.vals[index] = self.INF
        else:
            # `index` already exsit in heapq. 
            self.push(v, index)
            v, index = self.pop()
        return v, index

    def forward(self, index):
        i = self.locs[index]
        startpos = i
        j = i*2 + 1
        while j < len(self):
            if j+1 < len(self) and  self.vals[self.hq[j+1]] < self.vals[self.hq[j]]:
                j += 1
            self.hq[i], self.locs[self.hq[j]] = self.hq[j], i
            i, j = j, j*2+1
        self.hq[i], self.locs[index] = index, i
        self.backward(startpos, index)

    def backward(self, startpos, index):
        j = self.locs[index]
        while j > startpos:
            i = (j-1)//2
            if self.vals[self.hq[i]] < self.vals[index]:
                break
            self.hq[j], self.locs[self.hq[i]] = self.hq[i], j
            j = i
        self.hq[j], self.locs[index] = index, j

    def pop(self):
        """
        Returns
        -------
        tuple
            (v, index)
        """
        index = self.hq.pop()
        self.locs[index] = 0
        if self.hq:
            self.hq[0], index = index, self.hq[0]
            self.forward(self.hq[0])
        self.locs[index] = None
        v, self.vals[index] = self.vals[index], self.INF
        return (v, index)

    def __len__(self):
        return len(self.hq)

    def __getitem__(self, key):
        index = self.hq[0]
        return self.vals[index], index