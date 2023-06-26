import math
from bisect import bisect_left, bisect_right, insort
from operator import __le__, __lt__
from typing import Any, Tuple, List, Callable, Iterator, Optional, TypeVar, Generic
class Comparable:
    """Comparable class for comparison operations.

    This class provides comparison methods but raises NotImplementedError for each method
    since the Protocol feature is not available in this Python version.

    To use this class, derive from it and implement the comparison methods accordingly.
    """
    def __lt__(self: Any, other: Any) -> bool: raise NotImplemetedError
    def __le__(self: Any, other: Any) -> bool: raise NotImplemetedError
    def __eq__(self: Any, other: Any) -> bool: raise NotImplemetedError
    def __ne__(self: Any, other: Any) -> bool: raise NotImplemetedError
    def __ge__(self: Any, other: Any) -> bool: raise NotImplemetedError
    def __gt__(self: Any, other: Any) -> bool: raise NotImplemetedError
T = TypeVar('T', bound=Comparable)
BucketIndex = int
ElementIndex = int
class SortedMultiset(Generic[T]):
    """This is an sorted multiset using skip connection for index referencing.
    
    This Python program provides an implementation of a SortedMultiset, 
    which is an ordered collection (or multiset) of objects in which an object can 
    occur more than once. A multiset is similar to a set, but allows duplicate elements. 
    The SortedMultiset class maintains the elements in a sorted order, allowing efficient 
    operations like addition, removal, and searching of elements.

    Attributes
    ----------
    BUCKETSIZE : int
        The optimal size for the buckets. Never change this parameter.
    K : Tuple[int, int, int]
        Defines the skip connection widths. Never change this parameter.

    Methods
    -------
    add(x)
        Adds an element x to the multiset.
    lower_bound(x)
        Returns the index of the first element which is not less than `x`.
    upper_bound(x)
        Returns the index of the first element which is greater than `x`.
    pop(index):
        Removes and returns the element at the specified index.
    discard(x):
        Removes the first item from the list which matches the specified value.
    count(x):
        Returns the number of times a specified item appears in the list.
    flatten():
        Converts a 2-D multiset into a 1-D list.

    Notes
    -----
    In this implementation, the multiset is stored as a jagged array of buckets,
    where each bucket has a fixed maximum size. Random access to individual elements
    in the jagged array would require iterating through the number of buckets,
    resulting in a time complexity of O(√N) for these operations.

    However, to optimize access, the implementation uses skip connections during
    bucket index iteration. These skip connections occur at multiples of 64 and 8.
    For example, to reach the 1024th bucket, instead of iterating 1023 times,
    it can be reached in a total of 29 iterations: 999 = 64 * 15 + 8 * 7 + 1 * 7.

    By leveraging these skip connections, the implementation achieves efficient
    access to individual elements in the multiset.
    """
    BUCKETSIZE: int = 256                # Never change this parameter
    K: Tuple[int, int, int] = (0, 3, 6)  # Never change this parameter. It means skip connection widths are 2^0, 2^3, 2^6.
    def __init__(self, a: Optional[List[T]]=None):
        """Initialize a SortedMultiset.

        Parameters
        ----------
        a : Optional[List[T]], optional
            A 1-dimensional list of elements to initialize the SortedMultiset, by default None.

        Raises
        ------
        TypeError
            If the elements in `a` do not satisfy the Comparable protocol.

        Notes
        -----
        - The elements in `a` must satisfy the Comparable protocol, i.e., they must implement the comparison operators (<, <=, >, >=, ==, !=).
        - If `a` is not provided, an empty SortedMultiset is created.
        """
        if a:
            self.size = len(a)
            self.a = self._build_buckets(a)
        else:
            self.size = 0
            self.a = []
        self._sizes = [[0], [0], [0]]
        self._calc_info()
    
    @property
    def shape(self) -> Tuple[int, float]:
        """Return the shape of the multiset.

        Returns
        -------
        Tuple[int, float]
            A tuple of two values:
            - num_buckets: The number of buckets in the multiset.
            - bucket_size: The average size of the buckets in the multiset.

        Notes
        -----
        The shape of the multiset provides information about the distribution of elements
        among the buckets. It consists of the number of buckets and the average size of the
        buckets.
        """
        num_buckets = len(self.a)
        bucketsize = round(len(self)/num_buckets, 1) if num_buckets != 0 else 0.0
        return (num_buckets, bucketsize)
    
    def _build_buckets(self, a: List[T]) -> List[List[T]]:
        """Build the buckets for the multiset.

        This method constructs the buckets for the multiset based on the input list `a`.
        The elements in the list are divided into buckets of approximately equal size.
        If the input list is already sorted in non-decreasing order, the buckets are
        directly constructed based on the input list. Otherwise, the input list is sorted
        first before dividing it into buckets.

        Parameters
        ----------
        a : Optional[List[T]]
            The input list of elements to be divided into buckets.

        Returns
        -------
        List[List[T]]
            The list of buckets containing the elements from the input list.

        Examples
        --------
        >>> s = SortedMultiset()
        >>> a = s._build_buckets(list(range(1000)))
        >>> list(map(len, a))
        [128, 128, 128, 128, 128, 128, 128, 104]
        """
        for a0, a1 in zip(a[:-1], a[1:]):
            if a0 > a1:
                a = sorted(a)
                break
        _m = max(self.BUCKETSIZE>>1, math.ceil(math.sqrt(len(a))*0.7))
        k = min(max(1, math.ceil(len(a) / _m)), 1200)
        p, q = divmod(len(a), k)
        ii = [0] + [p] * (k-q) + [p+1] * q
        new_a = []
        for i in range(k):
            ii[i+1] += ii[i]
            new_a.append(a[ii[i]: ii[i+1]])
        return new_a

    def _calc_info(self) -> None:
        """Calculate and update important information for efficient random access.

        The `_calc_info` method calculates and updates several attributes that are crucial
        for efficient random access operations in the multiset.

        A Multiset is a collection where the size of elements 
        within a single bucket ideally falls between `_lo` and `_hi`. 
        A flag for uniformization (balancing) process is raised 
        when it exceeds `_excess`.

        Additionally, the method updates the following attributes based on the current state
        of the multiset:

        - `_sizes`: A list that holds the sizes of buckets at different aggregation levels.
        It is used to efficiently calculate the random access time complexity.
        - `_mins`: A list of the minimum values within each bucket.
        It provides easy access to the minimum value of each bucket and gets updated
        whenever elements are added or removed from the multiset.
        - `_maxs`: A list of the maximum values within each bucket.
        Similar to `_mins`, it allows quick access to the maximum value of each bucket
        and gets updated accordingly during element manipulation.

        Note: The `_mins` and `_maxs` attributes store 1-dimensional information instead
        of accessing `self.a[i][0]` or `self.a[i][-1]` directly. This design choice improves
        the efficiency of various methods that frequently rely on these values.

        Returns
        -------
        None
        """
        n = len(self.a)
        self._hi = max(self.BUCKETSIZE, n>>1)
        self._excess = self._hi << 1
        self._lo = self._hi >> 1

        if self:
            self._sizes[0] = list(map(len, self.a))
            self._sizes[1] = [sum(self._sizes[0][i:i+8]) for i in range(0, len(self.a), 8)]
            self._sizes[2] = [sum(self._sizes[1][i:i+8]) for i in range(0, len(self._sizes[1]), 8)]
            self._mins = [a[0] for a in self.a]
            self._maxs = [a[-1] for a in self.a]

    def _balance(self) -> None:
        """Perform balancing of the multiset buckets. O(√N)

        The balancing process aims to maintain a uniform distribution of elements among the buckets
        and ensure that the size of elements within a single bucket falls within the desired range
        defined by `_lo` and `_hi`.

        Notes
        -----
        - If the number of elements in a bucket exceeds `_hi`, the bucket is split into multiple buckets.
        - If the total size of two adjacent buckets falls below `_lo`, the buckets are merged into one.
        """
        i: BucketIndex = 0
        while i < len(self.a):
            if self._hi < len(self.a[i]):
                k = math.ceil(len(self.a[i]) / self._lo)
                m = math.ceil(len(self.a[i]) / k)
                for _ in range(k-1):
                    self.a.insert(i+1, self.a[i][-m:])
                    del self.a[i][-m:]
            elif 0 < i and (len(self.a[i-1]) + len(self.a[i])) < self._lo:
                self.a[i-1].extend(self.a.pop(i))
                continue
            i += 1

    def _handle_empty_multiset(func: Callable[[T], None]) -> Callable[[T], None]:
        """Decorator to handle operations on an empty multiset.

        This decorator is used to wrap methods that perform operations on the multiset
        when it is empty. It ensures that the necessary initialization is done before
        executing the operation.

        Parameters
        ----------
        func : callable
            The method to be decorated.

        Returns
        -------
        callable
            The decorated method.
        """
        def inner_func(self, x):
            if self:
                func(self, x)
            else:
                self.a = [[x]]
                self.size = 1
                self._calc_info()

        return inner_func
    
    def _update_min_max(self, i: BucketIndex) -> None:
        """Update the minimum and maximum values of a bucket.

        This method updates the minimum and maximum values of the bucket at index `i`
        in the multiset. It is called after adding or removing elements from the bucket.

        Parameters
        ----------
        i : int
            The index of the bucket to update.

        Returns
        -------
        None
        """
        if self.a[i]:
            self._mins[i] = self.a[i][0]
            self._maxs[i] = self.a[i][-1]

    @_handle_empty_multiset
    def add(self, x: T) -> None:
        """Add an element to the multiset. O(√N)

        Parameters
        ----------
        x : T
            The element to be added to the multiset.

        Returns
        -------
        None

        Notes
        -----
        The `add` method adds an element `x` to the multiset. The element is inserted
        in a way that maintains the sorted order of the multiset. If the element already
        exists in the multiset, it will be inserted at the appropriate position to keep
        duplicate elements together.

        The time complexity of the `add` method is O(√N), where N is the size
        of the multiset. This complexity arises when adding an element to a bucket,
        which may involve shifting elements to make room for the new element. Since
        the size of each bucket is √N on average, the shift operation takes O(√N) time.
        """
        i: BucketIndex = max(0, bisect_left(self._mins, x) - 1)
        insort(self.a[i], x)
        self._update_min_max(i)
        self._countup(i)

    @_handle_empty_multiset
    def append(self, x: T) -> None:
        """Append `x` to the multiset, regardless of its existence, if it is greater than or equal to the maximum value. O(1)

        Parameters
        ----------
        x : T
            The value to append to the multiset.

        Raises
        ------
        ValueError
            If `x` is less than the maximum value in the multiset.

        Notes
        -----
        The `append` method appends the value `x` to the multiset, regardless of its existence in the multiset.
        However, `x` must be greater than or equal to the maximum value in the multiset. If `x` is less than the
        maximum value, a `ValueError` is raised.

        Examples
        --------
        >>> s = SortedMultiset([1, 2, 3])
        >>> s.append(3)  # No error, as 3 is equal to the maximum value in the multiset.

        >>> s = SortedMultiset([1, 2, 3])
        >>> s.append(2)
        ValueError: Appended value must be greater than or equal to the maximum value in the multiset.
        """
        i: BucketIndex = len(self.a) - 1
        if x < self.max():
            raise ValueError(f"Cannot append element {x} as it is less than or equal to the maximum value in the multiset.")
        self.a[i].append(x)
        self._update_min_max(i)
        self._countup(i)
        

    @_handle_empty_multiset
    def appendleft(self, x: T) -> None:
        """Append `x` to the beginning of the multiset, regardless of its existence, if it is less than or equal to the minimum value.  O(√N)

        Parameters
        ----------
        x : T
            The value to append to the multiset.

        Raises
        ------
        ValueError
            If `x` is greater than the minimum value in the multiset.

        Notes
        -----
        The `appendleft` method appends the value `x` to the beginning of the multiset, regardless of its existence in the multiset.
        However, `x` must be less than or equal to the minimum value in the multiset. If `x` is greater than the minimum value,
        a `ValueError` is raised.

        This operation has a time complexity of O(√N), where N is the size of the multiset. It involves adding an element to the
        beginning of a bucket (list) that contains √N elements.

        Examples
        --------
        >>> s = SortedMultiset([1, 2, 3])
        >>> s.appendleft(0)  # No error, as 0 is less than or equal to the minimum value in the multiset.

        >>> s = SortedMultiset([1, 2, 3])
        >>> s.appendleft(2)  # No error, as 2 is equal to the minimum value in the multiset.
        """
        i: BucketIndex = 0
        if self.min() < x:
            raise ValueError("Appended value must be less than or equal to the minimum value in the multiset.")
        self.a[i].insert(0, x)
        self._update_min_max(i)
        self._countup(i)

    def _countup(self, i: BucketIndex) -> None:
        """Increment the size counters and perform necessary balancing after adding an element to the multiset."""
        self.size += 1
        for k, _sizes in zip(self.K, self._sizes):
            _sizes[i>>k] += 1
        if len(self.a[i]) > self._excess:
            self._balance()
            self._calc_info()
    
    def _countdown(self, i: BucketIndex) -> None:
        """Decrement the size counters and perform necessary balancing after removing an element from the multiset."""
        self.size -= 1
        for k, _sizes in zip(self.K, self._sizes):
            _sizes[i>>k] -= 1
        if not len(self.a[i]):
            self.a.pop(i)
            self._calc_info()

    def pop(self, index: int=-1) -> T:
        """Remove and return the element at the specified index in the multiset. O(√N)"""
        i: BucketIndex
        j: ElementIndex
        if not self: raise IndexError("pop from empty list")
        if index < 0:
            index += self.size
        if 0 <= index < len(self):
            if -len(self.a[-1]) <= index - len(self):
                i, j = len(self.a) - 1, index - len(self)
            elif index < len(self.a[0]):
                i, j = 0, index
            else:
                i, j = self._loc(index)
            x = self.a[i].pop(j)
            self._update_min_max(i)
            self._countdown(i)
            return x
        else:
            raise IndexError("pop index out of range")

    def discard(self, x: T) -> None:
        """Remove the first occurrence of the specified element from the multiset, if exists. O(√N)"""
        i: BucketIndex
        j: ElementIndex
        tmp = self._find(x)
        if tmp is not None:
            i, j = tmp
            self.a[i].pop(j)
            self._update_min_max(i)
            self._countdown(i)

    def optional_bound(decorated_func: Callable[[T], int]) -> Callable[[T], Optional[int]]:
        """Decorator that wraps a function to return an optional index value."""
        def wrapper(self, x: T) -> Optional[int]:
            index = decorated_func(self, x)
            if index < len(self):
                return index
            else:
                return None
        return wrapper

    @optional_bound
    def lower_bound(self, x: T) -> int:
        """Return the index of the first element in the multiset that is not less than `x`. O(√N)

        Parameters
        ----------
        x : T
            The value to compare against the elements in the multiset.

        Returns
        -------
        index : int or None
            The index of the first element that is not less than `x`, or None if `x` is greater than all elements.

        Notes
        -----
        The `lower_bound` method returns the index of the first element in the multiset that is
        not less than the given value `x`. If the multiset contains duplicate elements equal to `x`,
        the index of the first occurrence of `x` is returned. If `x` is greater than all elements in
        the multiset, None is returned.

        The time complexity of the `lower_bound` method is O(√N), where N is the size of the multiset.
        Although it appears that the method requires iterating through √N buckets, in practice,
        the multiset uses skip connections at multiples of 64 and 8, allowing skipping over multiple
        buckets in a single iteration.

        Examples
        --------
        >>> s = SortedMultiset([1, 2, 3, 4, 5])
        >>> s.lower_bound(3)
        2
        - The multiset [1, 2, 3, 4, 5] contains the value 3 at index 2.

        >>> s.lower_bound(6)
        None
        - The multiset [1, 2, 3, 4, 5] does not contain a value greater than or equal to 6.
        """
        i: BucketIndex
        if self:
            i, index = self._iterate_row_index(x, __lt__)
            index += bisect_left(self.a[i], x)
        else:
            index = 0
        return index
    
    @optional_bound
    def upper_bound(self, x: T) -> int:
        """Return the index of the first element in the multiset that is greater than `x`. O(√N)

        Parameters
        ----------
        x : T
            The value to compare against the elements in the multiset.

        Returns
        -------
        int or None
            The index of the first element that is greater than `x`, or None if `x` is greater than or equal to all elements.

        Notes
        -----
        The `upper_bound` method returns the index of the first element in the multiset that is
        greater than the given value `x`. If the multiset contains duplicate elements equal to `x`,
        the index of the first occurrence of an element greater than `x` is returned. If `x` is greater
        than or equal to all elements in the multiset, None is returned.

        The time complexity of the `upper_bound` method is O(√N), where N is the size of the multiset.
        In practice, the multiset uses skip connections at multiples of 64 and 8, which allows efficient
        skipping over multiple buckets in a single iteration.

        Examples
        --------
        >>> s = SortedMultiset([1, 2, 3, 4, 5])
        >>> s.upper_bound(3)
        3
        - The multiset [1, 2, 3, 4, 5] contains the value 4 at index 3, which is the first element greater than 3.

        >>> s.upper_bound(6)
        None
        - The multiset [1, 2, 3, 4, 5] does not contain a value greater than 6.
        """
        i: BucketIndex
        if self:
            i, index = self._iterate_row_index(x, __le__)
            index += bisect_right(self.a[i], x)
        else:
            index = 0
        return index

    def count(self, x: T) -> int:
        """Return the number of occurrences of the specified element in the multiset. O(√N)"""
        lo: Optional[int] = self.lower_bound(x)
        if lo is None:
            return 0
        hi: Optional[int] = self.upper_bound(x)
        if hi is None:
            hi = len(self)
        return hi - lo

    def gt(self, x: T) -> Optional[T]:
        """Return the smallest element in the multiset that is greater than the specified value, if exists. O(log N)"""
        i: BucketIndex
        if self:
            i = min(len(self.a)-1, bisect_right(self._maxs, x))
            if x < self.a[i][-1]:
                return self.a[i][bisect_right(self.a[i], x)]
        return None

    def ge(self, x: T) -> Optional[T]:
        """Return the smallest element in the multiset that is greater than or equal to the specified value, if exists. O(log N)"""
        i: BucketIndex
        if self:
            i = min(len(self.a)-1, bisect_left(self._maxs, x))
            if x <= self.a[i][-1]:
                j = bisect_left(self.a[i], x)
                return self.a[i][j]
        return None

    def lt(self, x) -> Optional[T]:
        """Return the largest element in the multiset that is less than the specified value, if exists. O(log N)"""
        i: BucketIndex
        if self:
            i = max(0, bisect_left(self._mins, x) - 1)
            if self.a[i][0] < x:
                return self.a[i][bisect_left(self.a[i], x) - 1]
        return None

    def le(self, x) -> Optional[T]:
        """Return the largest element in the multiset that is less than or equal to the specified value, if exists. O(log N)"""
        i: BucketIndex
        if self:
            i = max(0, bisect_right(self._mins, x) - 1)
            if self.a[i][0] <= x:
                return self.a[i][bisect_right(self.a[i], x) - 1]
        return None
        
    def _loc(self, index: int) -> Tuple[BucketIndex, ElementIndex]:
        """Convert the global index to the corresponding bucket index and element index. O(√N)"""
        i: BucketIndex = 0
        j: ElementIndex = index
        for k, _sizes in zip(reversed(self.K), reversed(self._sizes)):
            while i + (1<<k) < len(self.a) and j >= _sizes[i>>k]:
                j -= _sizes[i>>k]
                i += (1<<k)
        return i, j

    def _iterate_row_index(self, x: T, op: Callable[[T, T], bool]) -> Tuple[BucketIndex, int]:
        """Iteratively find the row index and corresponding global index based on the specified condition. O(√N)"""
        i: BucketIndex = 0 
        index: int = 0
        for k, _sizes in zip(reversed(self.K), reversed(self._sizes)):
            while i + (1<<k) < len(self.a) and op(self._mins[i + (1<<k)], x):
                index += _sizes[i>>k]
                i += (1<<k)
        return i, index
    
    def _find(self, x: T) -> Optional[Tuple[BucketIndex, ElementIndex]]:
        """Find the first occurrence of the specified element in the multiset and return its bucket index and element index, if exists. O(log N)"""
        i: BucketIndex
        j: ElementIndex
        if self:
            i = bisect_left(self._maxs, x)
            if i < len(self.a):
                j = bisect_left(self.a[i], x)
                if j < len(self.a[i]) and self.a[i][j] == x:
                    return i, j
        return None

    def flatten(self) -> List[T]:
        """Flatten the multiset into a single list, preserving the order of elements. O(N)"""
        a: List[T] = []
        for bucket in self.a:
            a.extend(bucket)
        return a

    def tolist(self) -> List[List[T]]:
        """Convert the multiset into a 2D list representation, where each inner list corresponds to a bucket. O(N)"""
        if self:
            return [bucket.copy() for bucket in self.a]
        else:
            return [[]]

    def min(self) -> Optional[T]:
        """Return the smallest element in the multiset, if not empty. O(1)"""
        if self:
            return self.a[0][0]
        else:
            raise ValueError("min() arg is an empty sequence")

    def max(self) -> Optional[T]:
        """Return the largest element in the multiset, if not empty. O(1)"""
        if self:
            return self.a[-1][-1]
        else:
            raise ValueError("max() arg is an empty sequence")

    def __len__(self) -> int:
        return self.size

    def __getitem__(self, index: int) -> T:
        """O(√N)"""
        i: BucketIndex
        j: ElementIndex
        if index < 0:
            index += self.size
        if 0 <= index < len(self):
            i, j = self._loc(index)
            return self.a[i][j]
        raise IndexError

    def __setitem__(self, index: int, value: T) -> None:
        raise NotImplementedError("use pop(index) then add(value)")

    def __contains__(self, x) -> bool:
        """O(log N)"""
        return False if self._find(x) is None else True

    def __str__(self) -> str:
        return self.flatten().__str__()

    def __repr__(self) -> str:
        return f"SortedMultiset({self.flatten()})"

    def __iter__(self) -> Iterator[T]:
        for bucket in self.a:
            for x in bucket:
                yield x

    def __reversed__(self) -> Iterator[T]:
        for bucket in reversed(self.a):
            for x in reversed(bucket):
                yield x
        
    # ----------------------------------------------------------------------
    # class methods
    @classmethod
    def count_inversion(cls, a: List[T], count_duplicate: bool=False) -> int:
        """count inversion in numbers.

        Example
        -------
        >>> a = [3, 2, 2, 1]
        >>> SortedMultiset.count_inversion(a)
        5

          3    a[0] > (a[1], a[2], a[3])
        + 1    a[1] > (a[3])
        + 1    a[2] > (a[3])
        -------------------
        = 5

        >>> a = [3, 2, 2, 1]
        >>> SortedMultiset.count_inversion(a, count_duplicate=True)
        6

          3    a[0] >= (a[1], a[2], a[3])
        + 2    a[1] >= (a[2], a[3])
        + 1    a[2] >= (a[3])
        -------------------
        = 6

        Processing Time
        ---------------
        conditions
        N       Time
        1*10^5  <0.2 sec
        2*10^5  <0.3 sec
        5*10^5  <0.8 sec
        1*10^6  ~1.6 sec
        ***with PyPy3 on AtCoder***
        """
        sm = cls()
        sm.op = sm.lower_bound if count_duplicate else sm.upper_bound
        cnt = 0
        for _, x in enumerate(a):
            v = sm.op(x)
            v = v if v is not None else len(sm)
            cnt += len(sm) - v
            sm.add(x)
        return cnt
