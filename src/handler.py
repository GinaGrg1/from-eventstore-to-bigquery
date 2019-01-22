#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 16:54:44 2017

@author: rgurung
"""
import logging
import json
from makeEventTransform import get_transformer_for

class EventHandler:
    def __init__(self, writer, supported_event_types):
        self._supported_event_types = supported_event_types
        self._writer = writer

    def handle_event(self, event):
        if event.type in self._supported_event_types and event.data:
            transform = get_transformer_for(event.type)
            try:
                data = json.loads(event.data)
                data['eventstore_timestamp'] = event.created
                event_data_out = transform(data)
                self._writer.write(event.type, [event_data_out])
            except json.decoder.JSONDecodeError as e:
                logging.exception(
                    'Event number:{}, Event type:{} data:{}'.format(
                        event.event_number,
                        event.type,
                        event.data
                    ),
                    exc_info=True
                )
