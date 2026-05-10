"""
Settings module for ArsForte.
Automatically loads dev or prod settings based on ENV_TYPE environment variable.
"""

import os
from decouple import config

ENV_TYPE = config('ENV_TYPE', default='dev')

if ENV_TYPE == 'prod':
    from .prod import *
else:
    from .dev import *