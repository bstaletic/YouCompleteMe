# Copyright (C) 2013  Google Inc.
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

from ycm.client.completion_request import CompletionRequest
from typing import Dict, List, Optional, Union
from unittest.mock import MagicMock
from ycm.omni_completer import OmniCompleter
from ycmd.request_wrap import RequestWrap


class OmniCompletionRequest( CompletionRequest ):
  def __init__( self, omni_completer: Union[MagicMock, str, OmniCompleter], request_data: Optional[Union[Dict[str, int], RequestWrap]] ) -> None:
    super( OmniCompletionRequest, self ).__init__( request_data )
    self._omni_completer = omni_completer


  def Start( self ) -> None:
    self._results = self._omni_completer.ComputeCandidates( self.request_data )


  def Done( self ) -> bool:
    return True


  def Response( self ) -> Dict[str, Union[List[Dict[str, Union[int, str]]], int, List[Dict[str, str]]]]:
    return {
      'line': self.request_data[ 'line_num' ],
      'column': self.request_data[ 'column_num' ],
      'completion_start_column': self.request_data[ 'start_column' ],
      'completions': self._results
    }


  def OnCompleteDone( self ) -> None:
    pass
