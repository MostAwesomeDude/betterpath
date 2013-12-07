def genericSibling(path, segment):
    """
    Return a L{IFilePath} with the same directory as the given path, but with a
    basename of C{segment}.

    @param segment: The basename of the L{IFilePath} to return.
    @type segment: L{str}

    @return: The sibling path.
    @rtype: L{IFilePath}
    """

    return path.parent().child(segment)


def genericChildren(path):
    """
    List the children of the given path.

    @return: an iterable of all currently-existing children of the path.
    """

    return map(path.child, path.listdir())
