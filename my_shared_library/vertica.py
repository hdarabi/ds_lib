# Name        : vertica
# Description : The main script to provide connection to Vertica
# Version     : 0.0.0
# Created On  : 2019-05-10
# Modified On : 2019-05-10
# Author      : Hamid R. Darabi, Ph.D.

import os
import numpy as np
import pandas as pd
import vertica_python
from dotenv import load_dotenv

load_dotenv()
ldap_pass = os.getenv('LDAP_PASS')

CPM_TO_DOLLAR = 1000.
SECONDS_IN_A_MINUTE = 60
NANO_SECOND_TO_SECOND = 1000000000


class Vertica:
    def __init__(self, connection_parameters=None):
        if not connection_parameters:
            self.conn_param = {
                'host': 'srv-01-41-b06.iad1.trmr.io',
                 'port': 5433,
                 'user': 'hdarabi',
                 'password': ldap_pass,
                 'database': 'tremordb',
                 'session_label': 'some_label',
                 'read_timeout': 6000,
                 'unicode_error': 'strict',
                 'ssl': False,
                 'use_prepared_statements': False,
                 'connection_timeout': 3000
            }
        else:
            self.conn_param = connection_parameters

    def __enter__(self, connection_parameters=None):
        self.__init__(connection_parameters)
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        self.connection = vertica_python.connect(**self.conn_param)
        self.cursor = self.connection.cursor()

    def execute(self, query):
        result = pd.read_sql(query, self.connection)
        return result

    def close(self):
        self.connection.close()

    def add_n_min_bucket_index(self, data, time_col, bucket_time_col, bucket_size_in_min):
        """
        Generates time indexes of n-minutes size and adds an index for it. IMPORTANT NOTE: the
        start time and first time found in the data should be aligned to match the indices.
        """
        # TODO: use pd.to_datetime(data['bucket'].astype(np.int64)) for plotting

        ns5min = bucket_size_in_min * SECONDS_IN_A_MINUTE * NANO_SECOND_TO_SECOND
        data[bucket_time_col] = pd.to_datetime(((data[time_col].astype(np.int64) // ns5min) * ns5min))
        start = pd.to_datetime(((min(data[time_col].astype(np.int64)) // ns5min) * ns5min))
        end = pd.to_datetime((((max(data[time_col].astype(np.int64)) + 1) // ns5min) * ns5min))
        five_min_index = pd.date_range(start=start, end=end, freq='%dmin' % bucket_size_in_min)
        empty = pd.DataFrame({bucket_time_col: five_min_index}).reset_index()
        data_with_index = data.merge(empty, how='outer', on=bucket_time_col)
        data_with_index = data_with_index[data_with_index[time_col].notnull()]
        return data_with_index

    def cpm_to_dollar(self, data, input_col, output_col):
        data[output_col] = data[input_col] * CPM_TO_DOLLAR
        return data
