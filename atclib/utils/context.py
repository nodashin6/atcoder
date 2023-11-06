class InterruptContext:
    """A context manager class that provides a mechanism to immediately exit from
    nested structures (like loops) within the context.

    Raises
    ------
    ExitContextError
        Internal exception used to handle the interruption of the context.
        This exception is caught within the context manager itself, so it 
        shouldn't be encountered directly by users.

    Example
    -------
    >>> with InterruptContext() as interrupt:
    >>>     for i in range(5):
    >>>         for j in range(5):
    >>>             if i == 3 and j == 3:
    >>>                 interrupt()
    >>> print(i, j)
    3 3
    """

    class ExitContextError(Exception):
        pass
    def __enter__(self):
        return self.interrupt
    def __exit__(self, exc_type, exc_value, traceback):
        return isinstance(exc_value, self.ExitContextError)
    def interrupt(self):
        raise self.ExitContextError