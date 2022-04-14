from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.results, name='results'),
    path('get_dentists/', views.get_dentists, name='get_dentists'),
    path('sendMessage/', views.send_message, name='send_message'),
]
