#*************************************************************************************************************
# Name        : snowflake
# Description : The main script to provide connection to SnowFlake
# Version     : 0.0.0
# Created On  : 2019-10-04
# Modified On : 2019-10-04
# Author      : Hamid R. Darabi, Ph.D.
#*************************************************************************************************************

import os
import numpy as np
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

load_dotenv()
ldap_pass = os.getenv('LDAP_PASS')

snowflake_user=os.getenv('SNOWFLAKE_USER')
snowflake_password=os.getenv('SNOWFLAKE_PASS')
snowflake_account=os.getenv('SNOWFLAKE_PASS')


class SnowFlake:
    def __init__(self, connection_parameters=None):
        if not connection_parameters:
            self.conn_param = {
                'account': snowflake_account,
                'user': snowflake_user,
                'pass': snowflake_password
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
        self.connection = snowflake.connector.connect(user=self.conn_param['user'],
            password=self.conn_param['pass'], account=self.conn_param['account'])
        self.cursor = self.connection.cursor()

    def execute(self, query, chunksize=None):
        result = pd.read_sql(query, self.connection, chunksize=chunksize)
        return result

    def execute_no_value(self, query):
        self.cursor.execute(query)

    def close(self):
        self.cursor.close()
        self.connection.close()
