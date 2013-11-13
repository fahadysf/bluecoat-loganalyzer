__author__ = 'Fahad'

from django.contrib import admin
from frontend.models import UserLog, IPLog, DailyExceptions, PermanentLimitExceptions


class UserLogAdmin(admin.ModelAdmin):
    list_display = ('username','date','data_usage','deny_count','blocked')
    readonly_fields = ('username','date','data_usage','deny_count','blocked')
    list_filter = ['blocked']
    search_fields = ('username',)

class IPLogAdmin(admin.ModelAdmin):
    list_display = ('ip_addr','date','data_usage','deny_count','blocked')
    readonly_fields = ('username','date','data_usage','deny_count','blocked')
    list_filter = ['blocked']
    search_fields = ('ip_addr',)

class DailyExceptionsAdmin(admin.ModelAdmin):
    list_display = ('username','ip_addr','date','data_limit')
    search_fields = ('ip_addr','username')

class PermanentLimitExceptionsAdmin(admin.ModelAdmin):
    list_display = ('username','ip_addr','data_limit')
    search_fields = ('ip_addr','username')

admin.site.register(UserLog, UserLogAdmin)
admin.site.register(IPLog, IPLogAdmin)
admin.site.register(DailyExceptions, DailyExceptionsAdmin)
admin.site.register(PermanentLimitExceptions, PermanentLimitExceptionsAdmin)