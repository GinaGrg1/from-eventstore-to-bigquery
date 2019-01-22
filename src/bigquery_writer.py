#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 09:49:31 2017

@author: rgurung
"""
import os
import logging

from google.cloud import bigquery


class BigQueryWriter:
    def __init__(self, dataset_id, tables):
        if len(tables) == 0:
            raise ValueError('Non empty array expected in tables parameter.')

        self.schemas = dict()
        self.tables = tables
        self.dataset_id = dataset_id

    def begin(self):
        self.get_client()
        self.add_dataset(self.dataset_id)

        for table in self.tables:
            if table not in self.schemas:
                self.add_table(table)

    def write(self, table, data):
        try:
            error_response = self.bigquery_client.create_rows(self.schemas[table], data)
            if error_response == []:
                logging.info('Loaded 1 row into %s:%s', self.dataset_id, table)
            else:
                for error in error_response.errors:
                    log.errror(' - ' + error)
                    log.errror(' - ' + data)

        except Exception:
            logging.exception(
                'BigQuery Exception',
                exc_info=True
            )

    def add_table(self, table):
        table_ref = self.dataset_ref.table(table)
        self.schemas[table] = self.bigquery_client.get_table(table_ref)

    def add_dataset(self, dataset_id):
        self.dataset_ref = self.bigquery_client.dataset(dataset_id)

    def get_client(self):
        self.bigquery_client = bigquery.Client.from_service_account_json(os.environ.get('BIGQUERY_ACCESS_TOKEN_PATH'))
