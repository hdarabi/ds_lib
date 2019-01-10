################################################################################
# Name        : mysql
# Description : A few utility functions for reading tables from mysql
# Version     : 0.0.0
# Created On  : 2019-01-10
# Modified On : 2019-01-10
# Author      : Hamid R. Darabi, Ph.D.
################################################################################

import os
import pandas as pd
from sqlalchemy import create_engine
import pymysql
import my_shared_library.string_utilities as su

def get_engine(server = os.environ.get('mysql_server'),
               db = os.environ.get('mysql_schema'),
               user = os.environ.get('mysql_user'),
               password = os.environ.get('mysql_password'),
               port = '3306'):
    """
    Establish a connection to the mysql database. Please don't forget to use engine.close() after running queries.
    :param server: name or ip address of the server
    :param db: default database to use
    :param user: username
    :param password: password
    :param port: MySQL database port. The default is 3306
    :return: the active engine to the database
    """
    # ToDo: Convert it to a context manager that closes connection after use.
    conn_str = 'mysql://%s:%s/%s?user=%s&password=%s' % \
                (server, port, db, user, password)
    pymysql.install_as_MySQLdb()
    engine = create_engine(conn_str)
    mysql_engine = engine.connect()
    return mysql_engine


def query(query_string, mysql_engine, chunk_size=None):
    """
    Sends a query and gets the data as a pandas dataframe; can read data in chucks
    :param query_string: the string of the query to run
    :param mysql_engine: the mysql engine that is created with get_engine
    :param chunk_size: if the data is large to be read in one pass, chuck_size sets the number of records at each pass
    :return: a pandas dataframe or an iterator to it
    """
    result = pd.read_sql(query_string, mysql_engine, chunksize=chunk_size)
    return result


def get_table_count(table_name, engine):
    """
    Gets the number of records in a table
    :param table_name: name of the table
    :param engine: the active engine to the MySQL database
    :return: the number of records in the table
    """
    query_string = "SELECT count(*) FROM %s.%s" % table_name
    count = query(query_string, engine)
    count_string = su.getFormatted(count.iloc[0, 0])
    print("Number of records in %s table is %s." % (table_name, count_string))


def get_table_columns(table_name, engine):
    """
    gets the number of columns in a table
    :param table_name: name of the table
    :param engine: active engine to the MySQL database
    :return: the number of columns in the table
    """
    query_string = "SHOW COLUMNS IN %s" % table_name
    columns = query(query_string, engine)
    print(columns)


def get_table(table_name, engine):
    """
    reads all contents of the table in one pass
    :param table_name: name of the table
    :param engine: the active MySQL engine
    :return: a pandas dataframe
    """
    query_string = "SELECT * FROM %s" % table_name
    table_data_frame = query(query_string, engine)
    return(table_data_frame)


if __name__ == "__main__":
    print("please import this script in my_shared_library")
