from django.db import models
from djangotoolbox.fields import ListField
import datetime
import settings
# Create your models here.

class PermanentLimitExceptions(models.Model):
    username = models.CharField(blank=True, max_length=200, default='')
    ip_addr = models.CharField(blank=True, max_length=200, default='')
    data_limit = models.IntegerField(default=0)

    def __str__(self):
        if self.username != '':
            return self.username
        else:
            return self.ip_addr

class UserLog(models.Model):
    date = models.DateField()
    first_access = models.DateTimeField(auto_now_add=True, blank=True)
    last_access = models.DateTimeField(auto_now_add=True, blank=True)
    deny_count = models.IntegerField(default=0)
    data_usage = models.IntegerField(default=0)
    custom_limit = models.IntegerField(default=-1)
    denied_data_size = models.IntegerField(default=0)
    username = models.CharField(max_length=200)
    blocked = models.BooleanField(default=False)
    data_usage_mb = data_usage/(1024**2)


    def data_limit(self):
        try:
            exception = PermanentLimitExceptions.objects.get(username=self.username)
        except:
            exception = None
        if exception:
            return exception.data_limit
        elif self.custom_limit != -1:
            return self.custom_limit
        else:
            return settings.DEFAULT_DATA_LIMIT

    data_usage_mb = data_usage/(1024**2)

    def is_blocked(self):
        if self.data_usage >= self.data_limit():
            return True
        else:
            return False

    def save(self):
        self.blocked = self.is_blocked()
        super(UserLog, self).save()

    def __str__(self):
        return self.username

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
    custom_limit = models.IntegerField(default=-1)
    denied_data_size = models.IntegerField(default=0)
    ip_addr = models.CharField(max_length=200)
    blocked = models.BooleanField(default=False)
    def data_usage_mb(self):
        return data_usage/(1024**2)

    def data_limit(self):
        try:
            exception = PermanentLimitExceptions.objects.get(username=self.username)
        except:
            exception = None

        if exception:
            return exception.data_limit
        elif self.custom_limit != -1:
            return self.custom_limit
        else:
            return settings.DEFAULT_DATA_LIMIT

    def is_blocked(self):
        if self.data_usage >= self.data_limit():
            return True
        else:
            return False

    def save(self):
        self.blocked = self.is_blocked()
        super(IPLog, self).save()

    def __str__(self):
        return self.ip_addr

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

    def __str__(self):
        return str(self.date)