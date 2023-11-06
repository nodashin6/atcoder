def merge_sorted_sequence(*args):
    """
    merge_sorted_sequence(sorted(A0), sorted(A1))
    -> sorted(A0 + A1)
    """
    a = [ai[::-1] for ai in args]
    b = []
    while a:
        x = None
        for i in range(len(a)):
            if x is None:
                x = a[i].pop()
            elif a[i][-1] < x:
                a[i-1].append(x)
                x = a[i].pop()
        for i in reversed(range(len(a))):
            if not a[i]:
                del a[i]
        b.append(x)
    return b