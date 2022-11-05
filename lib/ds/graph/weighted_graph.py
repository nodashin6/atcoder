from collections import deque
class WeightedGraph():
    """
    Problem
    -------
    T90-13,
    """

    def __init__(self, n, m):
        """
        n: 頂点数
        m: 辺の数
        """

        self.n = n
        self.m = m
        self.G = [{} for _ in range(N)]

        self.INF = 10**15

        return

    def input(self, to_zero_index=True):

        for _ in range(self.m):
            a, b, c = map(int, input().split())
            if to_zero_index:
                a -= 1
                b -= 1
            self.G[a][b] = c
            self.G[b][a] = c

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