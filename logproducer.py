# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.
"""
An example client. Run simpleserv.py first before running this.
"""

from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet.threads import deferToThread
import math
import random
import time

# a client protocol
class LogGeneratingClient(LineReceiver):
    """Once connected, send a message, then print the result."""
    
    def genRandomLine(self):
        return '2013-10-02 10:53:54 1 10.3.10.69 %s - - - "-" http://-/  304 - - - - - 80 - - - "-" 10.0.9.20 %d 845 - - -\n' % ('user-'+str('%d' % math.ceil(random.random()*100)), math.ceil(random.betavariate(1,20)*1000000))
        
    def sendRandomLine(self, data=None):
        if data is not None:
            self.transport.write(self.genRandomLine())
        time.sleep(0.004)
        deferToThread(self.genRandomLine).addCallback(self.sendRandomLine)        
        
    def connectionMade(self):
        print "sending"
        self.sendRandomLine()
            
    def dataReceived(self, data):
        "As soon as any data is received, write it back."
        print "Server said:", data
        self.transport.loseConnection()
    
    def connectionLost(self, reason):
        print "connection lost"

class LogLineFactory(protocol.ClientFactory):
    protocol = LogGeneratingClient
    
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()

# this connects the protocol to a server runing on port 8000
def main():
    f = LogLineFactory()
    reactor.connectTCP("localhost", 5140, f)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()