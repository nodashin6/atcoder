from typing import Hashable

class LoopedList:
    """
    a --> b --> c --> d ---> e
                ^            |
                |            |
                +------------+
    
    Example
    -------
    >>> x = [0, 1, 2, 3, 4, 2, 3, 4, 2, 3, 4, ..., 2, 3, 4]
    >>> ll = LoopedList()
    >>> for xi in x:
    >>>     ll.append(xi)
    >>>     if ll.is_looped():
    >>>         break
    """
    MAX_ITERATION_COUNT = 1_000_000
    
    def __init__(self):
        self._a = []
        self.indexer = {}
        self._loop_start_index = None
        self._loop_length = None
        
    def is_looped(self) -> bool:
        """Check if the list contains a loop."""
        return self._loop_start_index is not None

    def append(self, __x: Hashable) -> None:
        """Append an element to the list."""
        if self.is_looped():
            raise self.LoopDetectedError("Loop detected. Cannot append more elements.")
        
        if __x in self.indexer:
            self._loop_start_index = self.indexer[__x]
            self._loop_length = len(self._a) - self._loop_start_index
        else:
            self._a.append(__x)
            self.indexer[__x] = len(self._a) - 1
            
    def clear(self) -> None:
        """Reset the LoopedList."""
        self._a = []
        self.indexer = {}
        self._loop_start_index = None
            
    def __contains__(self, value: Hashable) -> bool:
        """Check if the element is in the list."""
        return value in self.indexer
    
    def __len__(self) -> int:
        """Return the length of the list."""
        return len(self._a)
    
    def _generate_loop(self):
        """Generate the looped sequence."""
        i = 0
        for _ in range(self.MAX_ITERATION_COUNT):
            if i == len(self._a):
                i = self._loop_start_index
            yield self._a[i]
            i += 1

    def __iter__(self):
        """Iterate over the elements."""
        if self.is_looped():
            yield from self._generate_loop()
        else:
            yield from self._a
            
    def __getitem__(self, index: int) -> Hashable:
        """Get the element at the specified index."""
        if index < len(self._a):
            return self._a[index]
        elif self.is_looped():
            index -= self._loop_start_index
            index %= self._loop_length
            return self._a[self._loop_start_index + index]
        else:
            raise self.LoopNotDetectedError
        
    def split(self):
        """split to outer_loop and inner_loop"""
        if self.is_looped():
            return self._a[:self._loop_start_index], self._a[self._loop_start_index:]
        raise self.LoopNotDetectedError
    
    def tolist(self):
        return self._a
        
    class LoopDetectedError(Exception):
        """Exception raised for loop detection errors."""

    class LoopNotDetectedError(Exception):
        """Exception raised when attempting to access an element without a loop."""


# bit iteration
from itertools import product
for seq in product([0, 1], repeat=3):
    print(seq)
    # (0, 0, 0)
    # (0, 0, 1)
    # (0, 1, 0)
    # (0, 1, 1)
    # (1, 0, 0)
    # (1, 0, 1)
    # (1, 1, 0)
    # (1, 1, 1)


from itertools import permutations
for seq in permutations(range(3), r=2):
    print(seq)
    # (0, 1)
    # (0, 2)
    # (1, 0)
    # (1, 2)
    # (2, 0)
    # (2, 1)


from itertools import combinations
for seq in combinations(range(3), r=2):
    print(seq)
    # (0, 1)
    # (0, 2)
    # (1, 2)

