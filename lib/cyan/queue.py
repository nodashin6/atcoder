class VariablePriorityQueue():

    def __init__(self, n, arr=None):
        self.n = n
        self.loc = {}
        self.unq = set([])
        if arr:
            self.hq = arr
            self._build(arr)
        else:
            self.hq = []
    
    def _build(self, arr):
        for i, (v, index) in enumerate(arr):
            self.loc[index] = i
            self.unq.add(index)
        return

    def push(self, v, index):
        if index in self.unq:
            self.hq[self.loc[index]][0] = v
        else:
            self.loc[index] = len(self.hq)
            self.unq.add(index)
            self.hq.append([v, index])
        self.forward(self.loc[index])
        

    def forward(self, i, should_backward=True):
        j = i*2+1
        while j < len(self):
            if j+1 < len(self) and self.hq[j] > self.hq[j+1]:
                j += 1
            if self.hq[i] < self.hq[j]:
                break
            self.hq[i], self.hq[j] = self.hq[j], self.hq[i]
            self.loc[self.hq[i][1]] = i
            self.loc[self.hq[j][1]] = j
            i, j = j, j*2+1
        if should_backward:
            self.backward(j=i)

    def backward(self, j):
        while j > 0:
            i = (j-1)//2
            if self.hq[i] < self.hq[j]:
                break
            self.hq[i], self.hq[j] = self.hq[j], self.hq[i]
            self.loc[self.hq[i][1]] = i
            self.loc[self.hq[j][1]] = j
            j = i

    def pop(self):
        if not self:
            raise IndexError("pop from empty list")

        (v, i) = self.hq[0]
        self.loc.pop(i)
        self.unq.remove(i)
        if len(self) == 1:
            self.hq.pop()
        else:
            self.hq[0] = self.hq.pop()
            self.loc[self.hq[0][1]] = 0
            self.forward(i=0, should_backward=False)
        return (v, i)

    def __len__(self):
        return len(self.hq)

    # ---------------------------------------
    # for debug
    def dprint(self, *args, **kwargs):
        if self.is_debug:
            print(*args, **kwargs)


N, M = map(int, input().split())
A = list(map(int, input().split()))
G = [[] for _ in range(N)]
C = [0]*N
for _ in range(M):
    u, v = map(int, input().split())
    u -= 1
    v -= 1
    G[u].append(v)
    G[v].append(u)
    C[u] += A[v]
    C[v] += A[u]
    
arr = sorted([[ci, i] for i, ci in enumerate(C)])
vpq = VariablePriorityQueue(n=N, arr=arr)
not_seen = set(range(N))
ans = 0
for _ in range(N):
    cx, x = vpq.pop()
    not_seen.remove(x)
    ans = max(ans, cx)
 
    for y in G[x]:
        C[y] -= A[x]
        if y in not_seen:
            vpq.push(*[C[y], y])
print(ans)