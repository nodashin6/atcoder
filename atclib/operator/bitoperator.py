def bit_subset(i: int):
    """subset generator
    
    Example
    -------
    >>> for j in bit_subset(13):
    >>>     print(j)
    12  # 1100
    9   # 1001
    8   # 1000
    5   # 0101
    4   # 0100
    1   # 0001
    0   # 0000
    -------------
    13  # 1101
    """
    j = i
    while 0 < j:
        j = i & (j - 1)
        yield j