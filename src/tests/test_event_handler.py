#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 17:53:07 2017

@author: rgurung
"""
import pytest

from photonpump import messages

from handler import EventHandler


class FakeBigQueryWriter:

    def __init__(self):
        self.data = []

    def write(self, event_type, data):
        self.data.append(event_type)


class TestEventHandler():
    examples = [
        ('sale_order', ['sale_order']),
        ('purchase_order', ['purchase_order']),
        ('purchase_o', []),
        ('sale_o', []),
    ]


    @pytest.mark.parametrize('event, expected', examples)
    def test_handle_event(self, event, expected):
        writer = FakeBigQueryWriter()
        event_types = ['sale_order', 'purchase_order']
        write_events = EventHandler(writer, event_types)

        event = messages.photonpump_eventrecord(
            'somestream', 'id', 'event_number', event, {}, 'metadata', 'created'
        )

        write_events.handle_event(event)
        assert writer.data == ['sale_order']
