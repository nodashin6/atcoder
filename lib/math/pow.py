"""
a^x (mod P) can be calculated pow(base=a, exp=x, mod) with python.
"""
pow(2, 10, mod=10**9+7)
# 1024 = 2^10

pow(2, 40, mod=10**9+7)
# 511620083 
# = 1099511627776 % 1000000007
# = 2^40 % 1000000007