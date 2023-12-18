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

def add_patient(request):
    
    return render(request, 'add_patient.html')

def add_outpatient(request):

    return render(request, 'add_outpatient.html')

def add_inpatient(request):

    return render(request, 'add_inpatient.html')

def addpatient(request):

    ...

def addoutpatient(request):

    ...

def addinpatient(request):

    ...


