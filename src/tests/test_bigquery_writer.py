#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 09:49:31 2017

@author: rgurung
"""

from bigquery_writer import BigQueryWriter
import unittest
from unittest.mock import Mock, call


class TestBigQueryWriter(unittest.TestCase):
    def test_whether_events_are_written_agains_correct_table(self):
        
        # Init expects non-empty array for supported events
        with self.assertRaises(ValueError) as context:
            writer = BigQueryWriter('test_dataset', [])

        self.assertTrue('Non empty array expected' in str(context.exception))

        # Tables added to the schemas dict
        writer = BigQueryWriter('test_dataset', ['event_a', 'event_b'])

        # Mock functions that connect to BigQuery
        writer.get_client = Mock()
        writer.add_dataset = Mock()
        writer.add_table = Mock()

        writer.begin()

        writer.get_client.assert_called_once()
        writer.add_dataset.assert_called_with('test_dataset')
        calls = [call('event_a'), call('event_b')]
        writer.add_table.assert_has_calls(calls)
        self.assertEqual(writer.add_table.call_count, 2)


if __name__ == "__main__":
    unittest.main()
