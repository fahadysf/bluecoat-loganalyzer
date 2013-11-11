from django.db import models
from djangotoolbox.fields import ListField
import datetime
# Create your models here.

class UserLog(models.Model):
    date = models.DateField()
    first_access = models.DateTimeField(auto_now_add=True, blank=True)
    last_access = models.DateTimeField(auto_now_add=True, blank=True)
    deny_count = models.IntegerField(default=0)
    data_usage = models.IntegerField(default=0)
    denied_data_size = models.IntegerField(default=0)
    username = models.CharField(max_length=200)
    blocked = models.BooleanField(default=False)
    
    class MongoMeta:
        indexes = [
                    [('username', 1)],
                    [('date', -1)],
					[('data_usage', -1)],
					[('denied_data_size', -1)],
                  ]
				  
class IPLog(models.Model):
    date = models.DateField()
    first_access = models.DateTimeField(auto_now_add=True, blank=True)
    last_access = models.DateTimeField(auto_now_add=True, blank=True)
    deny_count = models.IntegerField(default=0)
    data_usage = models.IntegerField(default=0)
    denied_data_size = models.IntegerField(default=0)
    ip_addr = models.CharField(max_length=200)
    blocked = models.BooleanField(default=False)
    
    class MongoMeta:
        indexes = [
                    [('ip_addr', 1)],
                    [('date', -1)],
					[('data_usage', -1)],
					[('denied_data_size', -1)],
                  ]

class DailyStatistics(models.Model):
    date = models.DateField()
    total_logged_users = models.IntegerField(default=0)
    total_logged_unauth_ips = models.IntegerField(default=0)
    total_requests_denied_users = models.IntegerField(default=0)
    total_requests_denied_ips = models.IntegerField(default=0)
    total_data_users = models.IntegerField(default=0)
    total_data_unauth_ips = models.IntegerField(default=0)
    total_data_denied_users = models.IntegerField(default=0)
    total_data_denied_unauth_ips = models.IntegerField(default=0)

class LimitSettings(models.Model):
    default_limit = models.IntegerField(default=2000)
    exception_list = ListField()
    exception_limit = models.IntegerField(default=5000)
