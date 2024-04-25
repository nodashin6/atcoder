from collections.abc import Container
from collections import Counter
from heapq import heapify, heappop, heappush

"""
要テスト
"""

class RemovableHeap(Container):
    
    def __init__(self, a: list) -> None:
        self.a = a
        heapify(self.a)
        self._exists_counter = Counter(self.a)
        self._remove_counter = Counter()
        self._size = len(self.a)
    
    def __contains__(self, __x: object) -> bool:
        return 0 < self._exists_counter[__x]
    
    def __len__(self) -> int:
        return self._size
    
    def push(self, __x: object) -> None:
        heappush(self.a, __x)
        self._exists_counter[__x] += 1
        self._size += 1
        
    def pop(self) -> object:
        if not self.a:
            raise ValueError
        __x = heappop(self.a)
        if 0 < self._remove_counter[__x]:
            self._remove_counter[__x] -= 1
            return self.pop()
        else:
            self._exists_counter[__x] -= 1
            self._size -= 1
            return __x
        
    def remove(self, __x: object) -> None:
        if __x not in self:
            raise ValueError
        self._remove_counter[__x] += 1
        self._exists_counter[__x] -= 1
        self._size -= 1
        
    def __getitem__(self, index: int) -> object:
        raise NotImplementedError