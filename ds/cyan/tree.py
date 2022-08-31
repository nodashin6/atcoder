class BinaryTrie():
    """
    If values are greater than 10^5, 
    values must be reduced scale as preprocess.
    """
    
    def __init__(self, n_bit):
        self.n = n_bit
        self.size = 2 ** (n_bit-1) * 2
        self.arr = [0] * self.size
 
    def add(self, x):
        useidxs = self.get_idxs(x)
        if self.arr[useidxs[-1]] == 1:
            # already exist
            return
        else:
            for idx in useidxs:
                self.arr[idx] += 1
            return
             
    def get_idxs(self, x):
        useidxs = []
        i = 1
        for ni in range(self.n-1, -1, -1):
            b = (x >> ni) & 1
            i += b
            useidxs.append(i)
            i *= 2
        return useidxs
 
    def lower_bound(self, x):
        """配列中のxより大きい数字の中で最小の数"""
        bit_x = self.to_bit(x)
        idxs = self.get_idxs(x)
        is_found = False
        for i, (b, idx) in enumerate(zip(bit_x[::-1], idxs[::-1])):
            """左から登って右に下れる数字があるか"""
            if b == '0' and self.arr[idx+1] > 0:
                bit_y = bit_x[:self.n-(i+1)] + '1'
                idx += 1
                is_found = True
                break
        
        # 自分より大きい数字がない
        if is_found is False:
            return None
 
        for _ in range(i):
            for b in (0, 1):
                if self.arr[2*idx + b] > 0:
                    idx = 2*idx+b
                    bit_y += str(b)
                    break
 
        return int(bit_y, 2)
 
    def to_bit(self, x):
        bit = bin(x)[2:]
        bit = '0'*(self.n-len(bit)) + bit
        return bit