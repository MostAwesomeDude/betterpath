from unittest import TestCase

from bp.util import modeIsWriting


class TestModeIsWriting(TestCase):

    def test_rIsReadOnly(self):
        self.assertFalse(modeIsWriting("r"))

    def test_rbIsReadOnly(self):
        self.assertFalse(modeIsWriting("rb"))

    def test_aIsWriting(self):
        self.assertTrue(modeIsWriting("a"))
