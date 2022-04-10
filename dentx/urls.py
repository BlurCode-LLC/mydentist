from django.shortcuts import redirect
from django.urls import path
from appointment import views as appointment_views
from dentist import views as dentist_views
from login import views as login_views
from mydentist.handler import is_authenticated
from patient import views as patient_views
from . import views as dentx_views


def dentx_redirect(request):
    if is_authenticated(request, "dentist"):
        return redirect("dentx:appointments")
    else:
        return redirect("dentx:login")


urlpatterns = [
    path('', dentx_redirect, name='index'),
    path('auth/login/', login_views.dentx_login, name='login'),
    path('auth/logout/', login_views.dentx_logout, name='logout'),
    path('reminders/', dentx_views.reminders, name='reminders'),
    path('settings/<str:active_tab>/', dentist_views.settings, name='settings'),
    path('get-clinic/', dentist_views.get_clinic, name='get_clinic'),
    path('update/<str:form>/', dentist_views.update, name='update_dentist'),
    path('delete/service/', dentist_views.delete_service, name='delete_service'),
    path('delete/clinic-photo/', dentist_views.delete_cabinet_photo, name='delete_cabinet_photo'),
    path('appointments/update/', appointment_views.appointments_update, name='appointments_update'),
    path('appointments/status/update/', appointment_views.status_update, name='status_update'),
    path('appointments/delete/', appointment_views.appointments_delete, name='appointments_delete'),
    path('appointments/', appointment_views.appointments, name='appointments'),
    path('table/', appointment_views.table, name='table'),
    path('test-table/', appointment_views.test_table, name='test_table'),
    path('patients/list/', appointment_views.patients, name='patients_list'),
    path('appointment/', appointment_views.appointment, name='appointment'),
    path('board/', dentx_views.board, name='board'),
    path('patients/', patient_views.patients, name='patients'),
    path('search/', patient_views.search, name='search'),
    path('patients/<int:id>/<str:active_tab>/', patient_views.patient, name='patient'),
    path('patients/<int:id>/update/<str:form>/', patient_views.update, name='update_patient'),
    path('appointment-plan/', appointment_views.appointment_plan, name='appointment_plan'),
    path('animations/', dentx_views.animations, name='animations'),
]
