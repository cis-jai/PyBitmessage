# pylint: disable=missing-docstring
import asyncore

try:
    from .http import HttpConnection
    from .tls import TLSDispatcher
except:
    from pybitmessage.network.http import HttpConnection
    from pybitmessage.network.tls import TLSDispatcher
"""
self.sslSock = ssl.wrap_socket(
    self.sock,
    keyfile=os.path.join(paths.codePath(), 'sslkeys', 'key.pem'),
    certfile=os.path.join(paths.codePath(), 'sslkeys', 'cert.pem'),
    server_side=not self.initiatedConnection,
    ssl_version=ssl.PROTOCOL_TLSv1,
    do_handshake_on_connect=False,
    ciphers='AECDH-AES256-SHA')
"""


class HTTPSClient(HttpConnection, TLSDispatcher):
    def __init__(self, host, path):
        # pylint: disable=non-parent-init-called
        if not hasattr(self, '_map'):
            asyncore.dispatcher.__init__(self)
        self.tlsDone = False
        """
        TLSDispatcher.__init__(
            self,
            address=(host, 443),
            certfile='/home/shurdeek/src/PyBitmessage/sslsrc/keys/cert.pem',
            keyfile='/home/shurdeek/src/PyBitmessage/src/sslkeys/key.pem',
            server_side=False,
            ciphers='AECDH-AES256-SHA')
        """
        HttpConnection.__init__(self, host, path, connect=False)
        TLSDispatcher.__init__(self, address=(host, 443), server_side=False)

    def handle_connect(self):
        TLSDispatcher.handle_connect(self)

    def handle_close(self):
        if self.tlsDone:
            HttpConnection.close(self)
        else:
            TLSDispatcher.close(self)

    def readable(self):
        if self.tlsDone:
            return HttpConnection.readable(self)
        else:
            return TLSDispatcher.readable(self)

    def handle_read(self):
        if self.tlsDone:
            HttpConnection.handle_read(self)
        else:
            TLSDispatcher.handle_read(self)

    def writable(self):
        if self.tlsDone:
            return HttpConnection.writable(self)
        else:
            return TLSDispatcher.writable(self)

    def handle_write(self):
        if self.tlsDone:
            HttpConnection.handle_write(self)
        else:
            TLSDispatcher.handle_write(self)


if __name__ == "__main__":
    client = HTTPSClient('anarchy.economicsofbitcoin.com', '/')
    asyncore.loop()
