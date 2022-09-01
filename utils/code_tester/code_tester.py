from contextlib import contextmanager
import time

@contextmanager
def timer():
    """
    measure processing time with `with timer():`.
    """
    t0 = time.time()
    yield
    print(f'{time.time() - t0:.3f} sec')