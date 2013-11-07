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

class User