class Erathosthenes():
    """
    Parameters:
    -----------
    n : int
        search primenumbers below `n`.

    Example:
    --------
    search prime numers below 30.
    >>> era = Erathostenes(n=30)
    >>> print(era.primes)
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

    Is 13 a prime number?
    >>> era.is_prime(13)
    True

    Is 15 a prime number?
    >>> era.is_prime(15)
    False

    Preprocessing Time:
    -------------------
    n       time(ms)
    10^6    <100
    10^7    <500
    10^8    ~7000
    ***with PyPy3 in AtCoder***
    """

    def __init__(self, n=10**6):
        self.n = n
        self.primes = self._seive()

    def _seive(self):
        is_primes = [True]*(self.n+1)
        is_primes[:2] = [False]*2
        for i in range(2, int(self.n**0.5)+2):
            if is_primes[i]:
                for j in range(i*2, self.n+1, i):
                    is_primes[j] = False
        self._is_primes = is_primes
        primes = [i for i in range(2, self.n+1) if is_primes[i]]
        return primes

    def is_prime(self, x):
        return self._is_primes[x]
