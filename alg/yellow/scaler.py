class ScaleReduction():
    """
    Example:
    --------
    >>> a = [1, 3, 5, 10]
    >>> sr = ScaleReduction(a=a)

    `sr(v)` can convert value to index.
    >>> print(sr(1))
    0
    >>> print(sr(5))
    2

    `sr[i]` can access the i-th smallest value.
    >>> print(sr[0])
    1
    >>> print(sr[3])
    10
    """

    def __init__(self, a):
        self.a = sorted(set(a))
        self.i2v = dict(zip(self.a, range(len(self.a))))
        
    def __call__(self, i):
        """convert index to value """
        return self.i2v[i]
    
    def __getitem__(self, i):
        """convert value to index"""
        return self.a[i]