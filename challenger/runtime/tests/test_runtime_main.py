"""Test suites for the application runtime."""
import logging
import os
import shutil
import signal
import threading
import time
import tempfile
import unittest

import sq.test

from ..__main__ import MainProcess
from ..__main__ import parser



class ApplicationRuntimeMainTestCase(unittest.TestCase):
    """Runs a set of tests ensuring that the application is able to
    start using its default configuration.
    """

    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.spool = tempfile.mkdtemp()
        os.environ['AORTA_SPOOL_DIR'] = self.spool
        os.environ['CHALLENGER_HTTP_PORT'] = str(sq.test.get_free_port())

        self.argv = ['-c', './etc/challenger.conf']
        self.args = parser.parse_args(self.argv)
        self.app = MainProcess(self.args)
        self.process = threading.Thread(target=self.app.start, daemon=True)

    def tearDown(self):
        if os.path.exists(os.getenv('AORTA_SPOOL_DIR')):
            shutil.rmtree(os.environ.pop('AORTA_SPOOL_DIR'))
        self.app.on_interrupt(signal.SIGTERM, None)
        if self.process.is_alive():
            self.process.join()
        logging.disable(logging.NOTSET)

    @sq.test.integration
    def test_application_starts(self):
        """Application must start regardless of upstream dependencies."""
        self.process.start()
        self.assertTrue(self.process.is_alive())

    @sq.test.integration
    def test_application_stays_alive_for_at_least_one_second(self): #pylint: disable=invalid-name
        """Application must still be alive after 1 second, regardless of upstream
        dependencies.
        """
        self.process.start()
        time.sleep(1)
        self.assertTrue(self.process.is_alive())

    @sq.test.system
    def test_application_stays_alive_for_at_least_five_seconds(self): #pylint: disable=invalid-name
        """Application must still be alive after 5 seconds, regardless of upstream
        dependencies.
        """
        self.process.start()
        time.sleep(5)
        self.assertTrue(self.process.is_alive())
