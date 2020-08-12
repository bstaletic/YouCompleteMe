# Copyright (C) 2013-2018 YouCompleteMe contributors
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

import logging
import json
import vim
from base64 import b64decode, b64encode
from hmac import compare_digest
from urllib.parse import urljoin, urlparse
from ycm import vimsupport
from ycmd.utils import ToBytes, GetCurrentDirectory
from ycmd.hmac_utils import CreateRequestHmac, CreateHmac
from ycmd.responses import ServerError, UnknownExtraConf
from concurrent.futures._base import Future
from requests.models import Response
from typing import Any, Dict, List, Optional, Union
from unittest.mock import MagicMock

_HEADERS = { 'content-type': 'application/json' }
_CONNECT_TIMEOUT_SEC = 0.01
# Setting this to None seems to screw up the Requests/urllib3 libs.
_READ_TIMEOUT_SEC = 30
_HMAC_HEADER = 'x-ycm-hmac'
_logger = logging.getLogger( __name__ )


class BaseRequest:

  def __init__( self ) -> None:
    self._should_resend = False


  def Start( self ):
    pass


  def Done( self ) -> bool:
    return True


  def Response( self ):
    return {}


  def ShouldResend( self ) -> bool:
    return self._should_resend


  def HandleFuture( self,
                    future: Union[MagicMock, Future],
                    display_message: bool = True,
                    truncate_message: bool = False ) -> Any:
    """Get the server response from a |future| object and catch any exception
    while doing so. If an exception is raised because of a unknown
    .ycm_extra_conf.py file, load the file or ignore it after asking the user.
    An identical request should be sent again to the server. For other
    exceptions, log the exception and display its message to the user on the Vim
    status line. Unset the |display_message| parameter to hide the message from
    the user. Set the |truncate_message| parameter to avoid hit-enter prompts
    from this message."""
    try:
      try:
        return _JsonFromFuture( future )
      except UnknownExtraConf as e:
        if vimsupport.Confirm( str( e ) ):
          _LoadExtraConfFile( e.extra_conf_file )
        else:
          _IgnoreExtraConfFile( e.extra_conf_file )
        self._should_resend = True
    except BaseRequest.Requests().exceptions.ConnectionError as e:
      # We don't display this exception to the user since it is likely to happen
      # for each subsequent request (typically if the server crashed) and we
      # don't want to spam the user with it.
      _logger.error( e )
    except Exception as e:
      _logger.exception( 'Error while handling server response' )
      if display_message:
        DisplayServerException( e, truncate_message )

    return None


  # This method blocks
  # |timeout| is num seconds to tolerate no response from server before giving
  # up; see Requests docs for details (we just pass the param along).
  # See the HandleFuture method for the |display_message| and |truncate_message|
  # parameters.
  def GetDataFromHandler( self,
                          handler: str,
                          timeout: int = _READ_TIMEOUT_SEC,
                          display_message: bool = True,
                          truncate_message: bool = False,
                          payload: None = None ) -> Optional[bool]:
    return self.HandleFuture(
        self.GetDataFromHandlerAsync( handler, timeout, payload ),
        display_message,
        truncate_message )


  def GetDataFromHandlerAsync( self,
                               handler: str,
                               timeout: int = _READ_TIMEOUT_SEC,
                               payload: Optional[Dict[str, str]] = None ) -> Future:
    return BaseRequest._TalkToHandlerAsync(
        '', handler, 'GET', timeout, payload )


  # This is the blocking version of the method. See below for async.
  # |timeout| is num seconds to tolerate no response from server before giving
  # up; see Requests docs for details (we just pass the param along).
  # See the HandleFuture method for the |display_message| and |truncate_message|
  # parameters.
  def PostDataToHandler( self,
                         data: Dict[str, Union[str, int, Dict[str, Dict[str, Union[List[str], str]]], List[Dict[str, Union[int, str]]], Dict[str, str]]],
                         handler: str,
                         timeout: Union[int, float] = _READ_TIMEOUT_SEC,
                         display_message: bool = True,
                         truncate_message: bool = False ) -> Any:
    return self.HandleFuture(
        BaseRequest.PostDataToHandlerAsync( data, handler, timeout ),
        display_message,
        truncate_message )


  # This returns a future! Use HandleFuture to get the value.
  # |timeout| is num seconds to tolerate no response from server before giving
  # up; see Requests docs for details (we just pass the param along).
  @staticmethod
  def PostDataToHandlerAsync( data: Dict[str, Any], handler: str, timeout: Union[int, float] = _READ_TIMEOUT_SEC ) -> Future:
    return BaseRequest._TalkToHandlerAsync( data, handler, 'POST', timeout )


  # This returns a future! Use HandleFuture to get the value.
  # |method| is either 'POST' or 'GET'.
  # |timeout| is num seconds to tolerate no response from server before giving
  # up; see Requests docs for details (we just pass the param along).
  @staticmethod
  def _TalkToHandlerAsync( data: Any,
                           handler: str,
                           method: str,
                           timeout: Union[int, float] = _READ_TIMEOUT_SEC,
                           payload: Optional[Dict[str, str]] = None ) -> Future:
    request_uri = _BuildUri( handler )
    if method == 'POST':
      sent_data = _ToUtf8Json( data )
      headers = BaseRequest._ExtraHeaders( method,
                                           request_uri,
                                           sent_data )
      _logger.debug( 'POST %s\n%s\n%s', request_uri, headers, sent_data )

      return BaseRequest.Session().post(
        request_uri,
        data = sent_data,
        headers = headers,
        timeout = ( _CONNECT_TIMEOUT_SEC, timeout ) )

    headers = BaseRequest._ExtraHeaders( method, request_uri )

    _logger.debug( 'GET %s (%s)\n%s', request_uri, payload, headers )

    return BaseRequest.Session().get(
      request_uri,
      headers = headers,
      timeout = ( _CONNECT_TIMEOUT_SEC, timeout ),
      params = payload )


  @staticmethod
  def _ExtraHeaders( method: str, request_uri: bytes, request_body: Optional[bytes] = None ) -> Dict[str, Union[str, bytes]]:
    if not request_body:
      request_body = bytes( b'' )
    headers = dict( _HEADERS )
    headers[ _HMAC_HEADER ] = b64encode(
        CreateRequestHmac( ToBytes( method ),
                           ToBytes( urlparse( request_uri ).path ),
                           request_body,
                           BaseRequest.hmac_secret ) )
    return headers


  # These two methods exist to avoid importing the requests module at startup;
  # reducing loading time since this module is slow to import.
  @classmethod
  def Requests( cls ):
    try:
      return cls.requests
    except AttributeError:
      import requests
      cls.requests = requests
      return requests


  @classmethod
  def Session( cls ):
    try:
      return cls.session
    except AttributeError:
      from ycm.unsafe_thread_pool_executor import UnsafeThreadPoolExecutor
      from requests_futures.sessions import FuturesSession
      executor = UnsafeThreadPoolExecutor( max_workers = 30 )
      cls.session = FuturesSession( executor = executor )
      return cls.session


  server_location = ''
  hmac_secret = ''


def BuildRequestData( buffer_number: Optional[int] = None ) -> Dict[str, Union[str, int, Dict[str, Dict[str, Union[List[str], str]]]]]:
  """Build request for the current buffer or the buffer with number
  |buffer_number| if specified."""
  working_dir = GetCurrentDirectory()
  current_buffer = vim.current.buffer

  if buffer_number and current_buffer.number != buffer_number:
    # Cursor position is irrelevant when filepath is not the current buffer.
    buffer_object = vim.buffers[ buffer_number ]
    filepath = vimsupport.GetBufferFilepath( buffer_object )
    return {
      'filepath': filepath,
      'line_num': 1,
      'column_num': 1,
      'working_dir': working_dir,
      'file_data': vimsupport.GetUnsavedAndSpecifiedBufferData( buffer_object,
                                                                filepath )
    }

  current_filepath = vimsupport.GetBufferFilepath( current_buffer )
  line, column = vimsupport.CurrentLineAndColumn()

  return {
    'filepath': current_filepath,
    'line_num': line + 1,
    'column_num': column + 1,
    'working_dir': working_dir,
    'file_data': vimsupport.GetUnsavedAndSpecifiedBufferData( current_buffer,
                                                              current_filepath )
  }


def _JsonFromFuture( future: Union[MagicMock, Future] ) -> Any:
  response = future.result()
  _logger.debug( 'RX: %s\n%s', response, response.text )
  _ValidateResponseObject( response )
  if response.status_code == BaseRequest.Requests().codes.server_error:
    raise MakeServerException( response.json() )

  # We let Requests handle the other status types, we only handle the 500
  # error code.
  response.raise_for_status()

  if response.text:
    return response.json()
  return None


def _LoadExtraConfFile( filepath: str ) -> None:
  BaseRequest().PostDataToHandler( { 'filepath': filepath },
                                   'load_extra_conf_file' )


def _IgnoreExtraConfFile( filepath: str ) -> None:
  BaseRequest().PostDataToHandler( { 'filepath': filepath },
                                   'ignore_extra_conf_file' )


def DisplayServerException( exception: Union[RuntimeError, ServerError], truncate_message: bool = False ) -> None:
  serialized_exception = str( exception )

  # We ignore the exception about the file already being parsed since it comes
  # up often and isn't something that's actionable by the user.
  if 'already being parsed' in serialized_exception:
    return
  vimsupport.PostVimMessage( serialized_exception, truncate = truncate_message )


def _ToUtf8Json( data: Dict[str, Any] ) -> bytes:
  return ToBytes( json.dumps( data ) if data else None )


def _ValidateResponseObject( response: Response ) -> bool:
  our_hmac = CreateHmac( response.content, BaseRequest.hmac_secret )
  their_hmac = ToBytes( b64decode( response.headers[ _HMAC_HEADER ] ) )
  if not compare_digest( our_hmac, their_hmac ):
    raise RuntimeError( 'Received invalid HMAC for response!' )
  return True


def _BuildUri( handler: str ) -> bytes:
  return ToBytes( urljoin( BaseRequest.server_location, handler ) )


def MakeServerException( data: Dict[str, Union[str, Dict[str, str]]] ) -> ServerError:
  if data[ 'exception' ][ 'TYPE' ] == UnknownExtraConf.__name__:
    return UnknownExtraConf( data[ 'exception' ][ 'extra_conf_file' ] )

  return ServerError( f'{ data[ "exception" ][ "TYPE" ] }: '
                      f'{ data[ "message" ] }' )
