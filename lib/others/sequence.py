def flatten(seq):
    a = []
    dq = seq.copy()
    while dq:
        u = dq.pop()
        if type(u) is list or type(u) is tuple:
            for ui in u:
                dq.append(ui)
        else:
            a.append(u)
    return a[::-1]