import math
from operator import \
    __add__, __sub__, __mul__, __floordiv__, __truediv__, \
    __xor__, __and__, __or__, __pow__
class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __len__(self): 
        return 2
    
    def __iter__(self):
        yield self.x
        yield self.y

    def __getitem__(self, index): 
        return (self.x, self.y)[index]
    
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError
        
    def __str__(self):
        return str((self.x, self.y))
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __ope(ope):
        def inner_func(self, value):
            if hasattr(value, "__iter__"):
                x, y = value[0], value[1]
                return Vector(ope(self.x, x), ope(self.y, y))
            else:
                return Vector(ope(self.x, value), ope(self.y, value))
        return inner_func
    __add__ = __ope(__add__)
    __sub__ = __ope(__sub__)
    __mul__ = __ope(__mul__)
    __floordiv__ = __ope(__floordiv__)
    __truediv__ = __ope(__truediv__)
    __xor__ = __ope(__xor__)
    __and__ = __ope(__and__)
    __or__ = __ope(__or__)
    __pow__ = __ope(__pow__)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __matmul__(self, value):
        if hasattr(value, "__iter__"):
            x, y = value[0], value[1]
            return self.x*x + self.y*y
        raise ValueError
    
    def __eq__(self, value):
        if hasattr(value, "__iter__"):
            x, y = value[0], value[1]
            return self.x == x and self.y == y
    
    def cross(self, value):
        """
        cross prodcut
        (a, b) x (c, d) = ad - bc

        ∠AOB < 180  <==> AO x OB > 0
        """
        if hasattr(value, "__iter__"):
            x, y = value[0], value[1]
            return self.x*y - self.y*x
        raise ValueError
    
    def rotate(self, r, degree=False):
        sin = math.sin
        cos = math.cos
        x, y = self.x, self.y
        r = math.radians(r) if degree else r
        f = [
            [cos(r), -sin(r)],
            [sin(r), cos(r)]
        ]
        return Vector(f[0][0]*x+f[0][1]*y, f[1][0]*x+f[1][1]*y)

    @staticmethod
    def circumcenter(va, vb, vc):
        """
        [[a, b],     [[x],     [[e],
         [c, d]]  *   [y]]  =   [f]]
        <=>
        [[x],     1/      [[d, -b],     [[e],
         [y]   =   det  *  [-c, a]]  *   [f]]

        See Also
        --------
            circumcenter: https://integraldx.info/circumcenter-1986
        """
        a = -2*(va[0]-vb[0])
        b = -2*(va[1]-vb[1])
        e = -(va[0]**2-vb[0]**2)-(va[1]**2-vb[1]**2)

        c = -2*(va[0]-vc[0])
        d = -2*(va[1]-vc[1])
        f = -(va[0]**2-vc[0]**2)-(va[1]**2-vc[1]**2)

        det = a*d - b*c
        if det == 0:
            max_dist = -1
            max_mid = None
            for vi, vj in zip((va, vb, vc), (vb, vc, va)):
                dist = sum((vi - vj) ** 2)
                mid = (vi + vj) / 2
                if max_dist < dist:
                    max_dist = dist
                    max_mid = mid
            return max_mid
        else:
            return Vector((d*e - b*f)/det, (-c*e + a*f)/det)
