class UnionFind():
    """
    Parameters:
    n : int
        size of list
    parents : int
        the parents of i-th node is `parents[i]`.
    """

    def __init__(self, n, kind='auto'):
        """
        kind : str
            [left] parent of x <- parent of y
            [auto] compare the size of group of x and y  
        """
        self.n = n
        self.parents = [-1]*n
        self._parents_set = set(range(n))
        swap_methods = {
            'auto': self._swap_auto,
            'left': self._swap_left}
        self.swap = swap_methods[kind]
    
    def _swap_auto(self, x, y):
        if self.parents[x] > self.parents[y]:
            x, y = y, x
        return x, y

    def _swap_left(self, x, y):
        return x, y

    def unite(self, x, y):
        if self.same(x, y):
            return
        x, y = self.swap(self.find(x), self.find(y))
        self.parents[x] += self.parents[y]
        self.parents[y] = x
        self._parents_set.remove(y)

    def find(self, x):
        dq = []
        while self.parents[x] > -1:
            dq.append(x)
            x = self.parents[x]
        while dq:
            self.parents[dq.pop()] = x
        return x

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def get_size(self, x):
        return -self.parents[self.find(x)]
    
    def get_parents(self):
        return self._parents_set


