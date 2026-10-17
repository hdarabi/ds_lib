################################################################################
# Name        : test_vertica
# Description : Unit tests for the Vertica connection. The live tests run only
# when VERTICA_HOST, VERTICA_USER, VERTICA_PASS and VERTICA_DB are set and
# create and drop the public.ds_lib_test_vertica table.
# Version     : 0.0.0
# Created On  : 2026-10-17
# Modified On : 2026-10-17
# Author      : Hamid R. Darabi, Ph.D.
################################################################################

import io
import os
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
from ds_lib.vertica import Vertica


PARAMS = {'host': 'vertica.example.com', 'port': 5433, 'user': 'dbadmin', 'password': 'secret', 'database': 'db'}


class TestVertica(unittest.TestCase):
    def setUp(self) -> None:
        patcher = patch('ds_lib.vertica.vertica_python.connect')
        self.connect = patcher.start()
        self.addCleanup(patcher.stop)
        self.connection = self.connect.return_value
        self.cursor = self.connection.cursor.return_value

    def test_connection_parameters_are_used(self) -> None:
        with Vertica(dict(PARAMS)):
            pass
        self.connect.assert_called_once_with(**PARAMS)
        self.connection.close.assert_called_once_with()

    def test_execute_no_value_reopens_cursor_and_commits(self) -> None:
        with Vertica(dict(PARAMS)) as v:
            self.connection.cursor.reset_mock()
            v.execute_no_value('DELETE FROM t')
        self.connection.cursor.assert_called_once_with()
        self.cursor.execute.assert_called_once_with('DELETE FROM t')
        self.connection.commit.assert_called_once_with()

    def test_verbose_hides_password(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            with Vertica(dict(PARAMS), verbose=True):
                pass
        self.assertIn('vertica.example.com', output.getvalue())
        self.assertNotIn('secret', output.getvalue())


@unittest.skipUnless(os.getenv('VERTICA_HOST'), 'VERTICA_HOST is not set')
class TestVerticaLive(unittest.TestCase):
    TABLE = 'public.ds_lib_test_vertica'

    def setUp(self) -> None:
        with Vertica() as v:
            v.execute_no_value('DROP TABLE IF EXISTS {0}'.format(self.TABLE))
            v.execute_no_value('CREATE TABLE {0} (id INT)'.format(self.TABLE))

    def tearDown(self) -> None:
        with Vertica() as v:
            v.execute_no_value('DROP TABLE IF EXISTS {0}'.format(self.TABLE))

    def test_execute_no_value_after_query(self) -> None:
        with Vertica() as v:
            v.query('SELECT 1')
            v.execute_no_value('INSERT INTO {0} VALUES (1)'.format(self.TABLE))

    def test_execute_no_value_commits(self) -> None:
        with Vertica() as v:
            v.execute_no_value('INSERT INTO {0} VALUES (1)'.format(self.TABLE))
        with Vertica() as v:
            result = v.query('SELECT COUNT(*) FROM {0}'.format(self.TABLE))
        self.assertEqual(result.iloc[0, 0], 1)
