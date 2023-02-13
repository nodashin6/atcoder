class BinaryTrie():
    """
    If values are greater than 10^5, 
    values must be reduced scale as preprocessing.

    Problems
    --------
    [with ScaleReduction]
    ABC217D: https://atcoder.jp/contests/abc217/submissions/34522173
    """
    
    def __init__(self, n_bit):
        self.n = n_bit
        self.size = 2 ** (n_bit+1) - 1
        self.m = self.size // 2
        self.a = [0] * self.size

    def add(self, x):
        i = x + self.m
        if self.a[i] == 1:
            # already exist
            return
        while i > -1:
            self.a[i] += 1
            i -= 1
            i //= 2
        return
 
    def lower_bound(self, x):
        """配列中のx以上の数字の中で最小の数"""
        i = x + self.m
        if self.a[i]:
            return i - self.m
        
        is_left = 0
        while i > 0:
            is_left = i%2
            j = (i-1)//2
            if is_left and self.a[j] > self.a[i]:
                i += 1
                break
            i = j
        while i < self.m:
            if is_left:
                l = i*2+1
                if self.a[l]:
                    i = l
                    continue
            i = i*2+2
        if self.a[i]:
            return i - self.m
        else:
            return None
