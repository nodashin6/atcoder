from typing import Union, Optional
from typing import List, Set, Dict, Tuple
from collections import deque
import heapq

class Graph:

    INF: int = 1 << 60
    BASE: int = 30

    def __init__(self, n: int, graph: List[Set[int]]=None) -> None:
        self.n = n
        self.__graph = [set() for _ in range(self.n)] if graph is None else graph
        self.__graph_T = None
        self.__weights = {}

    @property
    def T(self):
        if self.__graph_T is None:
            self._build_transpose_graph()
        return self.__graph_T
    
    @T.setter
    def T(self, *args):
        raise NotImplementedError
    
    def _build_transpose_graph(self) -> None:
        self.__graph_T = [set() for _ in range(self.n)]
        for u in range(self.n):
            for v in self[u]:
                self.__graph_T[v].add(u)
        return

    def __getitem__(self, index: int) -> set:
        if ~self.n <= index < self.n:
            return self.__graph[index]
        else:
            raise IndexError
        
    def __repr__(self):
        return (
            "Graph("
            f"n={self.n}, "
            f"graph={self.__graph}"
            ")"
        )

    def add_edge(self, u: int, v: int) -> None:
        self[u].add(v)
        return
    
    def add_weight(self, u: int, v: int, w: int) -> None:
        self.__weights[u<<self.BASE | v] = w

    def get_weight(self, u: int, v:int) -> Union[int, None]:
        return self.__weights.get(u<<self.BASE | v, None)
    
    def dfs(self, start: int, seen: Set[int]=None) -> List[int]:
        if seen is None:
            seen = set()
        return self._dfs(start, seen, graph=self)
    
    def _dfs(self, start: int, seen: Set[int], graph: List[Set[int]]) -> List[int]:
        stack = deque([start])
        seen.add(start)
        dfs_graph = {start: list(graph[start])}
        route = []
        while stack:
            u = stack.pop()
            route.append(u)
            while dfs_graph[u]:
                v = dfs_graph[u].pop()
                if v not in seen:
                    stack.append(u)
                    stack.append(v)
                    seen.add(v)
                    dfs_graph[v] = list(graph[v])
                    break
        return route
    
    def bfs(self, start: int, seen: Set[int]=None) -> Tuple[List[int], Dict[int, int]]:
        if seen is None:
            seen = set()
        return self._bfs(start, seen, graph=self)

    def _bfs(self, start: int, seen: Set[int], graph: List[Set[int]]) -> Tuple[List[int], Dict[int, int]]:
        queue = deque([start])
        seen.add(start)
        frm = {start: None}
        route = []
        while queue:
            u = queue.popleft()
            route.append(u)
            for v in graph[u]:
                if v not in seen:
                    queue.append(v)
                    seen.add(v)
                    frm[v] = u
        return route, frm
    

    # ------------------------------------------------------------------------------
    # Tree Graph
    # ------------------------------------------------------------------------------
    
    def calc_info(self, root: int=0):
        
        route = self.dfs(start=root)
        depth = [0] * self.n
        nodes = [1] * self.n
        seen = [0] * self.n
        seen[root] = 1
        for u, v in zip(route[:-1], route[1:]):
            if u == v:
                continue
            if not seen[v]:
                seen[v] = 1
                depth[v] = depth[u] + 1
            else:
                nodes[v] += nodes[u]
        return depth, nodes


    # ------------------------------------------------------------------------------
    # Directed Graph
    # ------------------------------------------------------------------------------
    
    def topological_sort(self) -> list:

        sorted_list = []
        graph = [graph_u.copy() for graph_u in self]
        stack = deque([u for u, graph_u in enumerate(self) if not graph_u])
        while stack:
            u = stack.pop()
            sorted_list.append(u)
            for v in self.T[u]:
                graph[v].remove(u)
                if not graph[v]:
                    stack.append(v)
        return sorted_list

    def scc(self) -> Dict[int, Set[int]]:
        
        seen = set()
        stack = []
        for u in range(self.n):
            if u not in seen:
                stack += self.dfs(start=u, seen=seen)
        seen = set()
        groups = {}
        for u in reversed(stack):
            if u not in seen:
                groups[u] = set(self._dfs(start=u, seen=seen, graph=self.T))
        return groups


    # ------------------------------------------------------------------------------
    # Weighted Graph
    # ------------------------------------------------------------------------------

    def dijkstra(self, start: int, dist: List[int]=None, graph: List[Set[int]]=None) -> List[int]:

        if dist is None:
            dist = [self.INF] * self.n
        if graph is None:
            graph = self
        dist[start] = 0
        hq = [start]
        while hq:
            x = heapq.heappop(hq)
            d_u, u = x>>60, x&(self.INF-1)
            if d_u > dist[u]:
                continue
            for v in graph[u]:
                w_uv = self.get_weight(u, v)
                if dist[v] > d_u + w_uv:
                    dist[v] = d_u + w_uv
                    hq.append(dist[v]<<60 | v)
        return dist
    
    def zero_one_bfs(self, start: int) -> List[int]:

        def divide(u):
            graph_u = [[], []]
            for v in self[u]:
                d_uv = self.get_weight(u, v)
                graph_u[d_uv].append(v)
            return graph_u

        seen = {start}
        bfs_graph = {start: divide(start)}
        dist = [self.INF] * self.n
        dist[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            while bfs_graph[u][0]:
                v = bfs_graph[u][0].pop()
                if v not in seen:
                    seen.add(v)
                    dist[v] = dist[u]
                    queue.appendleft(v)
                    bfs_graph[v] = divide(v)
            while bfs_graph[u][1]:
                v = bfs_graph[u][1].pop()
                if v not in seen:
                    seen.add(v)
                    dist[v] = dist[u] + 1
                    queue.append(v)
                    queue.append(u)
                    bfs_graph[v] = divide(v)
                    break
        return dist
    
    def floyd_warshall(self, matrix: List[List[int]]=None):

        if matrix is None:
            matrix = [[self.INF]*self.n for _ in range(self.n)]
            for u in range(self.n):
                matrix[u][u] = 0
                for v in self[u]:
                    matrix[u][v] = self.get_weight(u, v)
        for m in range(self.n):
            for u in range(self.n):
                for v in range(self.n):
                    matrix[u][v] = min(
                        matrix[u][v],
                        matrix[u][m] + matrix[m][v])
        return matrix