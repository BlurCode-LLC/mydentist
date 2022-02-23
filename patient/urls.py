from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('settings/<str:active_tab>', views.settings, name='settings'),
    path('update/<str:form>', views.update, name='update'),
]
