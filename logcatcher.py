#!/usr/bin/python

import re

import pymongo
import datetime, time
import time

from django.db.models import Sum, F
from django import db
import settings

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from frontend.models import UserLog, IPLog, DailyStatistics
import Queue

DATAFILE = 'usersats.json'
DENYSTATSFILE = 'denystats.json'

relay_clients = []
queue = dict()


class DataSender(LineReceiver):

    def __init__(self):
        global relay_clients, queue
        #print 'DataSender init called %s' % str(self)
    
    def connectionMade(self):
        print("Client connection from %s" % self)
        if len(self.factory.clients) >= self.factory.clients_max:
            print("Too many connections. bye !")
            self.transport.loseConnection()
        else:
            queue[self] = Queue.Queue()
            self.factory.clients.append(self)
            relay_clients.append(self)
            
    def connectionLost(self, reason):
        print('Lost client connection.  Reason: %s' % reason)
        if self in self.factory.clients:
            self.factory.clients.remove(self)
            relay_clients.remove(self)
            del queue[self]

    def have_data(self):
        line = (queue[self]).get()
        self.sendLine(line)
        
class LogProcessor():

    last_update = time.time()
    last_update_lines = 0
    userlog_dict = dict()
    iplog_dict = dict()
    objects_requiring_update = list()
    daily_stats = None
    lines_recieved = 0
    lre = re.compile('(?P<date>\d{4}-\d{2}-\d{2}) (?P<timestamp>\d{2}\:\d{2}:\d{2}) (?P<exec_time>\d*) '+
                     '(?P<src_ip>\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) (?P<username>\S+) \S+ (?P<exception_id>\S+) '+
                     '(?P<filter_result>\S+) (?P<categories>"[^"]*") \S+\s*(?P<http_status>\S+) (?P<action>\S+) '+
                     '(?P<http_method>\S+) (?P<content_type>\S+) \S+ \S+ \S+ \S+ \S+ \S+ (?P<user_agent>"[\s\S]*"|-) '+
                     '(?P<proxy_ip>\S+) (?P<datasize>\d+) (?P<client_datasize>\d+)')
    
    def __init__(self):
        #print 'LogProcessor init called %s' % str(self)
        try:
            stats_obj = DailyStatistics.objects.get(date=datetime.datetime.now().date())
        except:
            stats_obj = DailyStatistics()
            stats_obj.date = datetime.datetime.now().date()

        self.daily_stats = stats_obj
        return

    def update_stats(self):
        self.daily_stats.total_logged_users = UserLog.objects.count()
        self.daily_stats.total_logged_unauth_ips = IPLog.objects.count()
        qs_users = UserLog.objects.filter(date=datetime.datetime.now().date())
        qs_ips = IPLog.objects.filter(date=datetime.datetime.now().date())
        self.daily_stats.total_requests_denied_users = qs_users.aggregate(Sum('deny_count'))['deny_count__sum']
        self.daily_stats.total_requests_denied_ips = qs_ips.aggregate(Sum('deny_count'))['deny_count__sum']
        self.daily_stats.total_data_users = qs_users.aggregate(Sum('data_usage'))['data_usage__sum']
        self.daily_stats.total_data_unauth_ips = qs_ips.aggregate(Sum('data_usage'))['data_usage__sum']
        self.daily_stats.total_data_denied_users = qs_users.aggregate(Sum('denied_data_size'))['denied_data_size__sum']
        self.daily_stats.total_data_denied_unauth_ips = qs_ips.aggregate(Sum('denied_data_size'))['denied_data_size__sum']
        self.daily_stats.save()

class LogReceiver(LineReceiver):
    delimiter = '\n'
    log_processor = None

    def __init__(self, log_processor):
        self.log_processor = log_processor
    
    def connectionMade(self):
        print("Client connection from %s" % self)
        if len(self.factory.clients) >= self.factory.clients_max:
            #log.msg("Too many connections. bye !")
            self.transport.loseConnection()
        else:
            self.factory.clients.append(self)
 
    def connectionLost(self, reason):
        #log.msg('Lost client connection.  Reason: %s' % reason)
        if len(self.factory.clients):
            self.factory.clients.remove(self)
 
    def lineReceived(self, line):
        #log.msg('%s' % (line))
        self.process_logline(line)
 
    def process_logline(self,line):
        self.log_processor.lines_recieved +=1
        global queue
        try:
            res =  self.log_processor.lre.match(line)
            if res != None:
                res = res.groupdict()
                timestamp = ( datetime.datetime.strptime(res['date']+' '+res['timestamp'], "%Y-%m-%d %H:%M:%S")
                               +datetime.timedelta(hours=settings.UTC_OFFSET))
                res['date'] = timestamp.date()
            for key in queue:
                queue[key].put(line)
                key.have_data()
        except:
            print '-----'+line+'\n\n\n\n'
            raise
        if res == {} or res==None:
            #print "NON LOG DATA:"+line
            pass
        # For logs without usernames (unauthenticated IPs)
        elif res['username']=='-':
            if not self.log_processor.iplog_dict.has_key(res['date']):
                self.log_processor.iplog_dict[res['date']] = {}

            # Initialize the object
            if self.log_processor.iplog_dict[res['date']].has_key(res['src_ip']):
                obj = self.log_processor.iplog_dict[res['date']][res['src_ip']]
                obj.last_access = timestamp
            else:
                try:
                    obj = IPLog.objects.get(date=res['date'], ip_addr=res['src_ip'])
                    self.log_processor.iplog_dict[res['date']][res['src_ip']] = obj
                except:
                    obj = IPLog()
                    obj.ip_addr = res['src_ip']
                    obj.date = res['date']
                    obj.last_access = timestamp
                    obj.first_access = timestamp

            if res['action'] == 'TCP_DENIED':
                obj.deny_count += 1
                obj.denied_data_size += int(res['datasize'])
            else:
                obj.data_usage += int(res['datasize'])
            # Put the object in the requiring update queue
            self.log_processor.iplog_dict[res['date']][res['src_ip']] = obj
            if not obj.ip_addr in self.log_processor.objects_requiring_update:
                self.log_processor.objects_requiring_update.append(obj.ip_addr)

        else:
            if not self.log_processor.userlog_dict.has_key(res['date']):
                self.log_processor.userlog_dict[res['date']] = {}

            if self.log_processor.userlog_dict[res['date']].has_key(res['username']):
                obj = self.log_processor.userlog_dict[res['date']][res['username']]
                obj.last_access = timestamp
            else:
                try:
                    obj = UserLog.objects.get(date=res['date'], username=res['username'])

                except:
                    obj = UserLog()
                    obj.username = res['username']
                    obj.date = res['date']
                    obj.last_access = timestamp
                    obj.first_access = timestamp


            if res['action'] == 'TCP_DENIED':
                obj.deny_count += 1
                obj.denied_data_size += int(res['datasize'])
            else:
                obj.data_usage += int(res['datasize'])
            # Put the object in the requiring update queue
            self.log_processor.userlog_dict[res['date']][res['username']] = obj
            if not obj.username in self.log_processor.objects_requiring_update:
                self.log_processor.objects_requiring_update.append(obj.username)
            pending_lines = self.log_processor.lines_recieved - self.log_processor.last_update_lines
            if (datetime.datetime.now() > obj.last_access):
                lag = (datetime.datetime.now() - obj.last_access).seconds
            else:
                lag = 0

        try:
            if (time.time() - self.log_processor.last_update >= 5.0):
                if (lag < 200) or (pending_lines >= 10000):
                    while len(self.log_processor.objects_requiring_update)>0:
                        u_or_ip = self.log_processor.objects_requiring_update.pop()
                        try:
                            obj = self.log_processor.userlog_dict[res['date']][u_or_ip]
                        except:
                            obj = self.log_processor.iplog_dict[res['date']][u_or_ip]
                        obj.save()
                    self.log_processor.last_update = time.time()
                    self.log_processor.last_update_lines = self.log_processor.lines_recieved
                    print "[%s] Updateing Database: Lines Processed since last update: %d - Total Lines Processed: %d - Relay Clients Connected: %d - Last Log Timestamp: %s" % (
                        str(datetime.datetime.now()),
                        pending_lines,
                        self.log_processor.lines_recieved,
                        len(queue.keys()),
                        str(obj.last_access),
                    )
                    self.log_processor.update_stats()
                else:
                    print "[%s] Lag greater than 200 seconds (%ds). Processing more lines before updating DB. Pending Lines: %d" %(
                        str(datetime.datetime.now()),
                        lag,
                        pending_lines,
                    )
                db.reset_queries()
                self.log_processor.last_update = time.time()

        except:
            pass
        return
        
class LogRecieverFactory(ServerFactory):
    
    protocol = LogReceiver
    def __init__(self, processor, clients_max=10):
        self.clients_max = clients_max
        self.clients = []
        self.processor = lp
        
    def buildProtocol(self, addr):
        c = LogReceiver(self.processor)
        c.factory = self 
        return c

class RelayFactory(ServerFactory):
    protocol = DataSender
    def __init__(self, processor, clients_max=10):
        self.clients_max = clients_max
        self.clients = []
        

#log.startLogging(sys.stdout)
lp = LogProcessor()
ds = DataSender()
reactor.listenTCP(9989, RelayFactory(10))
reactor.listenTCP(5140, LogRecieverFactory(lp, 10))
reactor.run()