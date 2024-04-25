class DifferenceSegmentTree:
    """Range Add and Range Min
    
    See Also
    --------
    https://noshi91.hatenablog.com/entry/2023/11/03/183702
    """
    INF = 1 << 60
    
    def __init__(self, a):
        self.depth = (len(a)-1).bit_length()
        self.n_nodes = 1 << self.depth
        self.size = self.n_nodes + len(a)
        m = len(a)
        a += [self.INF] * (self.n_nodes - m)
        self._build(a)
    
    def _build(self, a):
        self.tree = ([None] * self.n_nodes) + a
        for i in reversed(range(1, self.n_nodes)):
            l = i << 1
            r = l + 1
            self.tree[i] = min(self.tree[l], self.tree[r])
        self.tree[0] = self.tree[1]
        for i in range(1, self.n_nodes):
            l = i << 1
            r = l + 1
            self.tree[i] = self.tree[l] - self.tree[r]
        self.tree = self.tree[:self.n_nodes]
        self.diff = [0] * (self.n_nodes + self.n_nodes)

    def get(self, index):
        index += self.n_nodes
        v = self.tree[0]
        parent = index >> 1
        for _ in range(self.depth):
            if index & 1:
                if self.tree[parent] < 0:
                    v -= self.tree[parent]
            else:
                if 0 < self.tree[parent]:
                    v += self.tree[parent]
            index = parent
            parent >>= 1
        return v
    
    def add(self, left, right, value):
        
        left += self.n_nodes
        right += self.n_nodes
        if self.size < right:
            raise IndexError("Out of range")
        
        _memo = (left, right)
        while left < right:
            if left & 1:
                self.diff[left] = value
                left += 1
            if right & 1:
                self.diff[right - 1] = value
            left >>= 1
            right >>= 1
        
        left, right = _memo
        right -= 1
        for _ in range(self.depth):
            if left & 1:
                left -= 1
            parent = left >> 1
            lmin = 0
            rmin = - self.tree[parent]
            bf_min = min(lmin, rmin)
            lmin += self.diff[left]
            rmin += self.diff[left + 1]
            af_min = min(lmin, rmin)
            self.tree[parent] = lmin - rmin
            self.diff[parent] += af_min - bf_min
            self.diff[left] = 0
            self.diff[left + 1] = 0
            
            if right & 1 == 0:
                right += 1
            parent = right >> 1
            lmin = 0
            rmin = - self.tree[parent]
            bf_min = min(lmin, rmin)
            lmin += self.diff[right-1]
            rmin += self.diff[right]
            af_min = min(lmin, rmin)
            self.tree[parent] = lmin - rmin
            self.diff[parent] += af_min - bf_min
            self.diff[right - 1] = 0
            self.diff[right] = 0
            
            left >>= 1
            right >>= 1
        
        self.tree[0] += self.diff[1]
        self.diff[1] = 0
        
        
    def query(self, left, right):
        
        left += self.n_nodes
        right += self.n_nodes
        min_value = self.INF
        
        queue = [(1, self.tree[0])]
        depth = self.depth
        for _ in range(self.depth):
            next_queue = []
            for i, value in queue:
                if min_value < value:
                    continue
                left_index = i << depth
                right_index = (i+1) << depth
                if right <= left_index or right_index <= left:
                    continue
                elif left <= left_index and right_index <= right:
                    min_value = min(min_value, value)
                else:
                    if self.tree[i] < 0:
                        next_queue.append((i<<1, value))
                        next_queue.append((i<<1 | 1, value - self.tree[i]))
                    else:
                        next_queue.append((i<<1, value + self.tree[i]))
                        next_queue.append((i<<1 | 1, value))
            queue = next_queue
            depth -= 1
        else:
            for i, value in queue:
                if left <= i < right:
                    min_value = min(min_value, value)
        return min_value
            
    def tolist(self):
        return [self.get(i) for i in range(self.n_nodes)]