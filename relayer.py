#!/usr/bin/python
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class DataSender(DatagramProtocol):

    def startProtocol(self):
        host = "127.0.0.1"
        port = 9989
        self.transport.connect(host, port)
        print "Sending UDP log stream to %s" % str((host, port))
        
    def sendData(self,data):
        self.transport.write(data) # no need for address

"""
# 0 means any port, we don't care in this case
ds = DataSender()
reactor.listenUDP(9989, ds)
reactor.run()
"""