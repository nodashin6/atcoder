class ExtendedBinaryIndexedTree:

    def __init__(self):
        # 24bit + 4bit + 4bit = 32bit
        self.n24 = 16777216
        self.n4 = 16
        self.k = 4
        self.bits = {i: {} for i in range(3)}
        self.accs = {i: {} for i in range(3)}
        self.bits[0][0] = [0] * (self.n24+1)
        self.accs[0][0] = [0] * (self.n24+1)
        return

    def add(self, x, v=1):
        
        vx = v*x
        xx = ((x>>8), (x>>4), x)
        yy = ((x>>8)&16777215, (x>>4)&15, x&15)
        bit = self.bits[0][0]
        acc = self.accs[0][0]
        for i, (x, y) in enumerate(zip(xx, yy)):
            self.bitadd(bit, y, v)
            self.bitadd(acc, y, vx)
            if i < 2:
                if self.bits[i+1].get(x, None) is None:
                    self.bits[i+1][x] = [0] * 17
                    self.accs[i+1][x] = [0] * 17
                bit = self.bits[i+1][x]
                acc = self.accs[i+1][x]

    def bitadd(self, bit, i, v=1):
        i += 1
        while i < len(bit):
            bit[i] += v
            i += i&-i

    def __getitem__(self, index):
        if index < 0:
            index += self.bits[0][0][-1]
        if 0 <= index < self.bits[0][0][-1]:
            return self._loc(index)
        raise IndexError

    def _loc(self, index):
        x = 0
        bit = self.bits[0][0]
        kk = (4, 4, 0)
        bit_lengths = (24, 4, 4)
        for i, bit_length in enumerate(bit_lengths):
            y, index = self.bisect_index(bit, index, bit_length)
            x += y
            if i < 2:
                bit = self.bits[i+1][x]
                x <<= kk[i]
        return x

    def bisect_index(self, bit, index, bit_length=4):
        index += 1
        l = 0
        i = 0
        for k in reversed(range(bit_length)):
            j = i + (1<<k)
            if j < len(bit) and bit[j] < index:
                index -= bit[j]
                i = j
        return i, index-1


    def sum(self, x):
        xx = ((x>>8), (x>>4), x)
        yy = ((x>>8)&16777215, (x>>4)&15, x&15)
        s = 0
        bit = self.bits[0][0]
        acc = self.accs[0][0]
        for i, (x, y) in enumerate(zip(xx, yy)):
            s += self.bitsum(acc, y)
            if i < 2:
                if self.bits[i+1].get(x, None) is None:
                    self.bits[i+1][x] = [0] * 17
                    self.accs[i+1][x] = [0] * 17
                bit = self.bits[i+1][x]
                acc = self.accs[i+1][x]
        return s

    def kthsum(self, k):
        x = 0
        s = 0
        bit = self.bits[0][0]
        acc = self.accs[0][0]
        index = k-1
        kk = (4, 4, 0)
        bit_lengths = (24, 4, 4)
        for i, bit_length in enumerate(bit_lengths):
            y, index = self.bisect_index(bit, index, bit_length)
            s += self.bitsum(acc, y)
            x += y
            if i < 2:
                bit = self.bits[i+1][x]
                acc = self.accs[i+1][x]
                x <<= kk[i]
        return s + x*(index+1)
            
    def bitsum(self, bit, i=None):
        i = len(bit) if i is None else i
        x = 0
        while i > 0:
            x += bit[i]
            i -= i&-i
        return x