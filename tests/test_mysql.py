################################################################################
# Name        : test_mysql
# Description : A handy test to examine correct performance of mysql code
# IMPORTANT: Please note this is not using patch and you need to create the
# empty dummy mysql table.
# Version     : 0.0.0
# Created On  : 2020-06-29
# Modified On : 2020-06-29
# Author      : Hamid R. Darabi, Ph.D.
################################################################################

import unittest
import pandas as pd
from ds_lib.mysql import MySQLUtil
from pandas.util.testing import assert_frame_equal


SERVER = None
DB = None
USER = None
PASSWORD = None


class TestMySQLUtil(unittest.TestCase):
    def setUp(self) -> None:
        self.df = pd.DataFrame({'a': [1, 2, 3], 'b': ['10', '20', '30']})

    def tearDown(self) -> None:
        self.df = None

    def test_insert_df(self) -> None:
        with MySQLUtil(server=SERVER, db=DB, user=USER, password=PASSWORD) as my:
            my.insert_df(self.df, table='test_table')
            result = my.query("select * from test_table")
            self.assertEqual(result.shape, (3, 4))

# """
# CREATE TABLE `testdb`.`test_table` (
#   `id` INT NOT NULL AUTO_INCREMENT,
#   `ts` DATETIME NULL DEFAULT CURRENT_TIMESTAMP(),
#   `a` VARCHAR(45) NULL,
#   `b` VARCHAR(45) NULL,
#   PRIMARY KEY (`id`));
# """