def prime_factorization(x):
    """
    Return:
    -------
    out : dict
        
    Example:
    --------
    prime factorization of 12
    >>> prime_factorization(12)
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
    
    
class Coprime:
    """Build O(logN), Get O(logA)"""
    
    def __init__(self, n=None):
        if n is None:
            n = 10**6
        self.n = n
        self.__build()
        
    def __build(self):
        n = self.n
        a = [0] * (n + 1)
        for i in range(2, n+1):
            if a[i]:
                continue
            for j in range(i, n+1, i):
                if not a[j]:
                    a[j] = i
        self.a = a
        return
        
    def __call__(self, x: int) -> list:
        """O(logA)"""
        divisors = []
        while 1 < x:
            p = self.a[x]
            x = x // p
            divisors.append(p)
        return divisors