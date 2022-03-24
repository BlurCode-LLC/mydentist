from django.contrib import admin
from .models import *


class ExpireAdmin(admin.ModelAdmin):
    list_display = ("dentist", "expire_date")
    fields = ("dentist", )

admin.site.register(Clinic)
admin.site.register(Clinic_translation)
admin.site.register(User)
admin.site.register(User_translation)
admin.site.register(Service)
admin.site.register(Service_translation)
admin.site.register(Cabinet_Image)
admin.site.register(Reminder)
admin.site.register(Reason)
admin.site.register(Expire, ExpireAdmin)
