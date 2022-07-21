from django.urls import path
from . import views

urlpatterns = [
    path('load-photo', views.load_photo, name='load_photo'),
    path('register/', views.register, name='register'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('password_reset/done', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>', views.reset, name='password_reset_confirm'),
    path('reset/done', views.reset_done, name='password_reset_complete'),
]
