class LinkError(Exception):
    """
    An error with symlinks - either that there are cyclical symlinks or that
    symlink are not supported on this platform.
    """


class UnlistableError(OSError):
    """
    An exception which is used to distinguish between errors which mean 'this
    is not a directory you can list' and other, more catastrophic errors.

    This error will try to look as much like the original error as possible,
    while still being catchable as an independent type.

    @ivar originalException: the actual original exception instance, either an
        L{OSError} or a L{WindowsError}.
    """

    def __init__(self, originalException):
        """
        Create an UnlistableError exception.

        @param originalException: an instance of OSError.
        """
        self.__dict__.update(originalException.__dict__)
        self.originalException = originalException
