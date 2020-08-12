# Copyright (C) 2016, Davit Samvelyan
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

from ycm import vimsupport
from ycm.client.event_notification import EventNotification
from ycm.diagnostic_interface import DiagnosticInterface
from typing import Dict, List, Union

DIAGNOSTIC_UI_FILETYPES = { 'cpp', 'cs', 'c', 'objc', 'objcpp', 'cuda',
                            'javascript', 'javascriptreact', 'typescript',
                            'typescriptreact' }


# Emulates Vim buffer
# Used to store buffer related information like diagnostics, latest parse
# request. Stores buffer change tick at the parse request moment, allowing
# to effectively determine whether reparse is needed for the buffer.
class Buffer:

  def __init__( self, bufnr: int, user_options: Dict[str, Union[str, int, Dict[str, int]]], filetypes: List[str] ) -> None:
    self._number = bufnr
    self._parse_tick = 0
    self._handled_tick = 0
    self._parse_request = None
    self._should_resend = False
    self._diag_interface = DiagnosticInterface( bufnr, user_options )
    self.UpdateFromFileTypes( filetypes )


  def FileParseRequestReady( self, block: bool = False ) -> bool:
    return bool( self._parse_request and
                 ( block or self._parse_request.Done() ) )


  def SendParseRequest( self, extra_data: Dict[str, List[str]] ) -> None:
    # Don't send a parse request if one is in progress
    if self._parse_request is not None and not self._parse_request.Done():
      self._should_resend = True
      return

    self._should_resend = False

    self._parse_request = EventNotification( 'FileReadyToParse',
                                             extra_data = extra_data )
    self._parse_request.Start()
    # Decrement handled tick to ensure correct handling when we are forcing
    # reparse on buffer visit and changed tick remains the same.
    self._handled_tick -= 1
    self._parse_tick = self._ChangedTick()


  def NeedsReparse( self ):
    return self._parse_tick != self._ChangedTick()


  def ShouldResendParseRequest( self ) -> bool:
    return ( self._should_resend
             or ( bool( self._parse_request )
                  and self._parse_request.ShouldResend() ) )


  def UpdateDiagnostics( self, force: bool = False ) -> None:
    if force or not self._async_diags:
      self.UpdateWithNewDiagnostics( self._parse_request.Response() )
    else:
      # We need to call the response method, because it might throw an exception
      # or require extra config confirmation, even if we don't actually use the
      # diagnostics.
      self._parse_request.Response()


  def UpdateWithNewDiagnostics( self, diagnostics: Union[List[Dict[str, Union[str, Dict[str, Union[int, str]], Dict[str, Dict[str, Union[int, str]]]]]], List[Union[Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Dict[str, Union[int, str]]], str, bool]], Dict[str, Union[str, Dict[str, Union[int, str]], Dict[str, Dict[str, Union[int, str]]], List[Dict[str, Dict[str, Union[int, str]]]], bool]]]], List[Dict[str, Union[str, Dict[str, Union[int, str]]]]], List[Dict[str, Union[str, Dict[str, Union[int, str]], Dict[str, Dict[str, Union[int, str]]], List[Dict[str, Dict[str, Union[int, str]]]], bool]]], List[Dict[str, Union[Dict[str, Union[int, str]], Dict[str, Dict[str, Union[int, str]]], str, bool]]]] ) -> None:
    self._diag_interface.UpdateWithNewDiagnostics( diagnostics )


  def UpdateMatches( self ) -> None:
    self._diag_interface.UpdateMatches()


  def PopulateLocationList( self ) -> bool:
    return self._diag_interface.PopulateLocationList()


  def GetResponse( self ):
    return self._parse_request.Response()


  def IsResponseHandled( self ) -> bool:
    return self._handled_tick == self._parse_tick


  def MarkResponseHandled( self ) -> None:
    self._handled_tick = self._parse_tick


  def OnCursorMoved( self ) -> None:
    self._diag_interface.OnCursorMoved()


  def GetErrorCount( self ) -> int:
    return self._diag_interface.GetErrorCount()


  def GetWarningCount( self ) -> int:
    return self._diag_interface.GetWarningCount()


  def UpdateFromFileTypes( self, filetypes: List[str] ) -> None:
    self._filetypes = filetypes
    self._async_diags = not any( x in DIAGNOSTIC_UI_FILETYPES
      for x in filetypes )


  def _ChangedTick( self ) -> int:
    return vimsupport.GetBufferChangedTick( self._number )


class BufferDict( dict ):

  def __init__( self, user_options: Dict[str, Union[str, int, Dict[str, int], Dict[str, List[str]], List[str]]] ) -> None:
    self._user_options = user_options


  def __missing__( self, key: int ) -> Buffer:
    # Python does not allow to return assignment operation result directly
    new_value = self[ key ] = Buffer(
      key,
      self._user_options,
      vimsupport.GetBufferFiletypes( key ) )

    return new_value
