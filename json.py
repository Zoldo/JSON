# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 17:12:56 2017

@author: weilnboeck
"""

import json

with open('jfile.json', 'r') as file:
    array = json.load(file)

for entry in array['Aktien']:
    print('-----------------------------')
    print(entry)