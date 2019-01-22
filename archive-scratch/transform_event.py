#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 12:33:02 2018

@author: rgurung
"""
import json
import pickle
from  makeEventTranform import MakeEventTransform
#from makeEventTranform import transform_etd_eta_changed

#from makeEventTransformFactory import MakeEventTransform


import os
print(os.getcwd())

event_list = pickle.load(open("clean_list.p","rb"))

delivery_list = ['cif', 'dap', 'ddp', 'exw', 'fob']

supported_event_types = "quantity_moved_in_to_new_po,etd_eta_changed,purchase_order_approved"
event_types = supported_event_types.split(",")

for event_type, event_data in event_list:
    if event_type in supported_event_types:
        print('EVENT TYPE IS : ', event_type)
        # transform_etd_eta_changed.makeTransform()
        transform = MakeEventTransform(event_type, event_data)
        print('test')
        print(event_data)
        event_data_out = transformEventData(event_data)
        # self._writer.write(event_type, [event_data_out])
        # else:
        # self.writer.write(event_type, event_data)
        # else:
        # print('enter correct event')
print("************finally*************")
print(event_data_out)














