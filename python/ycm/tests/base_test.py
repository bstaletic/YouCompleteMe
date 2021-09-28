# Copyright (C) 2013 Google Inc.
#               2020 YouCompleteMe contributors
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

import vim
from hamcrest import assert_that, equal_to
from unittest import TestCase

from ycm import base


class BaseTest( TestCase ):
  def test_AdjustCandidateInsertionText_Basic( self ):
    vim.current.buffer[ 0 ] = 'bar'
    vim.current.window.cursor = ( 1, 0 )
    assert_that( [ { 'word': 'foo',    'abbr': 'foobar' } ],
        equal_to( base.AdjustCandidateInsertionText( [
          { 'word': 'foobar', 'abbr': '' } ] ) ) )


  def test_AdjustCandidateInsertionText_ParenInTextAfterCursor( self ):
    vim.current.buffer[ 0 ] = 'bar(zoo'
    vim.current.window.cursor = ( 1, 0 )
    assert_that( [ { 'word': 'foo',    'abbr': 'foobar' } ],
        equal_to( base.AdjustCandidateInsertionText( [
          { 'word': 'foobar', 'abbr': '' } ] ) ) )


  def test_AdjustCandidateInsertionText_PlusInTextAfterCursor( self ):
    vim.current.buffer[ 0 ] = 'bar+zoo'
    vim.current.window.cursor = ( 1, 0 )
    assert_that( [ { 'word': 'foo',    'abbr': 'foobar' } ],
        equal_to( base.AdjustCandidateInsertionText( [
          { 'word': 'foobar', 'abbr': '' } ] ) ) )


  def test_AdjustCandidateInsertionText_WhitespaceInTextAfterCursor( self ):
    vim.current.buffer[ 0 ] = 'bar zoo'
    vim.current.window.cursor = ( 1, 0 )
    assert_that( [ { 'word': 'foo',    'abbr': 'foobar' } ],
        equal_to( base.AdjustCandidateInsertionText( [
          { 'word': 'foobar', 'abbr': '' } ] ) ) )


  def test_AdjustCandidateInsertionText_MoreThanWordMatchingAfterCursor( self ):
    vim.current.buffer[ 0 ] = 'bar.h'
    vim.current.window.cursor = ( 1, 0 )
    assert_that( [ { 'word': 'foo', 'abbr': 'foobar.h' } ],
        equal_to( base.AdjustCandidateInsertionText( [
          { 'word': 'foobar.h', 'abbr': '' } ] ) ) )

    vim.current.buffer[ 0 ] = 'bar(zoo'
    vim.current.window.cursor = ( 1, 0 )
    assert_that( [ { 'word': 'foo', 'abbr': 'foobar(zoo' } ],
        equal_to( base.AdjustCandidateInsertionText( [
          { 'word': 'foobar(zoo', 'abbr': '' } ] ) ) )


  def test_AdjustCandidateInsertionText_NotSuffix( self ):
    vim.current.buffer[ 0 ] = 'bar'
    vim.current.window.cursor = ( 1, 0 )
    assert_that( [ { 'word': 'foofoo', 'abbr': 'foofoo' } ],
        equal_to( base.AdjustCandidateInsertionText( [
          { 'word': 'foofoo', 'abbr': '' } ] ) ) )


  def test_AdjustCandidateInsertionText_NothingAfterCursor( self ):
    vim.current.buffer[ 0 ] = ''
    vim.current.window.cursor = ( 1, 0 )
    assert_that( [ { 'word': 'foofoo', 'abbr': '' },
      { 'word': 'zobar',  'abbr': '' } ],
      equal_to( base.AdjustCandidateInsertionText( [
        { 'word': 'foofoo', 'abbr': '' },
        { 'word': 'zobar',  'abbr': '' } ] ) ) )


  def test_AdjustCandidateInsertionText_MultipleStrings( self ):
    vim.current.buffer[ 0 ] = 'bar'
    vim.current.window.cursor = ( 1, 0 )
    assert_that( [ { 'word': 'foo',    'abbr': 'foobar' },
      { 'word': 'zo',     'abbr': 'zobar' },
      { 'word': 'q',      'abbr': 'qbar' },
      { 'word': '',       'abbr': 'bar' }, ],
      equal_to( base.AdjustCandidateInsertionText( [
        { 'word': 'foobar', 'abbr': '' },
        { 'word': 'zobar',  'abbr': '' },
        { 'word': 'qbar',   'abbr': '' },
        { 'word': 'bar',    'abbr': '' } ] ) ) )


  def test_AdjustCandidateInsertionText_DontTouchAbbr( self ):
    vim.current.buffer[ 0 ] = 'bar'
    vim.current.window.cursor = ( 1, 0 )
    assert_that( [ { 'word': 'foo',    'abbr': '1234' } ],
        equal_to( base.AdjustCandidateInsertionText( [
          { 'word': 'foobar', 'abbr': '1234' } ] ) ) )


  def test_AdjustCandidateInsertionText_NoAbbr( self ):
    vim.current.buffer[ 0 ] = 'bar'
    vim.current.window.cursor = ( 1, 0 )
    assert_that( [ { 'word': 'foo', 'abbr': 'foobar' } ],
        equal_to( base.AdjustCandidateInsertionText( [
          { 'word': 'foobar' } ] ) ) )


  def test_OverlapLength_Basic( self ):
    assert_that( 3, equal_to( base.OverlapLength( 'foo bar', 'bar zoo' ) ) )
    assert_that( 3, equal_to( base.OverlapLength( 'foobar', 'barzoo' ) ) )


  def test_OverlapLength_BasicWithUnicode( self ):
    assert_that( 3, equal_to( base.OverlapLength( 'bar fäö', 'fäö bar' ) ) )
    assert_that( 3, equal_to( base.OverlapLength( 'zoofäö', 'fäözoo' ) ) )


  def test_OverlapLength_OneCharOverlap( self ):
    assert_that( 1, equal_to( base.OverlapLength( 'foo b', 'b zoo' ) ) )


  def test_OverlapLength_SameStrings( self ):
    assert_that( 6, equal_to( base.OverlapLength( 'foobar', 'foobar' ) ) )


  def test_OverlapLength_Substring( self ):
    assert_that( 6, equal_to( base.OverlapLength( 'foobar', 'foobarzoo' ) ) )
    assert_that( 6, equal_to( base.OverlapLength( 'zoofoobar', 'foobar' ) ) )


  def test_OverlapLength_LongestOverlap( self ):
    assert_that( 7, equal_to( base.OverlapLength( 'bar foo foo',
                                                  'foo foo bar' ) ) )


  def test_OverlapLength_EmptyInput( self ):
    assert_that( 0, equal_to( base.OverlapLength( '', 'goobar' ) ) )
    assert_that( 0, equal_to( base.OverlapLength( 'foobar', '' ) ) )
    assert_that( 0, equal_to( base.OverlapLength( '', '' ) ) )


  def test_OverlapLength_NoOverlap( self ):
    assert_that( 0, equal_to( base.OverlapLength( 'foobar', 'goobar' ) ) )
    assert_that( 0, equal_to( base.OverlapLength( 'foobar', '(^($@#$#@' ) ) )
    assert_that( 0, equal_to( base.OverlapLength( 'foo bar zoo',
                                                  'foo zoo bar' ) ) )


  def test_LastEnteredCharIsIdentifierChar_Basic( self ):
    vim.current.buffer.options[ 'ft' ] = b''
    vim.current.buffer[ 0 ] = 'abc'

    for column in range( 3 ):
      with self.subTest( column = column ):
        vim.current.window.cursor = ( 1, column + 1 )
        assert_that( base.LastEnteredCharIsIdentifierChar() )

  def test_LastEnteredCharIsIdentifierChar_FiletypeHtml( self ):
    vim.current.buffer.options[ 'ft' ] = b'html'
    vim.current.buffer[ 0 ] = 'ab-'
    vim.current.window.cursor = ( 1, 3 )
    assert_that( base.LastEnteredCharIsIdentifierChar() )


  def test_LastEnteredCharIsIdentifierChar_ColumnIsZero( self ):
    vim.current.buffer[ 0 ] = 'abc'
    vim.current.window.cursor = ( 1, 0 )
    assert_that( not base.LastEnteredCharIsIdentifierChar() )


  def test_LastEnteredCharIsIdentifierChar_LineEmpty( self ):
    vim.current.buffer.options[ 'ft' ] = b''
    vim.current.buffer[ 0 ] = ''
    vim.current.window.cursor = ( 1, 3 )
    assert_that( not base.LastEnteredCharIsIdentifierChar() )
    vim.current.window.cursor = ( 1, 0 )
    assert_that( not base.LastEnteredCharIsIdentifierChar() )


  def test_LastEnteredCharIsIdentifierChar_NotIdentChar( self ):
    vim.current.buffer.options[ 'ft' ] = b''
    vim.current.buffer[ 0 ] = 'ab;'
    vim.current.window.cursor = ( 1, 3 )
    # assert_that( not base.LastEnteredCharIsIdentifierChar() )
    vim.current.buffer[ 0 ] = ';'
    vim.current.window.cursor = ( 1, 1 )
    assert_that( not base.LastEnteredCharIsIdentifierChar() )
    vim.current.buffer[ 0 ] = 'ab-'
    vim.current.window.cursor = ( 1, 3 )
    # assert_that( not base.LastEnteredCharIsIdentifierChar() )


  def test_LastEnteredCharIsIdentifierChar_Unicode( self ):
    vim.current.buffer.options[ 'ft' ] = b''
    # CurrentColumn returns a byte offset and character ø is 2 bytes length.
    vim.current.buffer[ 0 ] = 'føo( ' # NOTE: Had to add a 6th byte in the line.
    vim.current.window.cursor = ( 1, 6 )
    assert_that( not base.LastEnteredCharIsIdentifierChar() )
    vim.current.window.cursor = ( 1, 4 )
    assert_that( base.LastEnteredCharIsIdentifierChar() )
    vim.current.window.cursor = ( 1, 3 )
    assert_that( base.LastEnteredCharIsIdentifierChar() )
    vim.current.window.cursor = ( 1, 1 )
    assert_that( base.LastEnteredCharIsIdentifierChar() )


  def test_CurrentIdentifierFinished_Basic( self ):
    vim.current.buffer.options[ 'ft' ] = b''
    vim.current.buffer[ 0 ] = 'ab;'
    vim.current.window.cursor = ( 1, 3 )
    # assert_that( base.CurrentIdentifierFinished() )
    vim.current.window.cursor = ( 1, 2 )
    assert_that( not base.CurrentIdentifierFinished() )
    vim.current.window.cursor = ( 1, 1 )
    assert_that( not base.CurrentIdentifierFinished() )


  def test_CurrentIdentifierFinished_NothingBeforeColumn( self ):
    vim.current.buffer[ 0 ] = 'ab;'
    vim.current.window.cursor = ( 1, 0 )
    assert_that( base.CurrentIdentifierFinished() )
    vim.current.buffer[ 0 ] = ''
    assert_that( base.CurrentIdentifierFinished() )


  def test_CurrentIdentifierFinished_InvalidColumn( self ):
    # NOTE: This test isn't doing anything useful, because there is no "invalid
    # column". Setting the cursor just fails silently.
    vim.current.buffer.options[ 'ft' ] = b''
    vim.current.buffer[ 0 ] = ''
    vim.current.window.cursor = ( 1, 5 )
    assert_that( base.CurrentIdentifierFinished() )
    vim.current.buffer[ 0 ] = 'abc'
    vim.current.window.cursor = ( 1, 5 )
    assert_that( not base.CurrentIdentifierFinished() )
    vim.current.buffer[ 0 ] = 'ab;'
    vim.current.window.cursor = ( 1, 4 )
    # assert_that( base.CurrentIdentifierFinished() )


  def test_CurrentIdentifierFinished_InMiddleOfLine( self ):
    vim.current.buffer.options[ 'ft' ] = b''
    vim.current.window.cursor = ( 1, 4 )
    vim.current.buffer[ 0 ] = 'bar.zoo'
    assert_that( base.CurrentIdentifierFinished() )
    vim.current.buffer[ 0 ] = 'bar(zoo'
    assert_that( base.CurrentIdentifierFinished() )
    vim.current.buffer[ 0 ] = 'bar-zoo'
    assert_that( base.CurrentIdentifierFinished() )


  def test_CurrentIdentifierFinished_Html( self ):
    vim.current.buffer.options[ 'ft' ] = b'html'
    vim.current.buffer[ 0 ] = 'bar-zoo'
    vim.current.window.cursor = ( 1, 4 )
    assert_that( not base.CurrentIdentifierFinished() )


  def test_CurrentIdentifierFinished_WhitespaceOnly( self ):
    vim.current.buffer.options[ 'ft' ] = b''
    vim.current.buffer[ 0 ] = '\t'
    vim.current.window.cursor = ( 1, 1 )
    assert_that( base.CurrentIdentifierFinished() )
    vim.current.buffer[ 0 ] = '\t    '
    vim.current.window.cursor = ( 1, 3 )
    assert_that( base.CurrentIdentifierFinished() )
    vim.current.buffer[ 0 ] = '\t\t\t\t'
    vim.current.window.cursor = ( 1, 3 )
    assert_that( base.CurrentIdentifierFinished() )


  def test_CurrentIdentifierFinished_Unicode( self ):
    vim.current.buffer.options[ 'ft' ] = b''
    vim.current.buffer[ 0 ] = 'føo  ' # NOTE: Had to add a 6th byte in the line.
    vim.current.window.cursor = ( 1, 6 )
    assert_that( base.CurrentIdentifierFinished() )
    vim.current.window.cursor = ( 1, 5 )
    assert_that( base.CurrentIdentifierFinished() )
    vim.current.window.cursor = ( 1, 4 )
    assert_that( not base.CurrentIdentifierFinished() )
    vim.current.window.cursor = ( 1, 3 )
    assert_that( not base.CurrentIdentifierFinished() )
