"""
Tests using API.
"""

import base64
import json
import time
import xmlrpc.client as xmlrpclib  # nosec

from .test_process import TestProcessProto, TestProcessShutdown
from .tests_compatibility import utils

from pybitmessage.debug import logger
class TestAPIProto(TestProcessProto):
    """Test case logic for testing API"""
    _process_cmd = ['pybitmessage', '-t']
    # _files = (
    #     'keys.dat', 'messages.dat', 'knownnodes.dat',
    #     '.api_started', 'unittest.lock'
    # )

    @classmethod
    def setUpClass(cls):
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print('is this TestAPIProto')
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        
        """Setup XMLRPC proxy for pybitmessage API"""
        # super(TestAPIProto, cls).tearDownClass()
        try:
            print('*****************************')
            print('try block is I am successfully called the ')
            print('*****************************')
            super(TestAPIProto, cls).setUpClass()
        except:
            print('(((((((((((((((((((((((')
            print('except block because of this condition are getting failed')
            print('))))))))))))))))))))))))')

        cls.addresses = []
        cls.api = xmlrpclib.ServerProxy(    
            "http://username:password@127.0.0.1:8442/")
        for _ in range(5):
            if cls._get_readline('.api_started'):
                return
            time.sleep(1)

class TestAPIShutdown(TestAPIProto, TestProcessShutdown):
    """Separate test case for API command 'shutdown'"""
    def test_shutdown(self):
        """Shutdown the pybitmessage"""
        # try:
        #     self.assertEqual(self.api.shutdown(), 'done')
        # except Exception:
        self.assertEqual(self.api.shutdown(), 'done')
        for _ in range(5):
            if not self.process.is_running():
                logger.info('-----------------------------------------')      
                logger.info('test_shutdown test_shutdown test_shutdown inside the break condition')
                logger.info('-----------------------------------------')      
                break
            time.sleep(2)
        else:
            self.fail(
                 '{} has not stopped in 10 sec'.format(' '.join(self._process_cmd)))


class TestAPI(TestAPIProto):
    """Main API test case"""
    _seed = base64.encodebytes(
        'TIGER, tiger, burning bright. In the forests of the night'.encode(
            'raw_unicode_escape'))

    def _add_random_address(self, label):
        return self.api.createRandomAddress(base64.encodestring(label))

    def test_user_password(self):
        """Trying to connect with wrong username/password"""
        api_wrong = xmlrpclib.ServerProxy("http://test:wrong@127.0.0.1:8442/")
        self.assertEqual(
            api_wrong.clientStatus(),
            'RPC Username or password incorrect or HTTP header lacks'
            ' authentication at all.'
        )

    def test_connection(self):  
        """API command 'helloWorld'"""
        self.assertEqual(
            self.api.helloWorld('hello', 'world'),
            'hello-world'
        )

    def test_arithmetic(self):
        """API command 'add'"""
        self.assertEqual(self.api.add(69, 42), 111)

    def test_invalid_method(self):
        """Issuing nonexistent command 'test'"""
        self.assertEqual(
            self.api.test(),
            'API Error 0020: Invalid method: test'
        )

    def test_clientstatus_consistency(self):
        """If networkStatus is notConnected networkConnections should be 0"""
        status = json.loads(self.api.clientStatus())
        if status["networkStatus"] == "notConnected":
            self.assertEqual(status["networkConnections"], 0)
        else:
            self.assertGreater(status["networkConnections"], 0)

    def test_list_addresses(self):
        """Checking the return of API command 'listAddresses'"""
        self.assertEqual(
            json.loads(self.api.listAddresses()).get('addresses'),
            self.addresses
        )

    def test_decode_address(self):
        """Checking the return of API command 'decodeAddress'"""
        result = json.loads(
            self.api.decodeAddress('BM-2cWzSnwjJ7yRP3nLEWUV5LisTZyREWSzUK'))
        self.assertEqual(result.get('status'), 'success')
        self.assertEqual(result['addressVersion'], 4)
        self.assertEqual(result['streamNumber'], 1)

    def test_create_deterministic_addresses(self):
        #11111111111111111111111111
        """API command 'getDeterministicAddress': with various params"""
        self.assertEqual(
            self.api.getDeterministicAddress(self._seed, 4, 1),
            'BM-2cWzSnwjJ7yRP3nLEWUV5LisTZyREWSzUK'
        )
        self.assertEqual(
            self.api.getDeterministicAddress(self._seed, 3, 1),
            'BM-2DBPTgeSawWYZceFD69AbDT5q4iUWtj1ZN'
        )
        self.assertRegexpMatches(
            self.api.getDeterministicAddress(self._seed, 2, 1),
            r'^API Error 0002:'
        )
        # This is here until the streams will be implemented
        self.assertRegexpMatches(
            self.api.getDeterministicAddress(self._seed, 3, 2),
            r'API Error 0003:'
        )

    #currently working on this condition
    def test_create_random_address(self):
        #22222222222222222222222222222222
        """API command 'createRandomAddress': basic BM-address validation"""
        addr = self._add_random_address('random_1'.encode())
        self.assertRegexpMatches(addr, r'^BM-')
        self.assertRegexpMatches(addr[3:], r'[a-zA-Z1-9]+$')
        # Whitepaper says "around 36 character"
        self.assertLessEqual(len(addr[3:]), 40)
        self.assertEqual(self.api.deleteAddress(addr), 'success')

    def test_addressbook(self):
        """Testing API commands for addressbook manipulations"""
        # Initially it's empty
        self.assertEqual(
            json.loads(self.api.listAddressBookEntries()).get('addresses'),
            []
        )
        # Add known address
        self.api.addAddressBookEntry('BM-2cWzSnwjJ7yRP3nLEWUV5LisTZyREWSzUK', 
                                     base64.encodestring(utils.encoded_string(
                                         'tiger_4')).decode())
        # Check addressbook entry
        entries = json.loads(
            self.api.listAddressBookEntries()).get('addresses')[0]
        self.assertEqual(
            entries['address'], 'BM-2cWzSnwjJ7yRP3nLEWUV5LisTZyREWSzUK')
        self.assertEqual(
            base64.decodestring(utils.encoded_string(entries['label'])), 
            utils.encoded_string('tiger_4'))
        # Remove known address
        self.api.deleteAddressBookEntry(
            'BM-2cWzSnwjJ7yRP3nLEWUV5LisTZyREWSzUK')
        # Addressbook should be empty again
        self.assertEqual(
            json.loads(self.api.listAddressBookEntries()).get('addresses'),
            []
        )

    def test_send_broadcast(self):
        """API command 'sendBroadcast': ensure it returns ackData"""
        addr = self._add_random_address('random_2'.encode())
        ack = self.api.sendBroadcast(
            addr, base64.encodestring('test_subject'),
            base64.encodestring('test message')
        )
        try:
            int(ack, 16)
        except ValueError:
            self.fail('sendBroadcast returned error or ackData is not hex')
        finally:
            self.assertEqual(self.api.deleteAddress(addr), 'success')

    def test_chan(self):
        """Testing chan creation/joining"""
        # Cheate chan with known address
        self.assertEqual(
             self.api.createChan(self._seed),
            'BM-2cWzSnwjJ7yRP3nLEWUV5LisTZyREWSzUK'
        )
        # # cleanup
        # self.assertEqual(
        #     self.api.leaveChan('BM-2cWzSnwjJ7yRP3nLEWUV5LisTZyREWSzUK'),
        #     'success'
        # )
        # # Join chan with addresses of version 3 or 4
        # for addr in (
        #         'BM-2cWzSnwjJ7yRP3nLEWUV5LisTZyREWSzUK',
        #         'BM-2DBPTgeSawWYZceFD69AbDT5q4iUWtj1ZN'
        # ):
        #     self.assertEqual(self.api.joinChan(self._seed, addr), 'success')
        #     self.assertEqual(self.api.leaveChan(addr), 'success')
        # # Joining with wrong address should fail
        # self.assertRegexpMatches(
        #     self.api.joinChan(self._seed, 'BM-2cWzSnwjJ7yRP3nLEW'),
        #     r'^API Error 0008:'
        # )
