from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>/', views.dentist, name='dentist'),
    path('update-photo', views.update_photo, name='update_photo')
]
