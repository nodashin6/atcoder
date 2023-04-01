class DirectedGraph():
    """
    Problems
    --------
    T90-21.
    """

    def __init__(self, n):
        """
        n: 頂点数
        """
        self.n = n
        self.G = [set([]) for _ in range(self.n)]
        self.G_rvrs = [set([]) for _ in range(self.n)]
        return

    def add_edge(self, a, b):
        if b not in self.G[a]:
            self.G[a].add(b)
            self.G_rvrs[b].add(a)
        return

    def scc(self):
        """
        SCC: Strongly Connected Component
        """
        self.seen = [0] * self.n
        self.stack = []
        for x in range(self.n):
            if not self.seen[x]:
                self._dfs(x)
        self.seen = [0] * self.n
        self.groups = []
        for x in reversed(self.stack):
            if not self.seen[x]:
                self._dfs_reversed(x)
        return self.groups

    def _dfs(self, x):
        dq = [x]
        while dq:
            x = dq.pop()
            if self.seen[x] == 0:
                dq.append(x)
                self.seen[x] = 1
                for y in self.G[x]:
                    if not self.seen[y]:
                        dq.append(y)
            elif self.seen[x] == 1:
                self.seen[x] = 2
                self.stack.append(x) 
        return

    def _dfs_reversed(self, x):
        dq = [x]
        group = set([x])
        while dq:
            x = dq.pop()
            if not self.seen[x]:
                self.seen[x] = 1
                for y in self.G_rvrs[x]:
                    if not self.seen[y]:
                        group.add(y)
                        dq.append(y)
        self.groups.append(group)
        return