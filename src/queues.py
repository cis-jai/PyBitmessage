"""Most of the queues used by bitmessage threads are defined here."""
import queue as Queue

import threading
import time 
import traceback

try:
    from multiqueue import MultiQueue
except ModuleNotFoundError:
    from pybitmessage.multiqueue import MultiQueue

class ObjectProcessorQueue(Queue.Queue):
    """Special queue class using lock for `.threads.objectProcessor`"""

    maxSize = 32000000

    def __init__(self):
        Queue.Queue.__init__(self)
        self.sizeLock = threading.Lock()
        #: in Bytes. We maintain this to prevent nodes from flooding us
        #: with objects which take up too much memory. If this gets
        #: too big we'll sleep before asking for further objects.
        self.curSize = 0

    def put(self, item, block=True, timeout=None):
        """Putting values in queues"""
        while self.curSize >= self.maxSize:
            time.sleep(1)
        with self.sizeLock:
            self.curSize += len(item[1])
        Queue.Queue.put(self, item, block, timeout)

    def get(self, block=True, timeout=None):
        """Getting values from queues"""
        item = Queue.Queue.get(self, block, timeout)
        with self.sizeLock:
            self.curSize -= len(item[1])
        return item

class addressGeneratorQueueClass(Queue.Queue):
    
    debug_file = open("/tmp/addressgenerator.log", "a")
    
    def __init__(self):
        Queue.Queue.__init__(self)
        
    def put(self, item, block =True, timeout=None):
        self.debug_file.write('-------------------\n')
        self.debug_file.write('this put condition- ')
        self.debug_file.write(threading.current_thread().name)
        self.debug_file.write(traceback.print_exc())
        Queue.Queue.put(self, item, block, timeout)
        self.debug_file.write('-------------------\n')
        
    
    def get(self, item, block =True, timeout=None):
        self.debug_file.write('-------------------\n')
        self.debug_file.write('this get condition -')
        self.debug_file.write(threading.current_thread().name)
        self.debug_file.write(traceback.print_exc())
        item = Queue.Queue.get(self, block, timeout)
        self.debug_file.write('-------------------\n')
        return item

workerQueue = Queue.Queue()
UISignalQueue = Queue.Queue()
addressGeneratorQueue = addressGeneratorQueueClass()
#: `.network.ReceiveQueueThread` instances dump objects they hear
#: on the network into this queue to be processed.
objectProcessorQueue = ObjectProcessorQueue()
invQueue = MultiQueue()
addrQueue = MultiQueue()
portCheckerQueue = Queue.Queue()
receiveDataQueue = Queue.Queue()
#: The address generator thread uses this queue to get information back
#: to the API thread.
apiAddressGeneratorReturnQueue = Queue.Queue()
#: for exceptions
excQueue = Queue.Queue()


#new 