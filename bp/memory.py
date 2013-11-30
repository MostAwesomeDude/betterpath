from StringIO import StringIO

from zope.interface import implementer

from bp.abstract import IFilePath
from bp.better import AbstractFilePath

DIR = object()
FILE = object()


class MemoryFile(StringIO):
    """
    A file-like object that saves itself to an external mapping when closed.
    """

    def __init__(self, store, key, buf=""):
        StringIO.__init__(self, buf)
        self._target = store, key

    def close(self):
        buf = self.getvalue()
        store, key = self._target
        store[key] = buf
        StringIO.close(self)


class MemoryFS(object):
    """
    An in-memory filesystem.
    """

    def __init__(self):
        self._store = {}
        self._dirs = set()

    def open(self, path):
        if path in self._dirs:
            raise Exception("Directories cannot be opened")
        elif path in self._store:
            return MemoryFile(self._store, path, self._store[path])
        else:
            return MemoryFile(self._store, path)


@implementer(IFilePath)
class MemoryPath(AbstractFilePath):
    """
    An IFilePath which shows a view into a MemoryFS.
    """

    sep = "/"

    def __init__(self, fs, path=()):
        """
        Create a new path in memory.
        """

        self._fs = fs
        self._path = path

    def __eq__(self, other):
        return self._fs == other._fs and self._path == other._path

    @property
    def path(self):
        return self.sep.join(("/mem",) + self._path)

    def changed(self):
        pass

    def isdir(self):
        return self._path in self._fs._dirs

    def isfile(self):
        return self._path in self._fs._store

    def exists(self):
        return self.isdir() or self.isfile()

    def parent(self):
        if self._path:
            return MemoryPath(self._fs, self._path[:-1])
        else:
            return self

    def child(self, name):
        return MemoryPath(self._fs, self._path + (name,))

    def basename(self):
        return self._path[-1] if self._path else ""

    def open(self, mode="r"):
        return self._fs.open(self._path)

    def getsize(self):
        if self._path in self._fs._store:
            return len(self._fs._store[self._path])
        else:
            raise Exception("Non-file has no size")

    def getModificationTime(self):
        return 0.0

    def getStatusChangeTime(self):
        return 0.0

    def getAccessTime(self):
        return 0.0

    def listdir(self):
        """
        Pretend that we are a directory and get a listing of child names.
        """

        i = self._fs._store.iterkeys()

        # Linear-time search. Could be better.
        p = self._path
        l = len(p) + 1
        ks = [t[-1] for t in i if t[:-1] == p and len(t) == l]

        return ks
