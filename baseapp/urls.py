from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    path('api/', api.index, name='api_index'),
    path('results/', views.results, name='results'),
    path("api/results/", api.results, name = "api_results"),
    path('get_dentists/', views.get_dentists, name='get_dentists'),
    # path('get_dentists/', views.get_dentists, name='get_dentists'),
]
