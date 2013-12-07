from __future__ import division, absolute_import

from bp.errors import LinkError
from bp.generic import (genericChildren, genericDescendant, genericParents,
                        genericSibling, genericWalk)


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
    walk = genericWalk
    sibling = genericSibling
    descendant = genericDescendant

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
