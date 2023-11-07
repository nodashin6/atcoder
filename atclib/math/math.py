import math


def round(b, a=1, k=0) -> float:
    """b/a を四捨五入"""
    b *= 10**(k+1)
    b = (b // a + 5) // 10
    b /= 10**k
    return b