from __future__ import division, absolute_import

import errno
import os

from bp.errors import LinkError, UnlistableError
from bp.win32 import (ERROR_FILE_NOT_FOUND, ERROR_PATH_NOT_FOUND,
                      ERROR_INVALID_NAME, ERROR_DIRECTORY, WindowsError)


class AbstractFilePath(object):
    """
    Abstract implementation of an L{IFilePath}; must be completed by a
    subclass.

    This class primarily exists to provide common implementations of certain
    methods in L{IFilePath}. It is *not* a required parent class for
    L{IFilePath} implementations, just a useful starting point.
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

    def parents(self):
        """
        Retrieve an iterator of all the ancestors of this path.

        @return: an iterator of all the ancestors of this path, from the most
        recent (its immediate parent) to the root of its filesystem.
        """
        path = self
        parent = path.parent()
        # root.parent() == root, so this means "are we the root"
        while path != parent:
            yield parent
            path = parent
            parent = parent.parent()

    def children(self):
        """
        List the children of this path object.

        @raise OSError: If an error occurs while listing the directory.  If the
        error is 'serious', meaning that the operation failed due to an access
        violation, exhaustion of some kind of resource (file descriptors or
        memory), OSError or a platform-specific variant will be raised.

        @raise UnlistableError: If the inability to list the directory is due
        to this path not existing or not being a directory, the more specific
        OSError subclass L{UnlistableError} is raised instead.

        @return: an iterable of all currently-existing children of this object.
        """
        try:
            subnames = self.listdir()
        except WindowsError as winErrObj:
            # WindowsError is an OSError subclass, so if not for this clause
            # the OSError clause below would be handling these.  Windows error
            # codes aren't the same as POSIX error codes, so we need to handle
            # them differently.

            # Under Python 2.5 on Windows, WindowsError has a winerror
            # attribute and an errno attribute.  The winerror attribute is
            # bound to the Windows error code while the errno attribute is
            # bound to a translation of that code to a perhaps equivalent POSIX
            # error number.

            # Under Python 2.4 on Windows, WindowsError only has an errno
            # attribute.  It is bound to the Windows error code.

            # For simplicity of code and to keep the number of paths through
            # this suite minimal, we grab the Windows error code under either
            # version.

            # Furthermore, attempting to use os.listdir on a non-existent path
            # in Python 2.4 will result in a Windows error code of
            # ERROR_PATH_NOT_FOUND.  However, in Python 2.5,
            # ERROR_FILE_NOT_FOUND results instead. -exarkun
            winerror = getattr(winErrObj, 'winerror', winErrObj.errno)
            if winerror not in (ERROR_PATH_NOT_FOUND,
                                ERROR_FILE_NOT_FOUND,
                                ERROR_INVALID_NAME,
                                ERROR_DIRECTORY):
                raise
            raise UnlistableError(winErrObj)
        except OSError as ose:
            if ose.errno not in (errno.ENOENT, errno.ENOTDIR):
                # Other possible errors here, according to linux manpages:
                # EACCES, EMIFLE, ENFILE, ENOMEM.  None of these seem like the
                # sort of thing which should be handled normally. -glyph
                raise
            raise UnlistableError(ose)
        return map(self.child, subnames)

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
        yield self
        if self.isdir():
            for c in self.children():
                # we should first see if it's what we want, then we
                # can walk through the directory
                if (descend is None or descend(c)):
                    for subc in c.walk(descend):
                        if os.path.realpath(self.path).startswith(
                                os.path.realpath(subc.path)):
                            raise LinkError("Cycle in file graph.")
                        yield subc
                else:
                    yield c

    def sibling(self, path):
        """
        Return a L{FilePath} with the same directory as this instance but with
        a basename of C{path}.

        @param path: The basename of the L{FilePath} to return.
        @type path: L{str}

        @return: The sibling path.
        @rtype: L{FilePath}
        """
        return self.parent().child(path)

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

    # new in 8.0
    def __hash__(self):
        """
        Hash the same as another L{FilePath} with the same path as mine.
        """
        return hash((self.__class__, self.path))

    # pending deprecation in 8.0
    def getmtime(self):
        """
        Deprecated.  Use getModificationTime instead.
        """
        return int(self.getModificationTime())

    def getatime(self):
        """
        Deprecated.  Use getAccessTime instead.
        """
        return int(self.getAccessTime())

    def getctime(self):
        """
        Deprecated.  Use getStatusChangeTime instead.
        """
        return int(self.getStatusChangeTime())
