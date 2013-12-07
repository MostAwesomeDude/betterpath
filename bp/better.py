from __future__ import division, absolute_import

from bp.errors import LinkError
from bp.generic import (genericChildren, genericDescendant, genericParents,
                        genericSegmentsFrom, genericSibling, genericWalk)


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
    segmentsFrom = genericSegmentsFrom

    def __hash__(self):
        """
        Hash the same as another L{FilePath} with the same path as mine.
        """
        return hash((self.__class__, self.path))
