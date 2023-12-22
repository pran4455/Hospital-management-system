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
    path('addtreatment/', views.addtreatment, name='addtreatment'),
    path('add_treatment/', views.add_treatment, name='add_treatment'),
    # path('addappointment/', views.addappointment, name='addappointment'),
    # path('add_appointment/', views.add_appointment, name='add_appointment'),
    # path('addsurgery/', views.addsurgery, name='addsurgery'),
    # path('add_surgery/', views.add_surgery, name='add_surgery'),
    path('update_oproom/', views.update_oproom, name='update_oproom'),
    path('updateoproom/', views.updateoproom, name='updateoproom'),
    path('update_staff/', views.update_staff, name='update_staff'),
    path('updatedoctor/', views.updatedoctor, name='updatedoctor'),
    path('update_doctor/', views.update_doctor, name='update_doctor'),
    path('updatestaff/', views.updatestaff, name='updatestaff'),
    path('del_oproom/', views.del_oproom, name='del_oproom'),
    path('deloproom/', views.deloproom, name='deloproom'),
    path('del_staff/', views.del_staff, name='del_staff'),
    path('deldoctor/', views.deldoctor, name='deldoctor'),
    path('del_doctor/', views.del_doctor, name='del_doctor'),
    path('delstaff/', views.delstaff, name='delstaff'),
    # path('viewpatient/', views.viewpatient, name='viewpatient'),
    # path('view_patient/', views.view_patient, name='view_patient'),
    path('viewinpatient/', views.viewinpatient, name='viewinpatient'),
    path('viewoproom/', views.viewoproom, name='viewoproom'),
    path('viewstaff/', views.viewstaff, name='viewstaff'),
    path('viewdept/', views.viewdept, name='viewdept'),
    path('viewdoctor/', views.viewdoctor, name='viewdoctor'),
    path('viewoutpatient/', views.viewoutpatient, name='viewoutpatient'),
    # path('view_inpatient/', views.view_inpatient, name='view_inpatient'),
    # path('viewpatient/', views.viewpatient, name='viewpatient'),
    # path('view_patient/', views.view_patient, name='view_patient'),
    path('view_patient_staff/', views.view_patient_staff, name='view_patient_staff'),
    #
    path('add_treatd/', views.add_treatd, name='add_treatd'),
    path('addtreatd/', views.addtreatd, name='addtreatd'),
    path('viewtreatmentd/', views.viewtreatmentd, name='viewtreatmentd'),
    path('view_treatmentd/', views.view_treatmentd, name='view_treatmentd'),
    #
    path('add_treats/', views.add_treats, name='add_treats'),
    path('addtreats/', views.addtreats, name='addtreats'),
    path('viewtreatments/', views.viewtreatments, name='viewtreatments'),
    path('view_treatments/', views.view_treatments, name='view_treatments'),

    #
    path('viewsurgery/', views.viewsurgery, name='viewsurgery'),
    path('view_surgery/', views.view_surgery, name='view_surgery'),
    path('addsurgery/', views.addsurgery, name='addsurgery'),
    path('add_surgery/', views.add_surgery, name='add_surgery'),




] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)