################################################################################
# Name        : test_mysql
# Description : The formal unit tests for the mysql wrapper.
# Version     : 0.0.0
# Created On  : 2019-02-01
# Modified On : 2019-02-12
# Author      : Hamid R. Darabi, Ph.D.
################################################################################

import unittest
from my_shared_library.mysql import MySQLUtil
from mock import Mock, patch


class TestMySQL(unittest.TestCase):
    def setUp(self):
        self.data = {
            'id': [1, 2, 3],
            'name': ['A', 'B', 'C']
        }

    def tearDown(self):
        self.data = None

    def test_get_table_count(self):
        with MySQLUtil(server='***',
                       db='***', user='***', password='***') as db:
            result = db.get_table_count('***')
            print(result)

    def test_get_table_columns(self):
        with MySQLUtil(server='***',
                       db='***', user='***', password='***') as db:
            result = db.get_table_columns('***')
            print(result)
