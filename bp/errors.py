class LinkError(Exception):
    """
    An error with symlinks - either that there are cyclical symlinks or that
    symlink are not supported on this platform.
    """


class UnlistableError(Exception):
    """
    An exception which is used to distinguish between errors which mean 'this
    is not a directory you can list' and other, more catastrophic errors.
    """
