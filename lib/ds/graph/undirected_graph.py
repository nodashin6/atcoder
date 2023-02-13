from collections import deque
class UndirectedGraph():
    def __init__(self, n):
        self.n = n
        self.G = [[] for _ in range(n)]
        self.result = {}

    def add_edge(self, u, v):
        self.G[u].append(v)
        self.G[v].append(u)

    def dfs(self, start):
        seen = [-1]*self.n
        seen[start] = 0
        frm = [None]*self.n
        dq = [start]
        while dq:
            x = dq.pop()
            for y in self.G[x]:
                if seen[y] == -1:
                    seen[y] = seen[x] + 1
                    frm[y] = x
                    dq.append(y)
        self.result[start] = {
            'seen': seen,
            'frm': frm}
        return

    def bfs(self, start):
        seen = [-1]*self.n
        seen[start] = 0
        frm = [None]*self.n
        dq = deque([start])
        while dq:
            x = dq.popleft()
            for y in self.G[x]:
                if seen[y] == -1 or seen[y] > seen[x]+1:
                    seen[y] = seen[x] + 1
                    frm[y] = x
                    dq.append(y)
        self.result[start] = {
            'seen': seen,
            'frm': frm}
        return

    def search_route(self, start, end, kind='dfs'):
        if kind == 'dfs':
            self.dfs(start)
        elif kind == 'bfs':
            self.bfs(start)
        elif kind == None:
            pass
        else:
            raise ValueError(f"search_route kind must be one of 'dfs', 'bfs', or None (got '{kind}')")
        if self.result[start]['seen'][end] == -1:
            return None
        frm = self.result[start]['frm']
        route_rev = [end]
        while route_rev[-1] != start:
            route_rev.append(frm[route_rev[-1]])
        return route_rev[::-1]
