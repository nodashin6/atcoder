class ScaleReduction():
    """
    Example:
    --------
    >>> a = [1, 3, 5, 10]
    >>> sr = ScaleReduction(a=a)

    [] can convert value to index.

    >>> print(sr[1])
    0
    >>> print(sr[5])
    2

    () can convert index to value.

    >>> print(sr(0))
    1
    >>> print(sr(3))
    10
    """

    def __init__(self, a):
        self.a = sorted(set(a))
        self.i2v = {}
        self.v2i = {}
        for i, v in enumerate(self.a):
            self.i2v[i] = v
            self.v2i[v] = i

    def __call__(self, v):
        """convert value to index"""
        return self.i2v[v]
    
    def __getitem__(self, i):
        """convert index to value"""
        return self.v2i[i]