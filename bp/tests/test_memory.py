from bp.memory import MemoryFS, MemoryPath
from bp.tests.test_paths import AbstractFilePathTestCase
from bp.zippath import ZipArchive


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
