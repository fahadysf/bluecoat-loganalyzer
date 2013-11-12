__author__ = 'Fahad'

from django.contrib import admin
from frontend.models import UserLog, IPLog, PermanentLimitExceptions

@admin.register(UserLog)
class UserLogAdmin(admin.ModelAdmin):
    pass


@admin.register(IPLog)
class IPLogAdmin(admin.ModelAdmin):
    pass


@admin.register(PermanentLimitExceptions)
class PermanentLimitExceptionsAdmin(admin.ModelAdmin):
    pass
