#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 12:33:02 2018

@author: rgurung
"""
import json

delivery_list = ['cif','dap','ddp','exw','fob']

supported_event_types = "quantity_moved_in_to_new_po,etd_eta_changed,purchase_order_approved"
event_types = supported_event_types.split(",")


for event_type, event_data in event_list:
    if event_type in supported_event_types:
        print('EVENT TYPE IS : ', event_type)
       
        transform = MakeEventTransform(event_type)
        print('test')
        print(event_data)
        event_data_out = transform_etd_eta_changed(event_data)
        #self._writer.write(event_type, [event_data_out])
    #else:
       # self.writer.write(event_type, event_data)
    #else:
        # print('enter correct event')
       

def MakeEventTransform(event_type):

        if event_type in supported_event_types:
            print('its there')
            return transform_etd_eta_changed(data)
        #if event_type == 'purchase_order_approved':
        #    return transform_purchase_order_approved ()
        #if event_type == 'quantity_moved_in_to_new_po':
        #    return transform_quantity_moved_in_to_new_po ()
        
        #fun = search.functions("transform_", event_type)
        else:
            return transform_none



def transform_etd_eta_changed(data):    
    new_data = {}
    for key,value in data.items():
        print(key)
        if key.startswith('delivery'):
            for k, v in value.items():
                for i in delivery_list:
                    if k.startswith(i):
                        if 'eta' in v:
                            new_data['eta_date'] = v['eta']
                        else:
                            new_data['eta_date'] = None
                        if 'etd' in v:
                            new_data['etd_date'] = v['etd']
                        else:
                            new_data['etd_date'] = None
                                             
                        new_data['delivery_type'] = i
        else:
            new_data[key] = value
    return new_data


#def transform_purchase_order_approved(event):
    
#    return

#def transform_quantity_moved_in_to_new_po(event):

#    return

def transform_none(event) :
    return event


 
class transform(MakeEventTransform):
    
    def json_flatten(event_data):
        # write logic to flatten json here.
        
        new_data ={}
        
        data = json.load(event_data)
    
        for key,value in data.items():
            if key.startswith('delivery'):
                for k, v in value.items():
                    for i in delivery_list:
                        if k.startswith(i):
                            new_data['etd_date'] = v['eta']
                            new_data['eta_date'] = v['etd']
                            new_data['delivery_type'] = i
            else:
                new_data[key] = value
        return new_data

    
    
    












   
        