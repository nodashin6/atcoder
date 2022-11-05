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
        強連結成分分解 (SCC)
        """
        
        i = 1
        # seen[i] = [はじめに訪れたとき (FORWARD), 最後に訪れたとき (BACKWARD)]
        self.seen = [[0]*2 for _ in range(self.n)]
        for x in range(self.n):
            if self.seen[x][0] == 0:
                i = self._dfs(x, G=self.G, i_init=i, backward=True)
        # 帰りがけの遅い順にソートする
        # seen[x][1]: x に訪れた最後のターン
        idxs = self._agsort([sb for _, sb in self.seen], reverse=True)
        
        # 帰りが遅い順に，辺を逆向きに張った有向グラフでDFS
        self.seen = [[0]*2 for _ in range(self.n)]
        self.groups = []
        i = 1
        for x in idxs:
            if self.seen[x][0] == 0:
                i = self._dfs(x, G=self.G_rvrs, i_init=i, backward=False, make_group=True)
        # DFSが途切れた時が強連結成分
        return self.groups

    def _dfs(self, x, G, i_init=0, backward=True, make_group=False):
        i = i_init
        dq = [x, x] if backward else [x]
        group = set([x])
        while dq:
            x = dq.pop()
            if self.seen[x][0] == 0:
                self.seen[x][0] = i
                for y in G[x]:
                    if self.seen[y][0] == 0:
                        group.add(y)
                        dq.append(y)
                        if backward:
                            dq.append(y)
                i += 1
            elif self.seen[x][1] == 0:
                self.seen[x][1] = i
                i += 1
        if make_group:
            self.groups.append(group)
        return i

    def _agsort(self, a, reverse=False):
        tmp = [[ai, i] for i, ai in enumerate(a)]
        tmp.sort(reverse=reverse)
        return [i for ai, i in tmp]