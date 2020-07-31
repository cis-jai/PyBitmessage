"""
Test for chatmsg group
"""
import unittest
from pybitmessage.messagetypes.chatmsg import Chatmsg


class TestCharMessage(unittest.TestCase):
    """
    Test case for chat message group
    """
    
    def test_decode(self):
        """Test various types of decode method"""
        from pybitmessage import messagetypes
        result = messagetypes.constructObject({'': 'chatmsg', 'message': 'hello world'})
        self.assertTrue(isinstance(result.message, str))

    def test_encode(self):
        """Test various types of encode method"""
        chat_obj = Chatmsg()
        result = chat_obj.encode({'message': 'hello world'})
        self.assertTrue(True if result['message'] else False)
