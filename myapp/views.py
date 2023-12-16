from django.shortcuts import render
from django.http import HttpResponse
import csv
import datetime
import smtplib
import os
from email.message import EmailMessage
import random


# Create your views here.

def home(request):
    return render(request, 'home.html')

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         # Read the register.csv file
#         with open('register.csv', 'r') as csvfile:
#             reader = csv.reader(csvfile)
#             for row in reader:

#                 stored_username = row[3]
#                 stored_password = row[4]

#                 if username == stored_username:
#                     if password == stored_password:
#                         with open('logs.csv', 'a') as logs:
#                             write = csv.writer(logs)
#                             date_time = datetime.datetime.now()

#                             current_time = date_time.time()
#                             current_date = date_time.date()

#                             write.writerow([username, current_date, current_time])

#                             global CURRENT_USER, CURRENT_PRIV
#                             CURRENT_USER = username

#                         if row[-1] == "admin":
#                             CURRENT_PRIV = "admin"
#                             return render(request, "admin.html")
#                         elif row[-1] == "mentor":
#                             CURRENT_PRIV = "mentor"
#                             return render(request, "mentor.html")
#                         elif row[-1] == "mentee":
#                             CURRENT_PRIV = "mentee"
#                             return render(request, "mentee.html")
#                     else:
#                         return render(request, 'home.html', {'alertmessage': 'Wrong password'})  # Display wrong password message

#             return render(request, 'home.html', {'alertmessage': 'Username not found'})  # Display username not found message

#     return render(request, 'home.html')

def login(request):
    ...

def admin(request):
    return render(request, 'admin.html')

def generaldoc(request):
    return render(request, 'generaldoc.html')

def magoptroom(request):
    return render(request, 'magoptroom.html')

def staff(request):
    return render(request, 'staff.html')

def surgerydoc(request):
    return render(request, 'surgerydoc.html')

