################################################################################
# Name        : mysql
# Description : A few utility functions for reading tables from mysql
# Version     : 0.0.0
# Created On  : 2019-01-10
# Modified On : 2020-06-29
# Author      : Hamid R. Darabi, Ph.D.
################################################################################

import os
import pymysql
import pandas as pd
from sqlalchemy import create_engine
from ds_lib.string_utils import StringUtilities


class MySQLUtil:

    def __init__(self, server=None, db=None, user=None, password=None, port='3306', verbose=None):
        if server:
            self.server = server
        else:
            try:
                self.server = os.environ.get('mysql_server')
            except KeyError:
                print("Please pass server or define 'mysql_server' in .env file.")
                raise

        if db:
            self.db = db
        else:
            try:
                self.db = os.environ.get('mysql_schema')
            except KeyError:
                print("Please pass server or define 'mysql_schema' in .env file.")
                raise

        if user:
            self.user = user
        else:
            try:
                self.user = os.environ.get('mysql_user')
            except KeyError:
                print("Please pass server or define 'mysql_user' in .env file.")
                raise

        if password:
            self.password = password
        else:
            try:
                self.password = os.environ.get('mysql_password')
            except KeyError:
                print("Please pass server or define 'mysql_password' in .env file.")
                raise

        self.port = port
        self.engine = None
        self.verbose = verbose

    def __enter__(self):
        conn_str = 'mysql://%s:%s/%s?user=%s&password=%s' % \
                   (self.server, self.port, self.db, self.user, self.password)
        pymysql.install_as_MySQLdb()
        self.engine = create_engine(conn_str)
        self.con = self.engine.connect()
        if self.verbose:
            print("Connected to database successfully.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()
        if self.verbose:
            print("Connection to mysql was closed.")

    def query(self, query_string, chunk_size=None):
        """
        Sends a query and gets the data as a pandas dataframe; can read data in chucks
        :param query_string: the string of the query to run
        :param mysql_engine: the mysql engine that is created with get_engine
        :param chunk_size: if the data is large to be read in one pass, chuck_size sets the number of records at each pass
        :return: a pandas dataframe or an iterator to it
        """
        if chunk_size:
            result = pd.read_sql(query_string, self.engine, chunksize=chunk_size)
        else:
            result = pd.read_sql(query_string, self.engine)
        return result

    def insert_df(self, df, table, chunk_size=None):
        """
        Inserts a dataframe to the mysql table
        :param df: the dataframe to insert to the table
        :param table: the table to write information to
        :param chunk_size: the size of each chuck to insert
        :return: results of inserting records in the database
        """
        if chunk_size:
            result = df.to_sql(table, con=self.engine, if_exists='append', chunksize=chunk_size, index=False)
        else:
            result = df.to_sql(table, con=self.engine, if_exists='append', index=False)
        return result

    def get_table_count(self, table_name):
        """
        Gets the number of records in a table
        :param table_name: name of the table
        :return: the number of records in the table
        """
        query_string = "SELECT count(*) FROM {0}".format(table_name)
        count = self.query(query_string)
        count_string = StringUtilities.get_formatted(count.iloc[0, 0])
        return "Number of records in {0} table is {1}.".format(table_name, count_string)

    def get_table_columns(self, table_name):
        """
        gets the number of columns in a table
        :param table_name: name of the table\
        :return: the number of columns in the table
        """
        query_string = "SHOW COLUMNS IN %s" % table_name
        columns = self.query(query_string)
        return columns

    def get_table(self, table_name):
        """
        reads all contents of the table in one pass
        :param table_name: name of the table
        :return: a pandas dataframe
        """
        query_string = "SELECT * FROM %s" % table_name
        table_data_frame = self.query(query_string, self.engine)
        return table_data_frame


if __name__ == "__main__":
    print("please import this script in my_shared_library")
