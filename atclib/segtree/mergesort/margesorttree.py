class MergeSortTree:
    K = [15, 11, 6]
    W = [1 << k for k in K]
    
    def __init__(self, a: list[int]):
        self._a = [self._build(a, k) for k in self.K]
    
    def _build(self, __a: list[int], k: int) -> list[list[int]]:
        n = len(__a)
        m = ((n-1)>>k) + 1
        w = 1 << k
        return [sorted(__a[i*w: (i+1)*w]) for i in range(m)]
        
    def get_block_index(self, r: int):
        
        # index name:
        # 0 ----------- query -----------------> r       | N
        # l-----------------> i                          | N
        #                     i -----> j                 | N
        #                              j ------> r       | N
        ranges = [None] * 5
        l = 0
        for __i, k in enumerate(self.K):
            i = r >> k
            l = l >> k
            ranges[__i] = range(l, i)
            l = i << k
        ranges[-1] = range(l, r)
        return ranges