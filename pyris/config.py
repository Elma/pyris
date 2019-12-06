# coding: utf-8

"""Pyris configuration

Retrieve user and password from the YAML configuration file for the database
access
"""

import os
import io

from yaml import load as yload, FullLoader


_cfgfile = os.environ.get('PYRIS_APP_SETTINGS')

if _cfgfile is not None:
    with io.open(_cfgfile, 'r') as fobj:
        DATABASE = yload(fobj.read(), Loader=FullLoader).get('database', {})
else:
    DATABASE = {"USER": os.environ["USER"],
                "HOST": "localhost"}
