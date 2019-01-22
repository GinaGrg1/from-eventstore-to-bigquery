#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 11:00:51 2017
@author: rgurung
"""

"""
Usage:
EVENTSTORE_STREAM=<name> python reader.py
optional env vars:
EVENTSTORE_SUBSCRIPTION: subscription name
EVENTSTORE_BASEURL: Base url
"""

import json
import pprint as pp
import time
import requests


def default_handle(event_type, data):
    # Default handler, only prints the messages to the screen
    pp.pprint(event_type, data)


class Reader:

    def __init__(self, base_url, stream, subscription_name, count,handler=None):
        self._base_url = base_url
        self._stream = stream
        self._subscription_name = subscription_name
        self._count = count
        if handler is None:
            handler = default_handle
        self._handler = handler

    def start(self, continous=True):
        self._create_subscription()
        while True:
            links, event_list = self._read_from_subscription()
            if len(event_list) == 0:
                # No response means, we read all of them
                if continous:
                    # We can try again a bit later
                    time.sleep(1)
                    continue
                else:
                    # We can stop after the catch-up
                    return

            success = links['ackAll']
            failed = links['nackAll']

            try:
                self._handler(event_list)
                status = success
            except:
                print('Failed to process {} events from {}'.format(self._count, self._subscription_name))
                status = failed

            try:
                self._response(status)
            except:
                print('Failed to acknowldege {} events'' status from {}'.format(self._count, self._subscription_name))
                raise

    def _create_subscription(self):
        url = '{base_url}/subscriptions/{stream}/{subscription_name}'.format(
            base_url=self._base_url,
            stream=self._stream,
            subscription_name=self._subscription_name
        )
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.put(
            url, headers=headers, auth=('admin', 'changeit'),
            json={"ResolveLinkTos": True}
        )
        assert response.status_code in (201, 409), 'Unexpected status'

    def _read_from_subscription(self):
        url = '{base_url}/subscriptions/{stream}/{subscription_name}/{count}?embed=body'.format(
            base_url=self._base_url,
            stream=self._stream,
            subscription_name=self._subscription_name,
            count=self._count
        )

        response = requests.get(
            url,
            headers={
                'Accept': 'application/vnd.eventstore.competingatom+json'
            }
        )
        assert response.status_code == 200

        entries = response.json()['entries']
        
        event_list = []
               
        for event in entries:
            if event['data']:
                type = event['eventType']
                data = json.loads(event['data'])
                data['eventstore_timestamp'] = event['updated']
                event_list.append([type, data])
            else:
                print("The data is empty.")
                                 
                
        links = response.json()['links']
        links_dict = {}
        for link in links:
            links_dict[link['relation']] = link['uri']

        return (links_dict, event_list)

    def _response(self, uri):
        res = requests.post(uri, headers={'Content-Type': 'application/json'})
        assert res.status_code == 202, (res.status_code, res.text)