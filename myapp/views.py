from django.shortcuts import render
from django.http import HttpResponse
import csv
import datetime
import smtplib
import os
from email.message import EmailMessage
import random
from . import connection

# Create your views here.

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        out = connection.login(username,password)
        if not out:
            return render(request, 'home.html', {'alertmessage': 'Wrong login, try again'})
        
        else:
            hid,priv = out
            if priv == 'Surgeon':
                return render(request, 'surgerydoc.html')
            elif priv == 'Staff':
                return render(request, 'staff.html')
            elif priv == 'Admin':
                return render(request, 'admin.html')
            else:
                return render(request, 'generaldoc.html')
    return render(request, 'home.html')


def admin(request):
    return render(request, 'admin.html')

def generaldoc(request):
    return render(request, 'generaldoc.html')

def staff(request):
    return render(request, 'staff.html')

def surgerydoc(request):
    return render(request, 'surgerydoc.html')

def add_oproom(request):
    return render(request, 'add_operating_room.html')

def add_doctor(request):

    if request.method == 'POST':
        doctor_type = request.POST.get('doctor_type')
        name = request.POST.get('name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        contact_number = request.POST.get('contact_number')
        department_name = request.POST.get('department_name')
        email_id = request.POST.get('email_id')

        print(doctor_type)
        if doctor_type == 'tertiary_care':
            doctor_type = 'Surgeon'
        else:
            doctor_type = 'General Practitioner'

        a = connection.add_doctors(names=name,
                               username=username,
                               contact=contact_number,
                               department_name=department_name,
                               doctortype=doctor_type,
                               email=email_id,
                               password=password)
        
        if not a:
            return render(request, 'admin.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'admin.html', {'alertmessage': 'Completed process'})
    
    return render(request, 'admin.html')

def add_dept(request):

    if request.method == 'POST':
        dept_id = request.POST['dept_name']

        print(dept_id)

        a = connection.add_department(dept_id)
        if not a:
            return render(request, 'admin.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'admin.html', {'alertmessage': 'Completed process'})

    return render(request, 'admin.html')


def add_oper_room(request):

    if request.method == 'POST':
        dept_name = request.POST['dept_name']
        room_no = request.POST['room_no']

        a = connection.add_operating_room(department_name=dept_name,
                                      room_number=room_no)
        if not a:
            return render(request, 'add_operating_room.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'admin.html', {'alertmessage': 'Completed process'})

    return render(request, 'admin.html')


def add_staff(request):
    if request.method == 'POST':
        name = request.POST['name']
        username = request.POST['username']
        contact = request.POST['contact']
        department_name = request.POST['department_name']
        email = request.POST['email']
        password = request.POST['password']

        a = connection.add_staff(name=name,
                                  username=username,
                                  contact=contact,
                                  deptname=department_name,
                                  email=email,
                                  password=password)

        if not a:
            return render(request, 'admin.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'admin.html', {'alertmessage': 'Completed process'})

    return render(request, 'admin.html')

def adddoc(request):

    return render(request, 'add_doctors.html')

def adddept(request):

    return render(request, 'add_dept.html')

def addstaff(request):

    return render(request, 'add_staff.html')

def manage_doc(request):

    return render(request, 'manage_doctor.html')

def manage_dept(request):

    return render(request, 'manage_dept.html')

def manage_oproom(request):

    return render(request, 'manage_oproom.html')

def manage_staff(request):

    return render(request, 'manage_staff.html')

def manage_inpatient(request):

    return render(request, 'manage_inpatient.html')

def manage_outpatient(request):

    return render(request, 'manage_outpatient.html')

def manage_patient(request):

    return render(request, 'manage_patient.html')

def addpatient(request):
    
    return render(request, 'add_patients.html')

def addoutpatient(request):

    return render(request, 'add_outpatients.html')

def addinpatient(request):

    return render(request, 'add_inpatients.html')

def addtreatment(request):
    
    return render(request, 'add_patient.html')

def add_patient(request):

    if request.method == 'POST':

        pname = request.POST['pname']
        email = request.POST['email']
        contact = request.POST['contact']
        deptname = request.POST['deptname']
        
        a = connection.add_patient(pname=pname,
                                 email=email,
                                 contact=contact,
                                 deptname=deptname)
        if not a:
            return render(request, 'staff.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'staff.html', {'alertmessage': 'Completed process'})

    return render(request, 'staff.html')

def add_outpatient(request):

    if request.method == 'POST':

        pname = request.POST['pname']
        email = request.POST['email']
        admission_date = request.POST['appointment_date']
        assigned_doctor = request.POST['doctor_name']
        doc_email = request.POST['doc_email']
        checkin = request.POST['checkin']


        a = connection.add_outpatient(patient_name=pname,
                                      email=email,
                                      appointment_date=admission_date,
                                      doctor_name=assigned_doctor,
                                      docemail=doc_email,
                                      checkin=checkin)

        if not a:
            return render(request, 'staff.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'staff.html', {'alertmessage': 'Completed process'})

    return render(request, 'staff.html')

def add_inpatient(request):

    if request.method == 'POST':

        pname = request.POST['pname']
        email = request.POST['email']
        admission_date = request.POST['admission_date']
        room_number = request.POST['room_number']
        assigned_doctor = request.POST['assigned_doctor']
        doc_email = request.POST['doc_email']
        discharge_date = request.POST['discharge_date']

        print(pname,email,admission_date,room_number,assigned_doctor,doc_email,discharge_date)

        a = connection.add_inpatient(patient_name=pname,
                                 email=email,
                                 admission_date=admission_date,
                                 room_number=room_number,
                                 assigned_doctor_name=assigned_doctor,
                                 doc_email=doc_email,
                                 discharge_date=discharge_date)
        print(a)
        if not a:
            return render(request, 'staff.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'staff.html', {'alertmessage': 'Completed process'})

    return render(request, 'staff.html')

def add_treatment(request):
    ...

def update_oproom(request):

    if request.method == 'POST':
        oldroom = request.POST['oldno']
        newroom = request.POST['newno']
        department_name = request.POST['deptname']

        a = connection.updateor(old_room_number=oldroom,
                            new_room_number=newroom,
                            department_name=department_name)
        
        if not a:
            return render(request, 'admin.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'admin.html', {'alertmessage': 'Completed process'})

    return render(request, 'admin.html')

def update_staff(request):

    if request.method == 'POST':
        oldmail = request.POST['omail']
        newmail = request.POST['nmail']
        newcontact = request.POST['newcont']
        dept = request.POST['dept']

        a = connection.updatestaff(old_email=oldmail,
                                   new_email=newmail,
                                   new_contact=newcontact,
                                   new_department_name=dept)
        
        if not a:
            return render(request, 'admin.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'admin.html', {'alertmessage': 'Completed process'})

    return render(request, 'admin.html')

def update_doctor(request):

    if request.method == 'POST':
        oldmail = request.POST['omail']
        newmail = request.POST['nmail']
        newcontact = request.POST['newcont']

        a = connection.updatedoc(old_email=oldmail,
                                   new_email=newmail,
                                   new_contact=newcontact)
        
        if not a:
            return render(request, 'admin.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'admin.html', {'alertmessage': 'Completed process'})

    return render(request, 'admin.html')

def updateoproom(request):

    return render(request, 'upd_operateroom.html')

def updatedoctor(request):

    return render(request, 'update_doctor.html')

def updatestaff(request):

    return render(request, 'update_staff.html')

def del_oproom(request):

    if request.method == 'POST':
        room = request.POST['room']
        department_name = request.POST['deptname']

        a = connection.delor(roomno=room,
                            deptname=department_name)
        
        if not a:
            return render(request, 'admin.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'admin.html', {'alertmessage': 'Completed process'})

    return render(request, 'admin.html')

def del_staff(request):

    if request.method == 'POST':
        mail = request.POST['email']
        name = request.POST['name']

        a = connection.delstaff(email=mail,
                                name=name)
        
        if not a:
            return render(request, 'admin.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'admin.html', {'alertmessage': 'Completed process'})

    return render(request, 'admin.html')

def del_dept(request):

    if request.method == 'POST':
        dept = request.POST['dept']

        a = connection.de
        
        if not a:
            return render(request, 'admin.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'admin.html', {'alertmessage': 'Completed process'})

    return render(request, 'admin.html')

def del_doctor(request):

    if request.method == 'POST':
        email = request.POST['Email']
        name = request.POST['Name']

        a = connection.deldoc(email=email,
                                name=name)
        
        if not a:
            return render(request, 'admin.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'admin.html', {'alertmessage': 'Completed process'})

    return render(request, 'admin.html')

def deloproom(request):

    return render(request, 'del_operateroom.html')

def deldoctor(request):

    return render(request, 'delete_doctor.html')

def delstaff(request):

    return render(request, 'delete_staff.html')

def deldept(request):

    return render(request, 'del_department.html')


def view_patient_staff(request):

        patients = connection.viewpat()
        print(patients)
        print(type(patients))
        return render(request, 'view_patient_staff.html', {'patients' : patients})
    

def addtreatd(request):

    return render(request, 'gen_doct_add_tre_det.html')

def add_treatd(request):

    if request.method == 'POST':
        doc_name = request.POST['doc_name']
        name = request.POST['patient_name']
        email = request.POST['email']
        docemail = request.POST['docemail']
        treatment_details = request.POST['treatment_details']
        treatment_date = request.POST['treatment_date']

        print(treatment_date)

        a = connection.add_treatment_details(patient_name=name,
                                         email=email,
                                         doctor_name=doc_name,
                                         docemail=docemail,
                                         treatment_details=treatment_details,
                                         treatment_date=treatment_date
                                         )
        
        if not a:
            return render(request, 'generaldoc.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'generaldoc.html', {'alertmessage': 'Completed process'})

    return render(request, 'generaldoc.html')


# def viewinpatient(request):

#     return render(request, 'view_in_patient.html')

def viewinpatient(request):

    Viewinpatients = connection.viewinpat()
    print(Viewinpatients)
    return render(request, 'view_in_patient.html', {'Viewinpatients': Viewinpatients})

def viewoproom(request):

    operaterooms = connection.viewor()
    print(operaterooms)
    return render(request, 'view_operateroom.html', {'operaterooms': operaterooms})


def viewstaff(request):

    staffs = connection.viewstaff()
    print(staffs)
    return render(request, 'view_staff.html', {'staffs': staffs})

def viewdept(request):

    depts = connection.viewdepartments()
    print(depts)
    return render(request, 'view_dept.html', {'depts': depts})

def viewdoctor(request):

    list_doc = connection.viewdoctor()
    print(list_doc)
    return render(request, 'view_doctor.html', {'list_doc': list_doc})

def viewoutpatient(request):

    outpatients = connection.viewoutpat()
    print(outpatients)
    return render(request, 'out_patient_view.html', {'outpatients': outpatients})

def view_treatmentd(request):

    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']

        Viewtreatmentdets = connection.viewtreatmentdets(name=name,email=email)
        print(Viewtreatmentdets)
        return render(request, 'view_treatmentdet_gen.html', {'Viewtreatmentdets': Viewtreatmentdets})
    
    return render(request, 'generaldoc.html')


def viewtreatmentd(request):

    return render(request, 'patient.html')



def addtreats(request):

    return render(request, 'gen_doct_add_tre_det2.html')

def add_treats(request):

    if request.method == 'POST':
        doc_name = request.POST['doc_name']
        name = request.POST['patient_name']
        email = request.POST['email']
        docemail = request.POST['docemail']
        treatment_details = request.POST['treatment_details']
        treatment_date = request.POST['treatment_date']

        print(treatment_date)

        a = connection.add_treatment_details(patient_name=name,
                                         email=email,
                                         doctor_name=doc_name,
                                         docemail=docemail,
                                         treatment_details=treatment_details,
                                         treatment_date=treatment_date
                                         )
        
        if not a:
            return render(request, 'surgerydoc.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'surgerydoc.html', {'alertmessage': 'Completed process'})

    return render(request, 'surgerydoc.html')

def view_treatments(request):

    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']

        Viewtreatmentdets = connection.viewtreatmentdets(name=name,email=email)
        print(Viewtreatmentdets)
        return render(request, 'view_treatmentdet_gen2.html', {'Viewtreatmentdets': Viewtreatmentdets})
    
    return render(request, 'surgerydoc.html')


def viewtreatments(request):

    return render(request, 'patient2.html')

def view_surgery(request):

    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']

        doctors = connection.viewcurrentsurgery(docname=name,email=email)
        print(doctors)
        return render(request, 'view_surgery.html', {'doctors': doctors})
    
    return render(request, 'surgerydoc.html')

def viewsurgery(request):

    return render(request, 'doc_input.html')

def add_surgery(request):

    if request.method == 'POST':

        name = request.POST['doc_name']
        p_name = request.POST['pat_name']
        email = request.POST['email']
        room_no = request.POST['room_no']
        surgery_date = request.POST['surgery_date']
        doc_email = request.POST['doc_email']
        surgery_name = request.POST['surgery_name']

        a = connection.add_surgery(patient_name=p_name,
                                   email=email,
                                   doctor_name=name,
                                   docemail=doc_email,
                                   room_number=room_no,
                                   surgery_date=surgery_date,
                                   surgeryname=surgery_name)

        if not a:
            return render(request, 'surgerydoc.html', {'alertmessage': 'Incorrect information, please try again'})
        else:
            return render(request, 'surgerydoc.html', {'alertmessage': 'Completed process'})

    return render(request, 'surgerydoc.html')

def addsurgery(request):

    return render(request, 'add_surgery.html')

