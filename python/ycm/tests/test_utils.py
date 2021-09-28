# Copyright (C) 2011-2019 YouCompleteMe contributors
#
# This file is part of YouCompleteMe.
#
# YouCompleteMe is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# YouCompleteMe is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with YouCompleteMe.  If not, see <http://www.gnu.org/licenses/>.

from collections import defaultdict, namedtuple
from unittest.mock import DEFAULT, MagicMock, patch
from unittest import skip
from hamcrest import assert_that, equal_to
import contextlib
import functools
import json
import os
import re
import sys

from unittest import skipIf

from ycmd.utils import GetCurrentDirectory, OnMac, OnWindows, ToUnicode


WindowsAndMacOnly = skipIf( not OnWindows() or not OnMac(),
                            'Windows and macOS only' )


@contextlib.contextmanager
def CurrentWorkingDirectory( path ):
  old_cwd = GetCurrentDirectory()
  os.chdir( path )
  try:
    yield
  finally:
    os.chdir( old_cwd )


class ExtendedMock( MagicMock ):
  """An extension to the MagicMock class which adds the ability to check that a
  callable is called with a precise set of calls in a precise order.

  Example Usage:
    from ycm.tests.test_utils import ExtendedMock
    @patch( 'test.testing', new_callable = ExtendedMock, ... )
    def my_test( test_testing ):
      ...
  """

  def assert_has_exact_calls( self, calls, any_order = False ):
    self.assert_has_calls( calls, any_order )
    assert_that( self.call_count, equal_to( len( calls ) ) )


def ExpectedFailure( reason, *exception_matchers ):
  """Defines a decorator to be attached to tests. This decorator
  marks the test as being known to fail, e.g. where documenting or exercising
  known incorrect behaviour.

  The parameters are:
    - |reason| a textual description of the reason for the known issue. This
               is used for the skip reason
    - |exception_matchers| additional arguments are hamcrest matchers to apply
                 to the exception thrown. If the matchers don't match, then the
                 test is marked as error, with the original exception.

  If the test fails (for the correct reason), then it is marked as skipped.
  If it fails for any other reason, it is marked as failed.
  If the test passes, then it is also marked as failed."""
  def decorator( test ):
    @functools.wraps( test )
    def Wrapper( *args, **kwargs ):
      try:
        test( *args, **kwargs )
      except Exception as test_exception:
        # Ensure that we failed for the right reason
        test_exception_message = ToUnicode( test_exception )
        try:
          for matcher in exception_matchers:
            assert_that( test_exception_message, matcher )
        except AssertionError:
          # Failed for the wrong reason!
          import traceback
          print( 'Test failed for the wrong reason: ' + traceback.format_exc() )
          # Real failure reason is the *original* exception, we're only trapping
          # and ignoring the exception that is expected.
          raise test_exception

        # Failed for the right reason
        skip( reason )
      else:
        raise AssertionError( f'Test was expected to fail: { reason }' )
    return Wrapper

  return decorator
