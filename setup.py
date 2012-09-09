# setup.py

import py2exe
from distutils.core import setup

py2exe_options = {
   "compressed": 1,
   "optimize": 2,
   "bundle_files": 1,
   "includes" : ["sip", "PyQt4", "PyQt4.QtCore"]
}

setup(
   options={"py2exe" : py2exe_options},
   windows=[{"script" : "DXAFSDataConverter.py"}],
)