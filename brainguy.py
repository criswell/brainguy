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

import os.path, sys, os, argparse, re

import imdb
from pytvdbapi import api

parser = argparse.ArgumentParser(
    description = 'Fixes series nfo lookup files.')
parser.add_argument('paths', nargs='+',
    help='Path or paths to directories to process.')

args = parser.parse_args()

supported_types = [
    'series',
    'movie'
]

global_config = None
try:
    global_config = configparser.SafeConfigParser()
    global_config.readfp('%s/.brainguy' % os.path.expanduser("~"))
    tvdb_api = None
    if global_config.has_option('global', 'api_key'):
        tvdb_api = global_config.get('global', 'api_key')
except:
    print('-= Problem parsing ~/.brainguy, no global settings used')

def get_info_from_file(f):
    result = re.findall(r"(?:s|season)(\d{2})(?:e|x|episode|\n)(\d{2})", f, re.I)
    season = None
    episode = None
    if len(result) > 0:
        season = int(result[0][0])
        episode = int(result[0][1])
    return (season, episode)

def process_series(root, files):
    root_id = None
    if config.has_option('hint', 'root_id'):
        root_id = config.get('hint', 'root_id')

    service = 'imdb'
    if config.has_option('hint', 'service'):
        service = config.get('hint', 'service')

    if service == 'imdb':
        process_series_imdb(root_id, root, files)
    elif service == 'tvdb':
        process_series_tvdb(root_id, root. files)
    else:
        print('-= ERROR! Service id "%s" unknown, skipping' % service)

def write_nfo_file(root, f, url):
    file_pre = ''.join(f.split('.')[:-1])
    nfo_fname = '%s/%s.nfo' % (root, file_pre)
    print('>--- Writing "%s"' % nfo_fname)
    with open(nfo_fname, 'wb') as outfile:
        outfile.write('%s\n' % url)

def process_series_tvdb(root_id, root, files):
    print('-= Connecting to the TVDB')
    db = api.TVDB(tvdb_api)
    series = db.get_series(root_id, 'en')
    if len(series) > 0:
        for f in files:
            (season, episode) = get_info_from_file(f)
            if episode is not None:
                try:
                    e = series[season][episode]
                    url = 'http://www.thetvdb.com/?tab=episode&seriesid=%d&seasonid=%d&id=%d' % (
                        root_id, e.seasonid, e.id)
                    write_nfo_file(root, f, url)
                except:
                    print('-= ERROR! Processing s%de%d' % (season, episode))
    else:
        print('-= ERROR! Could not find series "%s"' % root_id)

def process_series_imdb(root_id, root, files):
    print("-= Connecting to IMDb")

    i = imdb.IMDb()
    m = i.get_movie(root_id)

    print("-= Updating all episodes...")
    i.update(m, 'episodes')

    for f in files:
        (season, episode) = get_info_from_file(f)
        if episode is not None:
            try:
                e = m['episodes'][season][episode]
                url = 'http://www.imdb.com/title/tt%s/' % e.movieID
                write_nfo_file(root, f, url)
            except:
                print('>--- ERROR processing s"%d" e"%d"' % (season, episode))

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
