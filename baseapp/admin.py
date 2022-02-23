from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import *


admin.site.site_header = _("MyDentist sayti boshqaruvi")
admin.site.site_title = _("MyDentist sayti boshqaruvi")


admin.site.register(Language)
admin.site.register(Region)
admin.site.register(Gender)
