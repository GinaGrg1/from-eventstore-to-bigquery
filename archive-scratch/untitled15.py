#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 15:41:42 2018

@author: rgurung
"""

new_data = {}
for key, value in etd_test_data.items():
    if key == 'delivery_schedule':
        if 'eta' in  next(iter(value.values())).keys():
            new_data['eta_date'] = next(iter(value.values())).get('eta')
        if 'etd' in next(iter(value.values())).keys():
            new_data['etd_date'] = next(iter(value.values())).get('etd')
        new_data['delivery_type'] = next(iter(value.keys())).split('_')[0]
    else:
        new_data[key] = value
