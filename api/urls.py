from django.urls import path
from django.views.generic import TemplateView
from rest_framework_swagger.views import get_swagger_view

from . import views


schema_view = get_swagger_view(title='MyDentist API')

urlpatterns = [
    path('', TemplateView.as_view(
        template_name="swagger.html",
        extra_context={
            'schema_url': "api/"
        }
    ), name='swagger'),
    path('index/', views.index, name='api_index'),
    path("results/", views.results, name="api_results"),
    path("dentist/", views.dentist, name="api_dentist"),
    path("query/", views.query, name="api_query"),
    path("register/user/", views.register_user, name="api_register_user"),
    path("register/illness/", views.register_illness, name="api_register_illness"),
    path("register/other-illness/", views.register_other_illness, name="api_register_other_illness"),
    path("token/", views.token, name="api_token"),
    path("token/refresh/", views.refresh, name="api_token_refresh"),
    path("profile/", views.profile, name="api_profile"),
    path("settings/", views.settings, name="api_settings"),
    path("update/user/", views.update_user, name="api_update_user"),
    path("update/password/", views.update_password, name="api_update_password"),
    path("update/illness/", views.update_illness, name="api_update_illness"),
    path("update/other-illness/", views.update_other_illness, name="api_update_other_illness"),
]
