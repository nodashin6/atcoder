import math
def search_divisor(n):
    """
    約数の列挙
    res[2*i] * res[2*i+1] = n
    になるような配列を返す。
    """
    res = []
    for i in range(1, math.floor(n**0.5 + 1)):
        if n % i == 0:
            res.append(i)
            res.append(n//i)
    return res


def rround(b, a=1, k=0) -> float:
    """b/a を四捨五入"""
    b *= 10**(k+1)
    b = (b // a + 5) // 10
    b /= 10**k
    return b