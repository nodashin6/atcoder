def z_algorithm(S):
    z = [0] * len(S)
    z[0] = len(S)
    i = 1
    j = 0
    while i < len(S):
        while i + j < len(S) and S[j] == S[i + j]: j += 1
        z[i] = j
        if j == 0:
            i += 1
            continue
        k = 1
        while i + k < len(S) and k + z[k] < j:
            z[i + k] = z[k]
            k += 1
        i += k
        j -= k
    
    return z