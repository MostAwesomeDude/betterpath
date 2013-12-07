from bp.errors import LinkError


def genericParents(path):
    """
    Retrieve an iterator of all the ancestors of the given path.

    @return: an iterator of all the ancestors of the given path, from the most
             recent (its immediate parent) to the root of its filesystem.
    """

    parent = path.parent()
    # root.parent() == root, so this means "are we the root"
    while path != parent:
        yield parent
        path = parent
        parent = parent.parent()


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


def genericWalk(path, descend=None):
    """
    Yield a path, then each of its children, and each of those children's
    children in turn.

    The optional argument C{descend} is a predicate that takes a FilePath,
    and determines whether or not that FilePath is traversed/descended
    into.  It will be called with each path for which C{isdir} returns
    C{True}.  If C{descend} is not specified, all directories will be
    traversed (including symbolic links which refer to directories).

    @param descend: A one-argument callable that will return True for
        FilePaths that should be traversed, False otherwise.

    @return: a generator yielding FilePath-like objects.
    """

    # Note that we already agreed to yield this path.
    yield path

    if path.isdir():
        for c in path.children():
            # we should first see if it's what we want, then we
            # can walk through the directory
            if descend is None or descend(c):
                for subc in c.walk(descend):
                    # Check for symlink loops.
                    rsubc = subc.realpath()
                    rself = path.realpath()
                    if rsubc == rself or rsubc in rself.parents():
                        raise LinkError("Cycle in file graph.")
                    yield subc
            else:
                yield c


def genericDescendant(path, segments):
    """
    Retrieve a child or child's child of the given path.

    @param segments: A sequence of path segments as L{str} instances.

    @return: A L{FilePath} constructed by looking up the C{segments[0]}
        child of this path, the C{segments[1]} child of that path, and so
        on.
    """

    for name in segments:
        path = path.child(name)
    return path


def genericSegmentsFrom(path, ancestor):
    """
    Return a list of segments between a child and its ancestor.

    For example, in the case of a path X representing /a/b/c/d and a path Y
    representing /a/b, C{Y.segmentsFrom(X)} will return C{['c',
    'd']}.

    @param ancestor: an instance of the same class as self, ostensibly an
    ancestor of self.

    @raise: ValueError if the 'ancestor' parameter is not actually an
    ancestor, i.e. a path for /x/y/z is passed as an ancestor for /a/b/c/d.

    @return: a list of strs
    """

    # The original author alludes to an "obvious fast implementation". I
    # cannot envision an obvious fast implementation which behaves
    # correctly on arbitrary IFilePaths, so I will leave this here for the
    # next brave hacker. ~ C.
    f = path
    p = f.parent()
    segments = []
    while f != ancestor and f != p:
        segments.append(f.basename())
        f, p = p, p.parent()
    if f == ancestor and segments:
        segments.reverse()
        return segments
    raise ValueError("%r not parent of %r" % (ancestor, path))


def genericGetContent(path):
    """
    Retrieve the data from a given file path.
    """

    # We are not currently willing to use a with-statement here, for backwards
    # compatibility.
    fp = path.open()
    try:
        return fp.read()
    finally:
        fp.close()
