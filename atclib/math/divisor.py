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
