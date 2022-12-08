"""
case1. When you want to search all prime numbers below n.
    -> Use class `Erathosthenes(n)`.

case2. When you want to factorize an integer x into prime factors.
    -> Use function `primefactorization(x)`.

case3. When you want to factorize all integers below n into prime factors.
    -> Use class `ArrangePrimeFactorization(n)`.
"""

class Erathosthenes():
    """
    Parameters:
    -----------
    n : int
        search prime numbers below `n`.

    Example:
    --------
    search prime numbers below 30.
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
    ***with PyPy3 on AtCoder***
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


def primefactorization(x):
    """
    Return:
    -------
    out : dict
        
    Example:
    --------
    prime factorization of 12
    >>> primefactorization(12)
    {2: 2, 3: 1}
    This is means 12 = 2^2 x 3^1

    Processing Time:
    ----------------
    x       time
    10^12   0.01 sec
    10^14   0.10 sec
    10^16   1.00 sec
    10^18   10.0 sec
    ***with PyPy3 on AtCoder**
    """
    factors = {}
    for i in range(2, int(x**0.5 + 2)):
        if x%i == 0:
            factors[i] = 0
        while x%i == 0:
            x //= i
            factors[i] += 1
    if x > 1:
        factors[x] = 1
    return factors


from collections import defaultdict
class ArrangePrimeFactorization():
    """
    All integers below `n` are factorized into prime numbers.

    Parameters:
    -----------
    i_factors : list[defaultdict(int)]
        i-th `i_factors` is factors of factorized number i.
    is_primes : list[bool]
        Is number i prime? 

    Example:
    --------
    >>> apf = ArrangePrimeFatorization(10**5)
    >>> apf[12]
    defaultdict(<class 'int'>, {2: 2, 3: 1})

    >>> apf[15444]
    defaultdict(<class 'int'>, {2: 2, 3: 3, 11: 1, 13: 1})
    This means that 15444 = 2^2 x 3^3 x 11 x 13
    
    Processing Time:
    ----------------
    n       time
    10^4    < 0.04 sec
    10^5    < 0.11 sec
    10^6    > 2.27 sec
    ***with PyPy3 on AtCoder**
    """
    def __init__(self, n):

        i_factors = [defaultdict(int) for _ in range(n+1)]
        is_primes = [True]*(n+1)
        is_primes[:2] = [False]*2
        for i in range(2, n+1):
            if not is_primes[i]:
                continue
            p = i
            while p < n+1:
                i_factors[p][i] += 1
                for j in range(2*p, n+1, p):
                    for k, v in i_factors[i].items():
                        i_factors[j][k] += v
                    is_primes[j] = False
                p *= i
        self.i_factors = i_factors

    def __getitem__(self, i):
        return self.i_factors[i]