__author__ = 'Fahad'

from django.contrib import admin
from frontend.models import UserLog, IPLog, PermanentLimitExceptions


class UserLogAdmin(admin.ModelAdmin):
    pass



class IPLogAdmin(admin.ModelAdmin):
    pass


admin.site.register(PermanentLimitExceptions)
class PermanentLimitExceptionsAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserLog)
admin.site.register(IPLog)
admin.site.register(PermanentLimitExceptions)