from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Dentist2patient)
admin.site.register(Patient2dentist)
admin.site.register(Notification)
