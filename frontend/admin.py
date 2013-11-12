__author__ = 'Fahad'

from django.contrib import admin
from frontend.models import UserLog, IPLog, PermanentLimitExceptions


class UserLogAdmin(admin.ModelAdmin):
    pass



class IPLogAdmin(admin.ModelAdmin):
    pass


adminte.site.register(PermanentLimitExceptions)
class PermanentLimitExceptionsAdmin(admin.ModelAdmin):
    pass

adminte.site.register(UserLog)
adminte.site.register(IPLog)
adminte.site.register(PermanentLimitExceptions)