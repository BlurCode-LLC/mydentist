from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic.base import RedirectView
from . import handler


urlpatterns = [
    path('', include(('baseapp.urls', 'baseapp'), namespace='baseapp')),
    path('admin/', admin.site.urls, name='admin'),
    path('auth/', include(('login.urls', 'login'), namespace='login')),
    path('dentist/', include(('dentist.urls', 'dentist'), namespace='dentist')),
    path('dentx/', include(('dentx.urls', 'dentx'), namespace='dentx')),
    path('my/', include(('patient.urls', 'patient'), namespace='patient')),
    path('bot/', include(('bot.urls', 'bot'), namespace='bot')),
    path('set_language/<user_language>', handler.set_language, name='set_language'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url("favicon.ico"))),
] + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'baseapp.views.error_404'
handler403 = 'baseapp.views.error_403'
