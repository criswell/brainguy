#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   Fix MST3k nfo lookup files
"""

import os.path

import imdb

mst3k_id = '0094517'

print "-= Connecting to IMDb"

i = imdb.IMDb()
m = i.get_movie(mst3k_id)

episodes = dict()
lookup = []

print "-= Updating all episodes..."
i.update(m, 'episodes')

for season in m['episodes']:
    for e in season:
        i = 1
