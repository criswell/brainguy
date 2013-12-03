#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   Fix Series nfo lookup files
"""

from __future__ import print_function

try:
    import ConfigParser as configparser
except ImportError:
    import configparser

import os.path, sys, os, argparse

import imdb

parser = argparse.ArgumentParser(
    description = 'Fixes series nfo lookup files.')
parser.add_argument('paths', nargs='+',
    help='Path or paths to directories to process.')

args = parser.parse_args()

supported_types = [
    'series',
    'movie'
]

def process_series(root, files):
    root_id = None
    if config.has_option('hint', 'root_id'):
        root_id = config.get('hint', 'root_id')

    print("-= Connecting to IMDb")

    i = imdb.IMDb()
    m = i.get_movie(root_id)

    episodes = dict()
    titles = []

    print("-= Updating all episodes...")
    i.update(m, 'episodes')

    import pdb; pdb.set_trace()

    for season in m['episodes']:
        for e in m['episodes'][season]:
            episodes[e['title']] = e
            titles.append(e['title'].lower())


for p in args.paths:
    for root, dirs, files in os.walk(p):
        print('> Processing "%s"' % root)
        if '.hint' in files:
            config = configparser.SafeConfigParser()
            config.readfp(open(os.path.abspath('%s/.hint' % root)))
            show_type = 'series'
            if config.has_option('hint', 'type'):
                show_type = config.get('hint', 'type')
            if show_type not in supported_types:
                print('> Error in config, unknown type "%s"' % show_type)
                show_type = supported_types[0]
                print('>-- Using type "%s"' % show_type)

            if show_type == 'series':
                process_series(root, files)


#mst3k_path = sys.argv[1]

#print("-= Getting list of files from '%s'" % mst3k_path)

#for root, dirs, files in os.walk(mst3k_path):
#    foo
