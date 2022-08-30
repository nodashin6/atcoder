class UnionFind():
    """
    Parameters:
    n : int
        size of list
    parents : int
        the parents of i-th node is `parents[i]`.
    """

    def __init__(self, n):
        
        self.n = n
        self.parents = [-1]*n

    def unite(self, x, y):
        
        if self.same(x, y):
            return
        px, py = self.find(x), self.find(y)
        if self.parents[px] > self.parents[py]:
            x, y = y, x
        self.parents[px] += self.parents[py]
        self.parents[py] = px

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


