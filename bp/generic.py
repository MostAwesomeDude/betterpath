def genericSibling(path, segment):
    """
    Return a L{FilePath} with the same directory as this instance but with
    a basename of C{path}.

    @param path: The basename of the L{FilePath} to return.
    @type path: L{str}

    @return: The sibling path.
    @rtype: L{FilePath}
    """

    return path.parent().child(segment)
