import bisect
def longest_increasing_subsequence(a: list) -> list:
    n = len(a)
    memo = [{} for _ in range(n+2)]
    dp = [float('inf')] * (n+2)
    dp[0] = -float('inf')
    for i, ai in enumerate(a + [float('inf')]):
        i = bisect.bisect_left(dp, ai)
        dp[i] = ai
        memo[i][ai] = dp[i-1]

    i = bisect.bisect_left(dp, float('inf'))
    v = float('inf')
    b = []
    for j in reversed(range(2, i+1)):
        b.append(memo[j][v])
        v = memo[j][v]
    b = b[::-1]
    return b