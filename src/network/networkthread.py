"""
src/network/networkthread.py
============================
"""
import network.asyncore_pollchoose as asyncore
import state
from debug import logger
from helper_threading import StoppableThread
from network.connectionpool import BMConnectionPool
from queues import excQueue


class BMNetworkThread(StoppableThread):
    """A thread to handle network concerns"""
    def __init__(self):
        super(BMNetworkThread, self).__init__(name="Asyncore")
        logger.info("init asyncore thread")

    def run(self):
        try:
            while not self._stopped and state.shutdown == 0:
                print("I am running in run method which calls a loop for BMConnectionPool line19..................................")
                BMConnectionPool().loop()
                print("I am running in run method which calls a loop for BMConnectionPool line 21..................................")
        except Exception as e:
            excQueue.put((self.name, e))
            raise

    def stopThread(self):
        super(BMNetworkThread, self).stopThread()
        for i in BMConnectionPool().listeningSockets.values():
            try:
                i.close()
            except:
                pass
        for i in BMConnectionPool().outboundConnections.values():
            try:
                i.close()
            except:
                pass
        for i in BMConnectionPool().inboundConnections.values():
            try:
                i.close()
            except:
                pass

        # just in case
        asyncore.close_all()
