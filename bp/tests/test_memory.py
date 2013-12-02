from bp.memory import MemoryFS, MemoryPath, format_memory_path
from bp.tests.test_paths import AbstractFilePathTestCase


def heads(t):
    for i in range(len(t)):
        yield t[:i]


class MemoryPathTestCase(AbstractFilePathTestCase):

    def subdir(self, *dirname):
        for head in heads(dirname):
            self.fs._dirs.add(head)
        self.fs._dirs.add(dirname)

    def subfile(self, *dirname):
        for head in heads(dirname):
            self.fs._dirs.add(head)
        return self.fs.open(dirname)

    def setUp(self):
        self.fs = MemoryFS()

        AbstractFilePathTestCase.setUp(self)

        self.path = MemoryPath(self.fs)
        self.root = self.path
        self.all = self.fs._dirs | set(self.fs._store.keys())
        self.all = set(format_memory_path(p, "/") for p in self.all)
