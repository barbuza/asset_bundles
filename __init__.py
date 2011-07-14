# -*- coding: utf-8 -*-

import os

from django.conf import settings
from django.contrib.staticfiles.finders import BaseFinder


class BundleFinder(BaseFinder):
    
    def __init__(self, apps=None, *args, **kwargs):
        pass
    
    def find(self, path, all=False):
        fullpath = os.path.join(settings.STATIC_ROOT, path)
        if os.path.isfile(fullpath):
            if not all:
                return fullpath
            return [fullpath]
        return []
    
    def list(self, ignore_patterns):
        return []
