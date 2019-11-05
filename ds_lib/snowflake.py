#*************************************************************************************************************
# Name        : snowflake
# Description : The main script to provide connection to SnowFlake
# Version     : 0.0.0
# Created On  : 2019-10-04
# Modified On : 2019-11-05
# Author      : Hamid R. Darabi, Ph.D.
#*************************************************************************************************************

import os
import numpy as np
import pandas as pd
import snowflake.connector

class SnowFlake:
    def __init__(self, connection_parameters=None, verbose=False):
        if not connection_parameters:
            self.conn_param = {
                'account': os.getenv('SNOWFLAKE_ACCOUNT'),
                'user': os.getenv('SNOWFLAKE_USER'),
                'pass': os.getenv('SNOWFLAKE_PASS')
            }
            if verbose:
                print("Data set from os, account: {}, user: {}, pass: {}".format(os.getenv(
                    'SNOWFLAKE_ACCOUNT'), os.getenv('SNOWFLAKE_USER'), '*' * len(os.getenv('SNOWFLAKE_PASS'))))
        else:
            self.conn_param = connection_parameters
            if verbose:
                print("Data set from os, account: {}, user: {}, pass: {}".format(connection_parameters[
                    'SNOWFLAKE_ACCOUNT'], connection_parameters['SNOWFLAKE_USER'], '*' * len(
                    connection_parameters['SNOWFLAKE_PASS'])))
        self.verbose = verbose

    def __enter__(self, connection_parameters=None):
        self.__init__(connection_parameters)
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        self.connection = snowflake.connector.connect(user=self.conn_param['user'],
            password=self.conn_param['pass'], account=self.conn_param['account'])
        self.cursor = self.connection.cursor()

    def execute(self, query, chunksize=None):
        result = pd.read_sql(query, self.connection, chunksize=chunksize)
        if self.verbose:
            print("The shape of the input data is".format(result.shape))
        return result

    def execute_no_value(self, query):
        self.cursor.execute(query)

    def close(self):
        self.cursor.close()
        self.connection.close()
