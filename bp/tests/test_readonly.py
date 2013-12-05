from bp.readonly import ReadOnlyPath
from bp.tests.test_paths import AbstractFilePathTestCase


class ReadOnlyPathTestCase(AbstractFilePathTestCase):

    def setUp(self):
        AbstractFilePathTestCase.setUp(self)

        self.path = ReadOnlyPath(self.path)
