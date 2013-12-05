from bp.readonly import ReadOnlyPath
from bp.tests.test_paths import AbstractFilePathTestCase


class ReadOnlyPathTestCase(AbstractFilePathTestCase):

    def setUp(self):
        AbstractFilePathTestCase.setUp(self)

        self.path = ReadOnlyPath(self.path)

    def test_createDirectory(self):
        """
        createDirectory() cannot create new directories on a read-only file
        path.
        """

        self.assertRaises(Exception,
                          self.path.child(b"directory").createDirectory)
