from __future__ import division, absolute_import

from bp.errors import LinkError
from bp.generic import genericChildren, genericParents, genericSibling


class AbstractFilePath(object):
    """
    Abstract implementation of an L{IFilePath}; must be completed by a
    subclass.

    This class primarily exists to provide common implementations of certain
    methods in L{IFilePath}. It is *not* a required parent class for
    L{IFilePath} implementations, just a useful starting point.

    Classes mixing in this class must provide the following methods:

     * basename()
     * child()
     * getAccessTime()
     * getModificationTime()
     * getStatusChangeTime()
     * isdir()
     * listdir()
     * open()
     * parent()

    And the following attributes:

     * path
    """

    def getContent(self):
        """
        Retrieve the file-like object for this file path.
        """
        fp = self.open()
        try:
            return fp.read()
        finally:
            fp.close()

    parents = genericParents

    children = genericChildren

    def walk(self, descend=None):
        """
        Yield myself, then each of my children, and each of those children's
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

        # Note that we already agreed to yield ourselves if we've been called.
        yield self

        if self.isdir():
            for c in self.children():
                # we should first see if it's what we want, then we
                # can walk through the directory
                if descend is None or descend(c):
                    for subc in c.walk(descend):
                        # Check for symlink loops.
                        rsubc = subc.realpath()
                        rself = self.realpath()
                        if rsubc == rself or rsubc in rself.parents():
                            raise LinkError("Cycle in file graph.")
                        yield subc
                else:
                    yield c

    sibling = genericSibling

    def descendant(self, segments):
        """
        Retrieve a child or child's child of this path.

        @param segments: A sequence of path segments as L{str} instances.

        @return: A L{FilePath} constructed by looking up the C{segments[0]}
            child of this path, the C{segments[1]} child of that path, and so
            on.

        @since: 10.2
        """
        path = self
        for name in segments:
            path = path.child(name)
        return path

    def segmentsFrom(self, ancestor):
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
        # this might be an unnecessarily inefficient implementation but it will
        # work on win32 and for zipfiles; later I will deterimine if the
        # obvious fast implemenation does the right thing too
        f = self
        p = f.parent()
        segments = []
        while f != ancestor and p != f:
            segments[0:0] = [f.basename()]
            f = p
            p = p.parent()
        if f == ancestor and segments:
            return segments
        raise ValueError("%r not parent of %r" % (ancestor, self))

    def __hash__(self):
        """
        Hash the same as another L{FilePath} with the same path as mine.
        """
        return hash((self.__class__, self.path))
