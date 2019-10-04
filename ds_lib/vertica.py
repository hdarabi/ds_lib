#*************************************************************************************************************
# Name        : vertica
# Description : The main script to provide connection to Vertica
# Version     : 0.0.0
# Created On  : 2019-05-10
# Modified On : 2019-10-04
# Author      : Hamid R. Darabi, Ph.D.
#*************************************************************************************************************

import os
import numpy as np
import pandas as pd
import vertica_python
from dotenv import load_dotenv

load_dotenv()
vertica_host = os.getenv('VERTICA_HOST')
vertica_user = os.getenv('VERTICA_USER')
vertica_pass = os.getenv('VERTICA_PASS')
vertica_db = os.getenv('VERTICA_DB')

class Vertica:
    def __init__(self, connection_parameters=None, verbose=False):
        if not connection_parameters:
            self.conn_param = {
                'host': vertica_host,
                 'port': 5433,
                 'user': vertica_user,
                 'password': vertica_pass,
                 'database': vertica_db,
                 'session_label': 'my_session_label',
                 'read_timeout': 6000,
                 'unicode_error': 'strict',
                 'ssl': False,
                 'use_prepared_statements': False,
                 'connection_timeout': 3000
            }
        else:
            self.conn_param = connection_parameters
        self.verbose = verbose

    def __enter__(self, connection_parameters=None):
        self.__init__(connection_parameters)
        self.connect()
        if self.verbose:
            print(connection_parameters)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        self.connection = vertica_python.connect(**self.conn_param)
        self.cursor = self.connection.cursor()

    def execute(self, query, chunksize=None):
        result = pd.read_sql(query, self.connection, chunksize=chunksize)
        return result

    def execute_no_value(self, query):
        self.cursor.execute(query)

    def close(self):
        self.connection.close()
