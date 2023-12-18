from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path("",views.home, name = "home"),
    path('login/', views.login, name='login'),
    path('admin/', views.admin, name='admin'),
    path('generaldoc/', views.generaldoc, name='generaldoc'),
    path('staff/', views.staff, name='staff'),
    path('surgerydoc/', views.surgerydoc, name='surgerydoc'),
    path('adddoc/', views.adddoc, name='adddoc'),
    path('add_doctor/', views.add_doctor, name='add_doctor'),
    path('adddept/', views.adddept, name='adddept'),
    path('add_dept/', views.add_dept, name='add_dept'),
    path('add_oproom/', views.add_oproom, name='add_oproom'),
    path('add_oper_room/', views.add_oper_room, name='add_oper_room'),
    path('addstaff/', views.addstaff, name='addstaff'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('manage_doc/', views.manage_doc, name='manage_doc'),
    path('manage_dept/', views.manage_dept, name='manage_dept'),
    path('manage_oproom/', views.manage_oproom, name='manage_oproom'),
    path('manage_staff/', views.manage_staff, name='manage_staff'),
    path('manage_inpatient/', views.manage_inpatient, name='manage_inpatient'),
    path('manage_outpatient/', views.manage_outpatient, name='manage_outpatient'),
    path('manage_patient/', views.manage_patient, name='manage_patient'),
    path('addpatient/', views.addpatient, name='addpatient'),
    path('add_patient/', views.add_patient, name='add_patient'),
    path('addoutpatient/', views.addoutpatient, name='addoutpatient'),
    path('add_outpatient/', views.add_outpatient, name='add_outpatient'),
    path('addinpatient/', views.addinpatient, name='addinpatient'),
    path('add_inpatient/', views.add_inpatient, name='add_inpatient'),


] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)