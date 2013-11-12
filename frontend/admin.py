__author__ = 'Fahad'

from django.contrib import admin
from frontend.models import UserLog, IPLog, PermanentLimitExceptions


class UserLogAdmin(admin.ModelAdmin):
    list_display = ('username','date','data_usage')

class IPLogAdmin(admin.ModelAdmin):
    list_display = ('ip_addr','date','data_usage')

class PermanentLimitExceptionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserLog)
admin.site.register(IPLog)
admin.site.register(PermanentLimitExceptions)