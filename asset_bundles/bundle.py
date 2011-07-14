# -*- coding: utf-8 -*-

import os
import hashlib
import subprocess

from django.conf import settings
from django.contrib import staticfiles


YUI_COMPRESSOR_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "yuicompressor-2.4.6.jar")


class Bundle(object):
    
    def __init__(self, type_, files, output, respect_debug=True):
        self.type = type_
        self.files = files
        self.output = output
        self.respect_debug = respect_debug
    
    @property
    def urls(self):
        if self.respect_debug and settings.DEBUG:
            for file_ in self.files:
                yield file_
        else:
            self.compress()
            yield self.filename

    def merge_data(self):
        self.data = ""
        for file_ in self.files:
            path = staticfiles.finders.find(file_)
            with open(path) as fp:
                self.data += fp.read()
        self.hash = hashlib.md5(self.data).hexdigest()
    
    def compress(self):
        self.merge_data()
        self.filename = "%s.%s.%s" % (self.output, self.hash, self.type)
        path = os.path.join(settings.STATIC_ROOT, self.filename)
        if os.path.isfile(path):
            return
        if not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        proc = subprocess.Popen(["java", "-jar", YUI_COMPRESSOR_PATH,
                                 "--type", self.type],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        proc.stdin.write(self.data)
        proc.stdin.close()
        with open(path, "w") as fp:
            fp.write(proc.stdout.read())
