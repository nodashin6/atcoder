from collections import deque
class WeightedGraph():
    """
    Problem
    -------
    T90-13,
    """

    def __init__(self, n, m, inf=float('inf')):
        """
        n: 頂点数
        m: 辺の数
        """
        self.n = n
        self.m = m
        self.G = [{} for _ in range(self.n)]
        self.INF = inf
        return

    def add_edge(self, u, v, c):
        self.G[u][v] = c
        return

    def bfs(self, x):
        """
        x: start point
        """
        
        self.costs = [self.INF]*self.n
        self.costs[x] = 0
        dq = deque([x])
        while dq:
            x = dq.popleft()
            cx = self.costs[x]
            for y, cy in self.G[x].items():
                if self.costs[y] > cx + cy:
                    self.costs[y] = cx + cy
                    dq.append(y)
        return

    def floyd_warshall(self, D=None):
        if D is None:
            D = [[self.INF]*self.n for _ in range(self.n)]
            for u in range(self.n):
                D[u][u] = 0
                for v, w in self.G[u].items():
                    D[u][v] = w
        for m in range(self.n):
            for u in range(self.n):
                for v in range(self.n):
                    D[u][v] = min(
                        D[u][v],
                        D[u][m] + D[m][v])
        return D