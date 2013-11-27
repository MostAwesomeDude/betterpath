# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Win32 utilities.

@var O_BINARY: the 'binary' mode flag on Windows, or 0 on other platforms, so
    it may safely be OR'ed into a mask for os.open.
"""

from __future__ import division, absolute_import

import os


isWindows = os.name in ("ce", "nt")

# http://msdn.microsoft.com/library/default.asp
# ?url=/library/en-us/debug/base/system_error_codes.asp
ERROR_FILE_NOT_FOUND = 2
ERROR_PATH_NOT_FOUND = 3
ERROR_INVALID_NAME = 123
ERROR_DIRECTORY = 267

O_BINARY = getattr(os, "O_BINARY", 0)


class FakeWindowsError(OSError):
    """
    Stand-in for sometimes-builtin exception on platforms for which it
    is missing.
    """

try:
    WindowsError = WindowsError
except NameError:
    WindowsError = FakeWindowsError
