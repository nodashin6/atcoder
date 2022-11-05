import numpy as np
def pow_array(A, n, mod):
    B = np.eye(len(A), dtype='object')
    while n:
        if n%2:
            B = (B@A) %mod
        A = (A@A) %mod
        n //= 2
    return B