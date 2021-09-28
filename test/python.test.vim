function! Test_Run_BasePy()
  py3 << EOF
import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, '../python')
sys.path.insert(0, '../third_party/ycmd')
import ycm
import ycmd
test_suite = unittest.defaultTestLoader.discover(
  start_dir = 'ycm.tests',
  pattern = 'base_test.py',
  top_level_dir = '..' )
output = StringIO()
runner = unittest.TextTestRunner( output, False, 0, False, True )
result = runner.run(test_suite)
if not result.wasSuccessful():
  output.seek(0)
  print(output.read())
EOF
endfunction


function! Test_Run_CommandPy()
  py3 << EOF
import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, '../python')
sys.path.insert(0, '../third_party/ycmd')
import ycm
import ycmd
test_suite = unittest.defaultTestLoader.discover(
  start_dir = 'ycm.tests',
  pattern = 'command_test.py',
  top_level_dir = '..' )
output = StringIO()
runner = unittest.TextTestRunner( output, False, 0, False, True )
result = runner.run(test_suite)
if not result.wasSuccessful():
  output.seek(0)
  print(output.read())
EOF
endfunction


function! Test_Run_CompletionPy()
  py3 << EOF
import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, '../python')
sys.path.insert(0, '../third_party/ycmd')
import ycm
import ycmd
test_suite = unittest.defaultTestLoader.discover(
  start_dir = 'ycm.tests',
  pattern = 'completion_test.py',
  top_level_dir = '..' )
output = StringIO()
runner = unittest.TextTestRunner( output, False, 0, False, True )
result = runner.run(test_suite)
if not result.wasSuccessful():
  output.seek(0)
  print(output.read())
EOF
endfunction


function! Test_Run_DiagnosticFilterPy()
  py3 << EOF
import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, '../python')
sys.path.insert(0, '../third_party/ycmd')
import ycm
import ycmd
test_suite = unittest.defaultTestLoader.discover(
  start_dir = 'ycm.tests',
  pattern = 'diagnostic_filter_test.py',
  top_level_dir = '..' )
output = StringIO()
runner = unittest.TextTestRunner( output, False, 0, False, True )
result = runner.run(test_suite)
if not result.wasSuccessful():
  output.seek(0)
  print(output.read())
EOF
endfunction


function! Test_Run_EventNotificationPy()
  py3 << EOF
import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, '../python')
sys.path.insert(0, '../third_party/ycmd')
import ycm
import ycmd
test_suite = unittest.defaultTestLoader.discover(
  start_dir = 'ycm.tests',
  pattern = 'event_notification_test.py',
  top_level_dir = '..' )
output = StringIO()
runner = unittest.TextTestRunner( output, False, 0, False, True )
result = runner.run(test_suite)
if not result.wasSuccessful():
  output.seek(0)
  print(output.read())
EOF
endfunction
function! Test_Run_OmniCompleterPy()
  py3 << EOF
import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, '../python')
sys.path.insert(0, '../third_party/ycmd')
import ycm
import ycmd
test_suite = unittest.defaultTestLoader.discover(
  start_dir = 'ycm.tests',
  pattern = 'omni_completer_test.py',
  top_level_dir = '..' )
output = StringIO()
runner = unittest.TextTestRunner( output, False, 0, False, True )
result = runner.run(test_suite)
if not result.wasSuccessful():
  output.seek(0)
  print(output.read())
EOF
endfunction


function! Test_Run_PathsPy()
  py3 << EOF
import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, '../python')
sys.path.insert(0, '../third_party/ycmd')
import ycm
import ycmd
test_suite = unittest.defaultTestLoader.discover(
  start_dir = 'ycm.tests',
  pattern = 'paths_test.py',
  top_level_dir = '..' )
output = StringIO()
runner = unittest.TextTestRunner( output, False, 0, False, True )
result = runner.run(test_suite)
if not result.wasSuccessful():
  output.seek(0)
  print(output.read())
EOF
endfunction


function! Test_Run_PostCompletePy()
  py3 << EOF
import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, '../python')
sys.path.insert(0, '../third_party/ycmd')
import ycm
import ycmd
test_suite = unittest.defaultTestLoader.discover(
  start_dir = 'ycm.tests',
  pattern = 'postcomplete_test.py',
  top_level_dir = '..' )
output = StringIO()
runner = unittest.TextTestRunner( output, False, 0, False, True )
result = runner.run(test_suite)
if not result.wasSuccessful():
  output.seek(0)
  print(output.read())
EOF
endfunction


function! Test_Run_SignatureHelpPy()
  py3 << EOF
import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, '../python')
sys.path.insert(0, '../third_party/ycmd')
import ycm
import ycmd
test_suite = unittest.defaultTestLoader.discover(
  start_dir = 'ycm.tests',
  pattern = 'signature_help_test.py',
  top_level_dir = '..' )
output = StringIO()
runner = unittest.TextTestRunner( output, False, 0, False, True )
result = runner.run(test_suite)
if not result.wasSuccessful():
  output.seek(0)
  print(output.read())
EOF
endfunction


function! Test_Run_SyntaxParsePy()
  py3 << EOF
import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, '../python')
sys.path.insert(0, '../third_party/ycmd')
import ycm
import ycmd
test_suite = unittest.defaultTestLoader.discover(
  start_dir = 'ycm.tests',
  pattern = 'syntax_parse_test.py',
  top_level_dir = '..' )
output = StringIO()
runner = unittest.TextTestRunner( output, False, 0, False, True )
result = runner.run(test_suite)
if not result.wasSuccessful():
  output.seek(0)
  print(output.read())
EOF
endfunction


function! Test_Run_VimsupportPy()
  py3 << EOF
import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, '../python')
sys.path.insert(0, '../third_party/ycmd')
import ycm
import ycmd
test_suite = unittest.defaultTestLoader.discover(
  start_dir = 'ycm.tests',
  pattern = 'vimsupport_test.py',
  top_level_dir = '..' )
output = StringIO()
runner = unittest.TextTestRunner( output, False, 0, False, True )
result = runner.run(test_suite)
if not result.wasSuccessful():
  output.seek(0)
  print(output.read())
EOF
endfunction


function! Test_Run_YouCompleteMePy()
  py3 << EOF
import unittest
import sys
import os
from io import StringIO
sys.path.insert(0, '../python')
sys.path.insert(0, '../third_party/ycmd')
import ycm
import ycmd
test_suite = unittest.defaultTestLoader.discover(
  start_dir = 'ycm.tests',
  pattern = 'youcompleteme_test.py',
  top_level_dir = '..' )
output = StringIO()
runner = unittest.TextTestRunner( output, False, 0, False, True )
result = runner.run(test_suite)
if not result.wasSuccessful():
  output.seek(0)
  print(output.read())
EOF
endfunction
