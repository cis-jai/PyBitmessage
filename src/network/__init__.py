
"""
Network subsystem packages
"""
import sys

if sys.version_info[0] == 2:
    from addrthread import AddrThread
    from announcethread import AnnounceThread
    from connectionpool import BMConnectionPool
    from dandelion import Dandelion
    from downloadthread import DownloadThread
    from invthread import InvThread
    from networkthread import BMNetworkThread
    from receivequeuethread import ReceiveQueueThread
    from threads import StoppableThread
    from uploadthread import UploadThread

else:
    from network.addrthread import AddrThread
    from network.announcethread import AnnounceThread
    from network.connectionpool import BMConnectionPool
    from network.dandelion import Dandelion
    from network.downloadthread import DownloadThread
    from network.invthread import InvThread
    from network.networkthread import BMNetworkThread
    from network.receivequeuethread import ReceiveQueueThread
    from network.threads import StoppableThread
    from network.uploadthread import UploadThread


__all__ = [
    "BMConnectionPool", "Dandelion",
    "AddrThread", "AnnounceThread", "BMNetworkThread", "DownloadThread",
    "InvThread", "ReceiveQueueThread", "UploadThread", "StoppableThread"
]
