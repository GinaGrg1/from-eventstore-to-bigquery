#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 12:36:07 2018

@author: rgurung
"""
import json
import pprint 

sample = {
  "purchase_order_id": "17IDL049-FR",
  "delivery_schedule": {
    "fob_dates": {
      "eta": "2018-04-17",
      "etd": "2018-03-21"
    }
  }
}

delivery_list = ['cif','dap','ddp','exw','fob']


def json_flatten(json_data):
    new_data ={}
    #data = json.load(json_data)
    
    for key,value in data.items():
        if key.startswith('delivery'):
            for k, v in value.items():
                for i in delivery_list:
                    if k.startswith(i):
                        if 'eta' in v:
                            new_data['eta_date'] = v['eta']
                        else:
                            new_data['eta_date'] = 'None'
                        if 'etd' in v:
                            new_data['etd_date'] = v['etd']
                        else:
                            new_data['etd_date'] = 'None'
                                             
                        new_data['delivery_type'] = i
        else:
            new_data[key] = value
    return new_data

data = json.load(open("./tests/files/sample_etd_eta_changed.json","rb"))
pprint.pprint(json_flatten(data))


with open("./src/tests/files/sample_etd_eta_changed.json") as json_data:
    pprint.pprint(json_flatten(json_data))

