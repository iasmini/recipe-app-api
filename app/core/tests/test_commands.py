from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available. It'll try and retrieve the
         database connection from Django."""
        # patch - used to mock the ConnectionHandler
        # try to get the default database via the ConnectionHandler
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.retun_value = True
            # wait_for_db is the name of our management command
            call_command('wait_for_db')

            self.assertEqual(gi.call_count, 1)

    # patch decorator: instead of mocking what we're mocking here we're going
    # to mock the time.sleep
    # pass the return_value as part of the function call
    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        """Test waiting for db"""
        # if gets OperationalError, waits a second to try to reconnect
        # we need to add the extra argument for 'ts' even though we're not
        # using it because when you run the test it will error, an unexpected
        # argument
        # What this mock does here is it replaces the behavior of time.sleep
        # with a mock function that returns true. So during our test it won't
        # actually wait the seconds. It is just to speed up
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # side effect - it raises the operational error 5 times and then on
            # the sixth time it won't raise the error it will just return.
            gi.side_effect = [OperationalError] * 5 + [True]
            # wait_for_db is the name of our management command
            call_command('wait_for_db')

            self.assertEqual(gi.call_count, 6)
