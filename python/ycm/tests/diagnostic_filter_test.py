# Copyright (C) 2016  YouCompleteMe contributors
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

from ycm.tests.test_utils import MockVimModule
MockVimModule()

from hamcrest import assert_that, equal_to
from ycm.diagnostic_filter import DiagnosticFilter
from typing import Dict, List, Union


def _assert_accept_equals( filter: DiagnosticFilter, text_or_obj: Union[str, Dict[str, str]], expected: bool ) -> None:
  if not isinstance( text_or_obj, dict ):
    text_or_obj = { 'text': text_or_obj }

  assert_that( filter.IsAllowed( text_or_obj ), equal_to( expected ) )


def _assert_accepts( filter: DiagnosticFilter, text: Union[str, Dict[str, str]] ) -> None:
  _assert_accept_equals( filter, text, True )


def _assert_rejects( filter: DiagnosticFilter, text: Union[str, Dict[str, str]] ) -> None:
  _assert_accept_equals( filter, text, False )


def _JavaFilter( config: Dict[str, Union[List[str], str]] ) -> Dict[str, Union[Dict[str, Dict[str, str]], Dict[str, Dict[str, List[str]]]]]:
  return { 'filter_diagnostics' : { 'java': config } }


def _CreateFilterForTypes( opts: Dict[str, Union[Dict[str, Dict[str, str]], Dict[str, Dict[str, List[str]]]]], types: List[str] ) -> DiagnosticFilter:
  return DiagnosticFilter.CreateFromOptions( opts ).SubsetForTypes( types )


def RegexFilter_test() -> None:
  opts = _JavaFilter( { 'regex' : 'taco' } )
  f = _CreateFilterForTypes( opts, [ 'java' ] )

  _assert_rejects( f, 'This is a Taco' )
  _assert_accepts( f, 'This is a Burrito' )


def RegexSingleList_test() -> None:
  opts = _JavaFilter( { 'regex' : [ 'taco' ] } )
  f = _CreateFilterForTypes( opts, [ 'java' ] )

  _assert_rejects( f, 'This is a Taco' )
  _assert_accepts( f, 'This is a Burrito' )


def RegexMultiList_test() -> None:
  opts = _JavaFilter( { 'regex' : [ 'taco', 'burrito' ] } )
  f = _CreateFilterForTypes( opts, [ 'java' ] )

  _assert_rejects( f, 'This is a Taco' )
  _assert_rejects( f, 'This is a Burrito' )


def RegexNotFiltered_test() -> None:
  opts = _JavaFilter( { 'regex' : 'taco' } )
  f = _CreateFilterForTypes( opts, [ 'cs' ] )

  _assert_accepts( f, 'This is a Taco' )
  _assert_accepts( f, 'This is a Burrito' )


def LevelWarnings_test() -> None:
  opts = _JavaFilter( { 'level' : 'warning' } )
  f = _CreateFilterForTypes( opts, [ 'java' ] )

  _assert_rejects( f, { 'text' : 'This is an unimportant taco',
                        'kind' : 'WARNING' } )
  _assert_accepts( f, { 'text' : 'This taco will be shown',
                        'kind' : 'ERROR' } )


def LevelErrors_test() -> None:
  opts = _JavaFilter( { 'level' : 'error' } )
  f = _CreateFilterForTypes( opts, [ 'java' ] )

  _assert_accepts( f, { 'text' : 'This is an IMPORTANT taco',
                        'kind' : 'WARNING' } )
  _assert_rejects( f, { 'text' : 'This taco will NOT be shown',
                        'kind' : 'ERROR' } )


def MultipleFilterTypesTypeTest_test() -> None:

  opts = _JavaFilter( { 'regex' : '.*taco.*',
                        'level' : 'warning' } )
  f = _CreateFilterForTypes( opts, [ 'java' ] )

  _assert_rejects( f, { 'text' : 'This is an unimportant taco',
                        'kind' : 'WARNING' } )
  _assert_rejects( f, { 'text' : 'This taco will NOT be shown',
                        'kind' : 'ERROR' } )
  _assert_accepts( f, { 'text' : 'This burrito WILL be shown',
                        'kind' : 'ERROR' } )


def MergeMultipleFiletypes_test() -> None:

  opts = { 'filter_diagnostics' : {
    'java' : { 'regex' : '.*taco.*' },
    'xml'  : { 'regex' : '.*burrito.*' } } }

  f = _CreateFilterForTypes( opts, [ 'java', 'xml' ] )

  _assert_rejects( f, 'This is a Taco' )
  _assert_rejects( f, 'This is a Burrito' )
  _assert_accepts( f, 'This is some Nachos' )


def CommaSeparatedFiletypes_test() -> None:

  opts = { 'filter_diagnostics' : {
    'java,c,cs' : { 'regex' : '.*taco.*' } } }

  f = _CreateFilterForTypes( opts, [ 'cs' ] )

  _assert_rejects( f, 'This is a Taco' )
  _assert_accepts( f, 'This is a Burrito' )
