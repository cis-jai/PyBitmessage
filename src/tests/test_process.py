"""
Common reusable code for tests and tests for pybitmessage process.
"""

import os
import signal
import subprocess  # nosec
import tempfile
import time
import unittest

try:
    import psutil
except ModuleNotFoundError:
    pass

from pybitmessage.debug import logger


def put_signal_file(path, filename):
    """Creates file, presence of which is a signal about some event."""
    with open(os.path.join(path, filename), 'wb') as outfile:
        outfile.write(str(time.time()).encode())

class TestProcessProto(unittest.TestCase):
    """Test case implementing common logic for external testing:
              it starts pybitmessage in setUpClass() and stops it in tearDownClass()
    """
    
    _process_cmd = ['pybitmessage', '-d']
    _threads_count = 15
    _files = (
        'keys.dat', 'messages.dat', 'knownnodes.dat',
        '.api_started', 'unittest.lock','singleton.lock'
    )
 
    @classmethod
    def setUpClass(cls):
        """Setup environment and start pybitmessage"""
        logger.error('Hello I am the setupClass')
        cls.home = os.environ['BITMESSAGE_HOME'] = tempfile.gettempdir()
        put_signal_file(cls.home, 'unittest.lock')
        subprocess.call(cls._process_cmd)  # nosec
        time.sleep(5)
        cls.pid = int(cls._get_readline('singleton.lock'))
        cls.process = psutil.Process(cls.pid)
 
    @classmethod
    def _get_readline(cls, pfile):
        pfile = os.path.join(cls.home, pfile)
        try:
            return open(pfile, 'rb').readline().strip()
        except (OSError, IOError, FileNotFoundError):
            pass

    @classmethod
    def _stop_process(cls, timeout=5):
        cls.process.send_signal(signal.SIGTERM)
        try:
            cls.process.wait(timeout)
            try:
                print('55555555555555555')
                print('psutil.pid_exists(cls.process.pid)-{}'.format(
                    psutil.pid_exists(cls.process.pid)))      
                print('55555555555555555')
            except:
                pass
            logger.error('_stop_process')
            logger.error('this condition are getting killed are not')
            logger.error('__stop__process')
        except psutil.TimeoutExpired:
            logger.error('#####_stop_process method condition--##')
            try:
                logger.error('cls.process PID -{}'.format(cls.process.pid))
            except:
                logger.error('cls.process -{}'.format(cls.process))

            logger.error('#####_stop_process method condition--##')            
            return False
        return True

    @classmethod
    def _cleanup_files(cls):
        for pfile in cls._files:
            try:
                os.remove(os.path.join(cls.home, pfile))
            except OSError:
                pass

    @classmethod
    def tearDownClass(cls):
        """Ensures that pybitmessage stopped and removes files"""
        try:
            print('is ever called tearDownC')
            if not cls._stop_process():
                cls.process.kill()
                logger.error('***********************')
                logger.error('tearDownClass are successfully killed')
                logger.error('***********************')
        except (psutil.NoSuchProcess, FileNotFoundError, AttributeError) as e:
            pass
        finally:
            cls._cleanup_files()

    def _test_threads(self):
        # only count for now
        # because of https://github.com/giampaolo/psutil/issues/613
        # PyBitmessage
        #   - addressGenerator
        #   - singleWorker
        #   - SQL
        #   - objectProcessor
        #   - singleCleaner
        #   - singleAPI
        #   - Asyncore
        #   - ReceiveQueue_0
        #   - ReceiveQueue_1
        #   - ReceiveQueue_2
        #   - Announcer
        #   - InvBroadcaster
        #   - AddrBroadcaster
        #   - Downloader
        self.assertEqual(
            len(self.process.threads()), self._threads_count)


class TestProcessShutdown(TestProcessProto):
    """Separate test case for SIGTERM"""
    def test_shutdown(self):
        """Send to pybitmessage SIGTERM and ensure it stopped"""
        # longer wait time because it's not a benchmark
        self.assertTrue(
            self._stop_process(20),
            '%s has not stopped in 20 sec' % ' '.join(self._process_cmd))

    @classmethod
    def tearDownClass(cls):
        """Special teardown because pybitmessage is already stopped"""
        cls._cleanup_files()


class TestProcess(TestProcessProto):
    """A test case for pybitmessage process"""
    def test_process_name(self):
        """Check PyBitmessage process name"""
        self.assertEqual(self.process.name(), 'pybitmessage')

    def test_files(self):
        """Check existence of PyBitmessage files"""
        for pfile in self._files:
            if pfile.startswith('.'):
                continue
            self.assertIsNot(
                self._get_readline(pfile), None,
                'Failed to read file {}'.format(pfile)
            )

    def test_threads(self):
        """Testing PyBitmessage threads"""
        self._test_threads()
