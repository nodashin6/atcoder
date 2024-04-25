import math


def round(b, a=1, k=0) -> float:
    """b/a を四捨五入"""
    b *= 10**(k+1)
    b = (b // a + 5) // 10
    b /= 10**k
    return b


GCD = int
def ext_gcd(x, y) -> tuple[int, int, 'GCD']:
    """ax + by = gcd(x, y)
    
    
    See Also
    --------
    https://www.youtube.com/watch?v=eiJyDb9c3Js
    """
    
    def _ext_gcd(x, y):
        """ax + by = gcd(x, y)   x <= y
        
        """
        if x == 0:
            return 0, 1, y
        s, t, g = _ext_gcd(y%x, x)
        # ---------------------------------------------------------
        # (1)             |  (y%x)s + xt = g
        # ---------------------------------------------------------
        # (2)             |  (y%x) + (y//x)*x = y
        #                 |  (y%x) = y - (y//x) * x
        # ---------------------------------------------------------
        # (1) <-- (2)     |  ( y - (y//x)*x )s + xt = g
        #                 |  ( t - (y//x)*s )x + sy = g
        #                 |        |
        #                 |        |  a = (t - (y//x)*s)
        #                 |        |  b = s
        #                 |        v
        #                 |  ax + by = g
        # ---------------------------------------------------------
        a = t - (y//x)*s
        b = s
        return a, b, g
    
    if x <= y:
        return _ext_gcd(x, y)
    else:
        a, b, g = _ext_gcd(y, x)
        return b, a, g