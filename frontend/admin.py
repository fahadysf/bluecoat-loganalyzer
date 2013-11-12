__author__ = 'Fahad'

from django.contrib import admin
from frontend.models import UserLog, IPLog, PermanentLimitExceptions


class UserLogAdmin(admin.ModelAdmin):
    list_display = ('username','date','data_usage','deny_count','custom_limit','blocked')
    list_filter = ('date','data_usage','blocked')
    search_fields = ('username',)

class IPLogAdmin(admin.ModelAdmin):
    list_display = ('ip_addr','date','data_usage','deny_count','custom_limit','blocked')
    list_filter = ('date','data_usage','blocked')
    search_fields = ('ip_addr',)

class PermanentLimitExceptionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserLog, UserLogAdmin)
admin.site.register(IPLog, IPLogAdmin)
admin.site.register(PermanentLimitExceptions, PermanentLimitExceptionsAdmin)