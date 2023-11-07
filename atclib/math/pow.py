import numpy as np


"""
a^x (mod P) can be calculated pow(base=a, exp=x, mod) with python.
"""
pow(2, 10, mod=10**9+7)
# 1024 = 2^10

pow(2, 40, mod=10**9+7)
# 511620083 
# = 1099511627776 % 1000000007
# = 2^40 % 1000000007


def pow_array(A, n, mod):
    B = np.eye(len(A), dtype='object')
    while n:
        if n%2:
            B = (B@A) %mod
        A = (A@A) %mod
        n //= 2
    return B