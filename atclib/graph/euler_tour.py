class EulerTour:
    """
    ABC294G
    """

    INF = 1<<60

    def __init__(self, n):
        self.n = n
        self.m = n - 1
        self.__graph = [set() for _ in range(self.n)]
        self.__weight = {}

    def __getitem__(self, index):
        return self.__graph[index]

    def add_weighted_edge(self, u, v, w):
        if u > v:
            u, v = v, u
        self.__graph[u].add(v)
        self.__graph[v].add(u)
        self.__weight[u<<30 | v] = w

    def get_weight(self, u, v):
        if u > v:
            u, v = v, u
        return self.__weight.get(u<<30 | v, None)
    
    def setup(self):
        
        first = [None] * self.n
        depth = [None] * self.n
        route = [None] * (2 * self.m + 1)
        dists = [None] * (2 * self.m)
        edges = {}

        u = 0
        i = 0
        depth[u] = 0
        first[u] = i
        stack = [(u, sorted(self[u], reverse=True))]
        while stack:
            u, gu = stack.pop()
            route[i] = u
            i += 1
            while gu:
                v = gu.pop()
                if first[v] is None:
                    first[v] = i
                    depth[v] = depth[u] + 1
                    self[v].remove(u)
                    stack.append((u, gu))
                    stack.append((v, sorted(self[v], reverse=True)))
                    break

        for i, (u, v) in enumerate(zip(route[:-1], route[1:])):
            w = self.get_weight(u, v)
            if depth[u] > depth[v]:
                w = -w
            dists[i] = w
            edges[u<<30 | v] = i

        self.first = first
        self.depth = depth
        self.route = route
        self.dists = dists
        self.edges = edges
        self._to_binary_indexed_tree()
        self._build_segment_tree_for_lca()
        return

    def _op(self, x, y):
        if x[0] < y[0]:
            return x
        else:
            return y

    def _build_segment_tree_for_lca(self):
        self.size = (1 << ((2*self.m).bit_length()+1)) - 1
        self.half = self.size >> 1

        minsg = [(self.INF, -1)] * self.size
        for i, u in enumerate(self.route, start=self.half):
            minsg[i] = (self.depth[u], u)
        for i in reversed(range(self.half)):
            l = (i<<1) + 1
            r = l + 1
            minsg[i] = self._op(minsg[l], minsg[r])
        self.minsg = minsg
        return

    def lca(self, u, v):
        l = self.first[u] + self.half
        r = self.first[v] + self.half
        if r < l:
            l, r = r, l
        r += 1
        lca = (self.INF, -1)
        while l < r:
            if (~l & 1):
                lca = self._op(lca, self.minsg[l])
                l += 1
            if (~r & 1):
                r -= 1
                lca = self._op(lca, self.minsg[r])
            l = (l-1)>>1
            r = (r-1)>>1
        return lca[1]

    def _to_binary_indexed_tree(self):
        len_ = len(self.dists)
        for i in range(len_):
            j = i + (~i & -~i)
            if j < len_:
                self.dists[j] += self.dists[i]
        return 

    def sum(self, u):
        r = self.first[u] - 1
        w = 0
        while 0 <= r:
            w += self.dists[r]
            r -= (~r & -~r)
        return w

    def update_weight(self, u, v, w):
        dw = w - self.get_weight(u, v)
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        i = self.edges[u<<30 | v]
        self._update_dists(i, dw)
        i = self.edges[v<<30 | u]
        self._update_dists(i, -dw)
        if u > v:
            u, v = v, u
        self.__weight[u<<30 | v] = w
        return

    def _update_dists(self, i, dw):
        len_ = len(self.dists)
        while i < len_:
            self.dists[i] += dw
            i += (~i & -~i)
        return
