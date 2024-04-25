import operator
class CumulativeList(list):
    
    def __init__(self, seq: list, op: callable = operator.add):
        super().__init__(self.__build(seq, op))
    
    def __build(self, __a, op):
        if __a:
            n = len(__a)
            __b = [None] * n
            __b[0] = __a[0]
            for i in range(1, n):
                __b[i] = op(__b[i-1], __a[i])
        else:
            __b = []
        return __b
