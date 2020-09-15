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
        self.debug_file.write('---this put condition--\n')
        self.debug_file.write('this put condition- ')
        self.debug_file.write('Current-thread-{} \n'.format(
            threading.current_thread().name))
        self.debug_file.write('Traceback-{} \n'.format(
            str(traceback.format_stack())))
        self.debug_file.write('Printig the put item-{}'.format(
            item))
        Queue.Queue.put(self, item, block, timeout)
        self.debug_file.write('-------------------\n \n')
        
    
    def get(self, block =True, timeout=None):
        self.debug_file.write('---this get condition ---\n')
        self.debug_file.write('Current-thread-{} \n '.format(
            threading.current_thread().name))
        self.debug_file.write('Traceback-{} \n'.format(
            str(traceback.format_stack())))
        item = Queue.Queue.get(self, block, timeout)
        self.debug_file.write('Printig the get item-{}'.format(
            str(item)))
        self.debug_file.write('-------------------\n \n')
        return item


class apiAddressGeneratorReturnQueueQueueClass(Queue.Queue):
    
    debug_file = open("/tmp/apiAddressGeneratorReturnQueue.log", "a")
    
    def __init__(self):
        self.debug_file.write(
            'apiAddressGeneratorReturnQueueQueue started.....\n'
        )
        Queue.Queue.__init__(self)

    def put(self, item, block =True, timeout=None):
        self.debug_file.write('-------------------\n')
        self.debug_file.write('this put condition- ')
        self.debug_file.write('@@@@@@ put 51 @@@@@@\n')
        self.debug_file.write(threading.current_thread().name)
        self.debug_file.write('@@@@@@ put 53 @@@@@@\n')
        self.debug_file.write(str(traceback.print_exc()))
        self.debug_file.write('@@@@@@ put 55 @@@@@@\n')
        Queue.Queue.put(self, item, block, timeout)
        self.debug_file.write('@@@@@@ put 57 @@@@@@\n') 
        self.debug_file.write('-------------------\n')
        
    
    def get(self, block =True, timeout=None):
        self.debug_file.write('-------------------\n')
        self.debug_file.write('this get condition -')
        self.debug_file.write('@@@@@@ get 64 @@@@@@')
        self.debug_file.write(threading.current_thread().name)
        self.debug_file.write('@@@@@@ get 66 @@@@@@')
        self.debug_file.write(str(traceback.print_exc()))
        self.debug_file.write('@@@@@@ get 68 @@@@@@')
        item = Queue.Queue.get(self, block, timeout)
        self.debug_file.write('@@@@@@ get 70 @@@@@@')
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
apiAddressGeneratorReturnQueue = apiAddressGeneratorReturnQueueQueueClass()
#: for exceptions
excQueue = Queue.Queue()


#new 