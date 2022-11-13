from collections import defaultdict
class UnionFind():
    """
    Parameters:
    n : int
        number of nodes
    parents : int
        the parents of i-th node is `parents[i]`.
    """

    def __init__(self, n):
        """
        n : int
            number of nodes
        """
        self.n = n
        self.nodes = set(range(n))
        self.parents = [-1]*self.n
        self._parents_set = set(range(n))
        return

    def unite(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x != y:
            self.parents[x] += self.parents[y]
            self.parents[y] = x
            self._parents_set.remove(y)
        return

    def _find(self, x):
        while self.parents[x] > -1:
            x = self.parents[x]
        return x

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

    def get_parents_size(self):
        return len(self.get_parents())

    def get_members(self):
        members = {x: set([]) for x in self.get_parents()}
        for x in self.nodes:
            members[self.find(x)].add(x)
        return members

    @classmethod
    def kruskal(cls, n, edges, inf=1<<62):
        uf = cls(n=n)
        uf.cost = 0
        for c, u, v in edges:
            if not uf.same(u, v):
                uf.unite(u, v)
                uf.cost += c
                if uf.get_parents_size() == 1:
                    break
        if uf.get_parents_size() == 1:
            return uf.cost
        else:
            return inf

    @classmethod
    def steiner(cls, n, edges, ignore_nodes=set([]), inf=1<<62):
        ignore_nodes = set(ignore_nodes)
        uf = cls(n=n)
        uf._parents_set = uf._parents_set.difference(ignore_nodes)
        uf.cost = 0
        for c, u, v in edges:
            if u in ignore_nodes or v in ignore_nodes:
                continue
            if not uf.same(u, v):
                uf.unite(u, v)
                uf.cost += c
            if uf.get_parents_size() == 1:
                break
        if uf.get_parents_size() == 1:
            return uf.cost
        else:
            return inf

    @classmethod
    def with_defaultdict(cls):

        class UnionFindWithDefaultDict(cls):

            def __init__(self):
                super().__init__(n=0)
                self.parents = defaultdict(lambda: -1)
                funcs = ['_find', 'find']
                for func in funcs:
                    exec(f"self.{func} = self.check_existance(self.{func})")

            def check_existance(self, func):
                def inner_func(*args):
                    for x in args:
                        if x not in self.nodes:
                            self.add_node(x)
                    return func(*args)
                return inner_func

            def add_node(self, x):
                self.n += 1
                self.nodes.add(x)
                self._parents_set.add(x)

        return UnionFindWithDefaultDict()