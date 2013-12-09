# -*- coding: utf-8 -*-

from __future__ import print_function

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

import os.path
import os
import time
from traceback import print_exp

class Config(object):

    def __init__(self, home_directory=os.path.expanduser("~")):
        self._home_directory = home_directory
        self._config_file = '%s/.brainguy'
        self.C = configparser.SafeConfigParser()
        self._load_config()

    def _load_config(self):
        if os.path.isfile(self._config_file):
            try:
                cf = open(self._config_file)
            except:
                print_exp()
                print("Error opening '%s' config file, backing up and creating new..." % self._config_file)
                self._backup_config()
                self._create_config()
            else:
                with cf:
                    self.C.readftp(cf)
        else:
            self._create_config()

    def _backup_config(self):
        backup_config = "%s.backup-%i" % (self._configFile % int(time.time()))
        os.rename(self._configFile, backup_config)

    def _create_config(self):
        if not self.C.has_section('main'):
            self.C.add_section('main')

        if not self.C.has_section('output'):
            self.C.add_section('output')

        # Our default is to enabled ERROR and above
        self.C.set('main', 'log_level', '3')
        self.C.set('main', 'log_file', None)

        # Yay, these are my defaults, motherfucker!
        self.C.set('main', 'scratch_vob', '/scratch2/temp_vob')
        self.C.set('output', 'dest_dir', '/mnt/video/Incoming')
