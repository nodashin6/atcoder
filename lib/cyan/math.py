import math
def search_divisor(n):
    res = []
    for i in range(1, math.floor(n**0.5 + 1)):
        if n % i == 0:
            res.append(i)
            res.append(n//i)
    return res