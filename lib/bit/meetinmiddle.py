# T90-51

import bisect

class BitIterator():

    def __init__(self, n_bit, start=0, stop=None):
        self.n_bit = n_bit
        self.i = start
        self.stop = 2**self.n_bit if stop is None else stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.i == self.stop:
            raise StopIteration()
        seq = [(self.i >> b)&1 for b in range(self.n_bit)]
        self.i += 1
        return seq


class MeetInTheMiddle():

    def __init__(self, a):
        """
        BitIterator クラスを使用
        """

        self.n = len(a)
        self.bl = self._bit_aggregate(a[:self.n//2])
        self.br = self._bit_aggregate(a[self.n//2:])
        return

    def _bit_aggregate(self, a):

        n = len(a)
        b = [[] for _ in range(n+1)]
        for lst in BitIterator(n):
            b[sum(lst)].append(sum([ai for i, ai in zip(lst, a) if i]))
        for bj in b:
            bj.sort()
        return b

    def meet(self, K=None, lower_bound=None):
        """
        選択する個数: K

        return:
            cnt_a = K個選択する場合の数
            cnt_b = cnt_aのうちlower_bound 以下の選び方
            cnt_c = cnt_aのうちlower_bound より大きい選び方
        """

        cnt_a = 0
        cnt_b = 0
        cnt_c = 0
        for i in range(len(self.bl)):
            if not 0 <= K-i < len(self.br):
                continue  # out of range
            cnt_a += len(self.bl[i]) * len(self.br[K-i])
            for x in self.bl[i]:
                cnt_b += bisect.bisect_right(self.br[K-i], lower_bound-x)
        cnt_c = cnt_a - cnt_b
        return cnt_a, cnt_b, cnt_c


N, K, P = map(int, input().split())
A = list(map(int, input().split()))
mm = MeetInTheMiddle(A)
_, ans, _ = mm.meet(K, P)   
print(ans)