#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   Fix MST3k nfo lookup files
"""

from __future__ import print_function

import os.path, sys, os

import imdb

if len(sys.argv) < 2:
    print "-= Need to specify the path to MST3k root folder"
    sys.exit(1)

mst3k_id = '0094517'

print("-= Connecting to IMDb")

i = imdb.IMDb()
m = i.get_movie(mst3k_id)

episodes = dict()
titles = []

print("-= Updating all episodes...")
i.update(m, 'episodes')

for season in m['episodes']:
    for e in season:
        episodes[e['title']] = e
        titles.append(e['title'].lower())

mst3k_path = sys.argv[1]

print("-= Getting list of files from '%s'" % mst3k_path)

for root, dirs, files in os.walk(mst3k_path):
    foo
