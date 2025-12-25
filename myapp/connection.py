import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r'C:\oraclexe\app\oracle\product\11.2.0\server\bin')

connection_string = "dbmsthird/test@localhost:1521/XE"

connection = cx_Oracle.connect(connection_string)
from datetime import datetime

'''
ADD operations 
done by admin 
-add department,
-add operating rooms,
-add docters,
-add staffs
'''
def add_department(department_name):
    try:
        cursor=connection.cursor()
        cursor.execute("SELECT departmentseq.nextval FROM dual")
        department_id = 'D' + str(cursor.fetchone()[0])

        # Insert data into the Departments table
        cursor.execute("INSERT INTO Departments VALUES (:deparment_id, :department_name)", (department_id, department_name))
        cursor.close()
        # Commit the transaction
        connection.commit()

        print(f"Department '{department_name}' with ID '{department_id}' added successfully.")
        return True
    except:
        return False

def add_operating_room(department_name, room_number):
    try:
        cursor = connection.cursor()

        # Look up the Department ID based on the provided Department Name
        cursor.execute("SELECT DepartmentID FROM Departments WHERE DepartmentName = :department_name", department_name=department_name)
        department_id = cursor.fetchone()

        if not department_id:
            return False

        # Get the next value from the OperatingRoomSeq
        cursor.execute("SELECT OperatingRoomSeq.NEXTVAL FROM DUAL")
        room_id ='OR'+ str(cursor.fetchone()[0])

        # Insert into OperatingRooms table
        cursor.execute("""
            INSERT INTO OperatingRooms (RoomID, RoomNumber, DepartmentID)
            VALUES (:id, :room_number, :department_id)
        """, id=room_id, room_number=room_number, department_id=department_id[0])

        cursor.close()
        connection.commit()
        return True
    except:
        return False

def add_doctors(names,username,password,contact,department_name,doctortype,email):
    try:
        cursor=connection.cursor()
        # Generate the next value for userseq and docterseq
        cursor.execute("SELECT userseq.nextval, docterseq.nextval FROM dual")
        user_id, doctor_id = cursor.fetchone()
        # Insert data into the Users table
        user_id='U'+str(user_id)
        cursor.execute("""
            INSERT INTO Users (UserID, Username, Passwords, Roles)
            VALUES (:user_id, :username, :password, :roles)
        """, user_id=user_id, username=username, password=password,roles='Doctor')  
        connection.commit()# Ensure roles is not longer than 20 characters
        # Look up the Department ID based on the provided Department Name
        cursor.execute("SELECT DepartmentID FROM Departments WHERE DepartmentName = :department_name", department_name=department_name)
        department_id =cursor.fetchone()
        if not department_id:
            raise ValueError(f"Department '{department_name}' not found.")
        doctor_id='DOC'+str(doctor_id)
        # Insert data into the Doctors table
        print(doctor_id,user_id,department_id)
        cursor.execute("""
            INSERT INTO Doctors (DoctorID, Names, ContactNumber, DepartmentID, DoctorType, Email, loginID)
            VALUES (:doctor_id, :names, :contact, :department_id, :doctortype, :email, :user_id)
        """, doctor_id=doctor_id, names=names, contact=contact, department_id=department_id[0],
           doctortype=doctortype, email=email, user_id=user_id)
        cursor.close()
        connection.commit()
        
        print(f"Doctor '{username}' added successfully.")
        return True
    except:
        return False

def add_staff(name,contact,deptname,email,username,password):
    try:
        cursor=connection.cursor()
        # Generate the next value for userseq and docterseq
        cursor.execute("SELECT userseq.nextval, staffseq.nextval FROM dual")
        user_id, staff_id = cursor.fetchone()
        # Insert data into the Users table
        user_id='U'+str(user_id)
        cursor.execute("""
            INSERT INTO Users (UserID, Username, Passwords, Roles)
            VALUES (:user_id, :username, :password, :roles)
        """, user_id=user_id, username=username, password=password,roles='Staff')  
        connection.commit()# Ensure roles is not longer than 20 characters
        
        # Look up the Department ID based on the provided Department Name
        cursor.execute("SELECT DepartmentID FROM Departments WHERE DepartmentName = :department_name", department_name=deptname)
        department_id =cursor.fetchone()

        if not department_id:
            raise ValueError(f"Department '{deptname}' not found.")
        staff_id='S'+str(staff_id)
        # Insert data into the Doctors table
        cursor.execute("""
            INSERT INTO Staff (staffID, Names, ContactNumber, DepartmentID,Email, loginID)
            VALUES (:staff_id, :names, :contact, :department_id,:email, :user_id)
        """, staff_id=staff_id, names=name, contact=contact, department_id=department_id[0],
           email=email, user_id=user_id)
        cursor.close()
        connection.commit()
        
        print(f"Staff '{username}' added successfully.")
        return True
    except:
        return False

def login(username,password):
    try:
        cursor=connection.cursor()

        cursor.execute('select UserID,roles from users where username=:username and passwords=:password',username=username,password=password)

        UserID,roles=cursor.fetchone()

        if roles=='Doctor':
            cursor.execute('Select DoctorType from Doctors where Loginid=:UserID',UserID=UserID)
            doctertype=cursor.fetchone()
            cursor.close()
            return UserID,doctertype[0]
        cursor.close()
        return UserID,roles
        return True
    except:
        return False
'''
ADD operations 
done by staff
-add patient
-add Inpatients,
-add Outpatients
'''
def add_patient(pname,contact,deptname,email):
    try:
        cursor = connection.cursor()

        # Look up the Department ID based on the provided Department Name
        cursor.execute("SELECT DepartmentID FROM Departments WHERE DepartmentName = :department_name", department_name=deptname)
        department_id = cursor.fetchone()

        if not department_id:
            return False

        # Get the next value from the OperatingRoomSeq
        cursor.execute("SELECT patientseq.NEXTVAL FROM DUAL")
        patient_id ='P'+ str(cursor.fetchone()[0])

        cursor.callproc('addpatient',(patient_id,pname,contact,department_id[0],email))
        cursor.close()
        connection.commit()
        print('patient successfully added')
        return True
    except:
        return False


def add_inpatient(patient_name,email,admission_date, room_number, assigned_doctor_name,doc_email, discharge_date):
    try:
        cursor = connection.cursor()

        # Get the next value from the InpatientSeq
        cursor.execute("SELECT inpatientseq.NEXTVAL FROM DUAL")
        inpatient_id = 'IP' + str(cursor.fetchone()[0])

        cursor.execute("SELECT patientID from patients where names=:patient_name and email=:email", patient_name=patient_name,email=email)
        patient_id = cursor.fetchone()
        print(1)
        if not patient_id:
            return False

        # Look up the Doctor ID based on the provided Doctor Name
        cursor.execute("SELECT DoctorID FROM Doctors WHERE Names = :doctor_name and email=:dremail", doctor_name=assigned_doctor_name,dremail=doc_email)
        doctor_id = cursor.fetchone()
        print(2)
        if not doctor_id:
            return False

        print(3)
        # Insert into Inpatients table with bind variables
        cursor.execute("""
            INSERT INTO Inpatients (InpatientID, PatientID, AdmissionDate, RoomNumber, AssignedDoctorID, DischargeDate)
            VALUES (:inpatient_id, :patient_id,TO_DATE(:admission_date,'YYYY-MM-DD'), :room_number, :doctor_id,TO_DATE(:discharge_date,'YYYY-MM-DD'))
        """, inpatient_id=inpatient_id, patient_id=patient_id[0], admission_date=admission_date,
        room_number=room_number, doctor_id=doctor_id[0], discharge_date=discharge_date)

        cursor.close()
        connection.commit()

        print('inpatient added successfully')
        return True
    except:
        return False

def add_outpatient(patient_name,email,appointment_date, doctor_name,docemail,checkin):
    try:
        cursor = connection.cursor()

        # Get the next value from the OutpatientSeq
        cursor.execute("SELECT outpatientseq.NEXTVAL FROM DUAL")
        outpatient_id = 'OP' + str(cursor.fetchone()[0])

        cursor.execute("SELECT patientID from patients where names=:patient_name and Email=:email",patient_name=patient_name,email=email)
        patient_id=cursor.fetchone()

        # Look up the Doctor ID based on the provided Doctor Name
        cursor.execute("SELECT DoctorID FROM Doctors WHERE Names = :doctor_name and email=:email", doctor_name=doctor_name,email=docemail)
        doctor_id = cursor.fetchone()

        if not doctor_id:
            return False

        # Insert into Outpatients table
        cursor.execute("""
            INSERT INTO Outpatients (OutpatientID, PatientID, AppointmentDate, DoctorID,Checkin)
            VALUES (:outpatient_id, :patient_id, TO_DATE(:appointment_date,'YYYY-MM-DD'), :doctor_id,TO_TIMESTAMP(:checkin,'HH24:MI'))
        """, outpatient_id=outpatient_id, patient_id=patient_id[0], appointment_date=appointment_date, doctor_id=doctor_id[0],checkin=checkin)

        cursor.close()
        connection.commit()

        print(f'Outpatient "{patient_name}" added successfully.')
        return True
    except:
        return False
'''
ADD OPERATIONS 
BY GENERAL PRACTIONER
-ADD TREATMENT DETAILS
-BOOK APPOINTMENT
BY SURGEON
-ADD TREATMENT DETAILS
-SCHEDULE SURGERY
'''

def add_treatment_details(patient_name,email, doctor_name,docemail, treatment_details, treatment_date):
    try:
        cursor = connection.cursor()

        # Look up the Patient ID based on the provided Patient Name
        cursor.execute("SELECT PatientID FROM Patients WHERE Names = :patient_name and email=:email", patient_name=patient_name,email=email)
        patient_id = cursor.fetchone()

        print(1)

        if not patient_id:
            return False

        # Look up the Doctor ID based on the provided Doctor Name
        cursor.execute("SELECT DoctorID FROM Doctors WHERE Names = :doctor_name and email=:docemail", doctor_name=doctor_name,docemail=docemail)
        doctor_id = cursor.fetchone()

        print(1)
        if not doctor_id:
            return False

        # Get the next value from the TreatmentDetailsSeq
        cursor.execute("SELECT treatmenthistoryseq.NEXTVAL FROM DUAL")
        treatment_details_id = 'TD' + str(cursor.fetchone()[0])

        # Insert into TreatmentDetails table
        cursor.execute("""
            INSERT INTO Treatmenthistory (TreatmentHistoryID, PatientID, DoctorID, TreatmentDetails, TreatmentDate)
            VALUES (:treatment_details_id, :patient_id, :doctor_id, :treatment_details, TO_DATE(:treatment_date, 'YYYY-MM-DD'))
        """, treatment_details_id=treatment_details_id, patient_id=patient_id[0],
        doctor_id=doctor_id[0], treatment_details=treatment_details, treatment_date=treatment_date)

        cursor.close()
        connection.commit()

        print('Treatment details added successfully.')
        return True
    except:
        return False

def add_appointment(patient_name, email,doctor_name,docemail, appointment_date, appointment_time):
    try:
        cursor = connection.cursor()

        # Look up the Patient ID based on the provided Patient Name
        cursor.execute("SELECT PatientID FROM Patients WHERE Names = :patient_name and email=:email", patient_name=patient_name,email=email)
        patient_id = cursor.fetchone()
        if not patient_id:
            return False

        # Look up the Doctor ID based on the provided Doctor Name
        cursor.execute("SELECT DoctorID FROM Doctors WHERE Names = :doctor_name and email=:docemail", doctor_name=doctor_name,docemail=docemail)
        doctor_id = cursor.fetchone()

        if not doctor_id:
            return False

        # Get the next value from the AppointmentSeq
        cursor.execute("SELECT appointmentseq.NEXTVAL FROM DUAL")
        appointment_id = 'A' + str(cursor.fetchone()[0])

        # Insert into Appointments table
        cursor.execute("""
            INSERT INTO appointments (AppointmentID, DoctorID, PatientID, AppointmentDate, AppointmentTime)
            VALUES (:appointment_id, :doctor_id, :patient_id, TO_DATE(:appointment_date, 'YYYY-MM-DD'), TO_TIMESTAMP(:appointment_time, 'HH24:MI'))
        """, appointment_id=appointment_id, patient_id=patient_id[0], doctor_id=doctor_id[0],
        appointment_date=appointment_date, appointment_time=appointment_time)

        cursor.close()
        connection.commit()

        print('Appointment added successfully.')
        return True
    except:
        return False

def add_surgery(patient_name,email,doctor_name,docemail, room_number, surgery_date, surgeryname):
    
            cursor = connection.cursor()

            # Look up the Doctor ID based on the provided Doctor Name
            cursor.execute("SELECT DoctorID FROM Doctors WHERE Names = :doctor_name and email=:docemail", doctor_name=doctor_name,docemail=docemail)
            doctor_id = cursor.fetchone()
            print(doctor_id)
            cursor.execute("SELECT PatientID FROM patients WHERE Names = :patient_name and email=:email", patient_name=patient_name,email=email)
            patient_id = cursor.fetchone()

            if not doctor_id:
                return False

            # Look up the Room ID based on the provided Room Number
            cursor.execute("SELECT RoomID FROM OperatingRooms WHERE RoomNumber = :room_number", room_number=room_number)
            room_id = cursor.fetchone()
            print(room_id)
            if not room_id:
                return False

            # Get the next value from the SurgerySeq
            cursor.execute("SELECT surgeryseq.NEXTVAL FROM DUAL")
            surgery_id = 'S' + str(cursor.fetchone()[0])

            # Insert into Surgeries table
            cursor.execute("""
                INSERT INTO Surgeries (SurgeryID,PatientID, DoctorID, RoomID, SurgeryDate, Surgeryname)
                VALUES (:surgery_id,:patientid, :doctor_id, :room_id, TO_DATE(:surgery_date, 'YYYY-MM-DD'), :surgeryname)
            """, surgery_id=surgery_id,patientid=patient_id[0],doctor_id=doctor_id[0], room_id=room_id[0], surgery_date=surgery_date, surgeryname=surgeryname)

            cursor.close()
            connection.commit()

            print('Surgery added successfully.')
            return True


'''
VIEW OPERATIONS BY ADMIN
-VIEW STAFF
-VIEW DOCTORS
-VIEW OPERATING ROOMS
-VIEW DEPARTMENTS
'''

def viewstaff():
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Names, contactnumber, departmentid, email 
            FROM STAFF
        """)
        rows = cursor.fetchall()

        staff_list = []
        for row in rows:
            cursor.execute('SELECT departmentname FROM departments WHERE departmentid=:depid', depid=row[2])
            department_name = cursor.fetchone()

            staff_details = {
                'name': row[0],
                'contact': row[1],
                'department': department_name[0] if department_name else None,
                'email': row[3]
            }

            staff_list.append(staff_details)
        cursor.close()
        return staff_list
    except:
        return False
def viewdoctor():
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Names, contactnumber, departmentid, email,DoctorType 
            FROM DOCTORS
        """)
        rows = cursor.fetchall()

        doctor_list = []
        for row in rows:
            cursor.execute('SELECT departmentname FROM departments WHERE departmentid=:depid', depid=row[2])
            department_name = cursor.fetchone()
            flag=True
            if row[4]=='General Practitioner':
                flag=True
            else:
                flag=False
            doctor_details = {
                'name': row[0],
                'contact': row[1],
                'department': department_name[0] if department_name else None,
                'email': row[3],
                'doctype':'primary care/secondary care' if flag==True else 'Tertiary Care'
            }

            doctor_list.append(doctor_details)
        cursor.close()
        return doctor_list
    except:
        return False

def viewdepartments():
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT departmentname
            FROM departments
        """)
        rows = cursor.fetchall()

        dept_list = []
        for row in rows:
            depts = {'dept_avail' : row[0]}
            dept_list.append(depts)
        cursor.close()
        return dept_list
    except:
        return False
def viewor():
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT roomnumber, departmentid 
            FROM operatingrooms
        """)
        rows = cursor.fetchall()

        or_list = []
        for row in rows:
            cursor.execute('SELECT departmentname FROM departments WHERE departmentid=:depid', depid=row[1])
            department_name = cursor.fetchone()

            or_dets = {
                'room_number': row[0],
                'department': department_name[0] if department_name else None
            }

            or_list.append(or_dets)
        cursor.close()
        return or_list
    except:
        return False
'''
DELETE OPERATIONS IN 
ADMIN 
-DELETE OR
-DELETE STAFF
-DELETE DEPARTMENTS
-DELETE DOCTORS
'''
def delor(roomno,deptname):
    try:
        cursor=connection.cursor()
        cursor.execute('select departmentid from departments where departmentname=:deptname',deptname=deptname)
        dept_id=cursor.fetchone()
        cursor.execute("""
        DELETE FROM operatingrooms
        where departmentid=:deptid and roomnumber=:roomno """,deptid=dept_id[0],roomno=roomno)
        connection.commit()
        cursor.close()
        return True
    except:
        return False

def delstaff(name,email):
    try:
        cursor=connection.cursor()
        cursor.execute("""
        SELECT loginID FROM STAFF
        where names=:name and email=:email""",name=name,email=email)
        userid=cursor.fetchone()
        print(userid)
        cursor.execute("""
        DELETE FROM USERS 
        WHERE userid=:userid""",userid=userid[0])
        print('deleted user')
        connection.commit()
        cursor.close()
        return True
    except:
        return False

def deldoc(name,email):
    try:
        cursor=connection.cursor()
        cursor.execute("""
        SELECT loginID FROM DOCTORS
        where names=:name and email=:email""",name=name,email=email)
        userid=cursor.fetchone()
        cursor.execute("""
        DELETE FROM USERS 
        WHERE userid=:userid""",userid=userid[0])
        connection.commit()
        cursor.close()
        return True
    except:
        return False
'''
UPDATE OPERATIONS
BY ADMIN
-update or
-update staff
-update doctors
'''
def updateor(old_room_number, new_room_number, department_name):
    try:
        cursor = connection.cursor()

        # Look up the Department ID based on the provided Department Name
        cursor.execute("SELECT DepartmentID FROM Departments WHERE DepartmentName = :department_name", department_name=department_name)
        department_id = cursor.fetchone()

        if not department_id:
            return False

        # Update OperatingRooms table
        cursor.execute("""
            UPDATE OperatingRooms
            SET RoomNumber = :new_room_number
            WHERE RoomNumber = :old_room_number AND DepartmentID = :department_id
        """, new_room_number=new_room_number, old_room_number=old_room_number, department_id=department_id[0])

        cursor.close()
        connection.commit()

        print(f"Operating room '{old_room_number}' updated to '{new_room_number}' successfully.")
        return True
    except:
        return False

    
def updatestaff(old_email, new_email,new_contact, new_department_name):
    try:
        cursor = connection.cursor()

        # Look up the Department ID based on the provided Department Name
        cursor.execute("SELECT DepartmentID FROM Departments WHERE DepartmentName = :department_name", department_name=new_department_name)
        department_id = cursor.fetchone()

        if not department_id:
            return False

        # Update Staff table
        cursor.execute("""
            UPDATE Staff
            SET ContactNumber = :new_contact,
                DepartmentID = :department_id,
                Email = :new_email
            WHERE Email = :old_email
        """, new_contact=new_contact, department_id=department_id[0], new_email=new_email,
        old_email=old_email)

        cursor.close()
        connection.commit()

        print(f"Staff updated successfully.")
        return True
    except:
        return False

def updatedoc(old_email,new_email,new_contact):
    try:
        cursor = connection.cursor()
        # Update Doctors table
        cursor.execute("""
            UPDATE Doctors
            SET ContactNumber = :new_contact,
                Email = :new_email
            WHERE Email = :old_email
        """,new_contact=new_contact,
        new_email=new_email, old_email=old_email)


        cursor.close()
        connection.commit()

        print(f"Doctor updated successfully.")
        return True
    except:
        return False

'''
VIEW-STAFFS
-VIEW PATIENTS
-VIEW INPATIENTS
-VIEW OUTPATIENTS
'''

def viewpat():
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT Names, contactnumber, departmentid, email 
            FROM PATIENTS
        """)
        rows = cursor.fetchall()

        pat_list = []
        for row in rows:
            cursor.execute('SELECT departmentname FROM departments WHERE departmentid=:depid', depid=row[2])
            department_name = cursor.fetchone()
            pat_details = {
                'name': row[0],
                'contact': row[1],
                'department': department_name[0] if department_name else None,
                'email': row[3]
            }

            pat_list.append(pat_details)
        cursor.close()
        return pat_list
    except:
        return False


def viewinpat():
    try:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT PatientID,AdmissionDate,RoomNumber,AssignedDoctorID,DischargeDate
            FROM Inpatients
        """)
        rows = cursor.fetchall()

        inpat_list = []
        for row in rows:
            cursor.execute('SELECT names FROM patients WHERE patientid=:patientid',patientid=row[0])
            patient_name = cursor.fetchone()
            cursor.execute('SELECT Names FROM Doctors WHERE doctorID=:doctorID',doctorid=row[3])
            doctor_name=cursor.fetchone()
            adm_date=row[1].strftime("%Y-%m-%d")
            dis_date=row[1].strftime("%Y-%m-%d")
            inpat_details = {
                'patient_name': patient_name[0],
                'admission_date': adm_date,
                'room_number':row[2],
                'doctor_name':doctor_name[0],
                'Discharge_date':dis_date
            }

            inpat_list.append(inpat_details)
        cursor.close()
        return inpat_list
    except:
        return False

def viewoutpat():
        cursor = connection.cursor()
        cursor.execute("""
            SELECT PatientID,AppointmentDate,DoctorID,Checkin
            FROM Outpatients
        """)
        rows = cursor.fetchall()

        outpat_list = []
        for row in rows:
            cursor.execute('SELECT names FROM patients WHERE patientid=:patientid',patientid=row[0])
            patient_name = cursor.fetchone()
            cursor.execute('SELECT Names FROM Doctors WHERE doctorID=:doctorID',doctorid=row[2])
            doctor_name=cursor.fetchone()
            app_date=row[1]
            datestring=app_date.strftime("%Y-%m-%d")
            inpat_details = {
                'name': patient_name[0],
                'appointment_date': datestring,
                'doc_name':doctor_name[0],
                'checkin_date':row[3],
            }
            outpat_list.append(inpat_details)
        cursor.close()
        return outpat_list
    
    
def viewtreatmentdets(name,email): 
    try:
        cursor = connection.cursor()
        cursor.execute("""
                       SELECT PatientID from Patients where Names=:name and email=:email
                       """,name=name,email=email)
        patient_id=cursor.fetchone()
        cursor.execute("""
            SELECT TreatmentDetails,TreatmentDate
            FROM TreatmentHistory where patientid=:patid
        """,patid=patient_id[0])
        rows = cursor.fetchall()
        treat_list = []
        for row in rows:
            treatmentobj=row[1]
            datestring=treatmentobj.strftime("%Y-%m-%d")
            treat_details = {
                'TreatmentDetails': row[0],
                'TreatmentDate': datestring
            }

            treat_list.append(treat_details)
        cursor.close()
        return treat_list
    except:
        return False

def viewcurrentappointment(docname,email):
    try:
        cursor = connection.cursor()

        # Get today's date
        today_date = datetime.now().date()
        cursor.execute("""
            SELECT doctorID FROM doctors where names=:doctorname
            and email=:email
            """,doctorname=docname,email=email)
        doc_id=cursor.fetchone()[0]
        # Execute the query to get today's appointments
        cursor.execute("""
            SELECT PatientID, AppointmentTime FROM Appointments WHERE AppointmentDate = :today_date and doctorID=:doctorid
        """, today_date=today_date,doctorid=doc_id)

        rows = cursor.fetchall()

        app_list = []
        for row in rows:
            # Fetch patient name for the given patient ID
            cursor.execute('SELECT names FROM patients WHERE patientid = :patientid', {'patientid': row[0]})
            patient_name = cursor.fetchone()
            app_time=row[1].strftime("%H:%M")
            app_details = {
                'patient name': patient_name[0] if patient_name else 'Unknown',  # Handle the case where patient_name is None
                'Appointment Time': app_time
            }

            app_list.append(app_details)

        cursor.close()

        # Return the list of today's appointments
        return app_list
    except:
        return False

def viewcurrentsurgery(docname,email):
    try:
        cursor = connection.cursor()

        # Get today's date
        today_date = datetime.now().date()
        cursor.execute("""
            SELECT doctorID FROM doctors where names=:doctorname
            and email=:email
            """,doctorname=docname,email=email)
        doc_id=cursor.fetchone()[0]
        print(doc_id)
        # Execute the query to get today's appointments
        cursor.execute("""
            SELECT PatientID,Surgeryname,RoomID FROM Surgeries WHERE SurgeryDate = :today_date and doctorID=:doctorid
        """, today_date=today_date,doctorid=doc_id)

        rows = cursor.fetchall()

        sur_list = []
        for row in rows:

            print(0)
            # Fetch patient name for the given patient ID
            cursor.execute('SELECT names FROM patients WHERE patientid = :patientid', {'patientid': row[0]})
            patient_name = cursor.fetchone()
            cursor.execute('SELECT RoomNumber FROM operatingrooms WHERE roomid =:roomid', {'roomid': row[2]})
            room_number = cursor.fetchone()
            sur_details = {
                'patient_name': patient_name[0] if patient_name else 'Unknown',  # Handle the case where patient_name is None
                'room_number': room_number[0],
                'surgery_name':row[1]
            }

            sur_list.append(sur_details)
            sur_list.append(1)

        cursor.close()

        # Return the list of today's appointments
        return sur_list
    except:
        return False
    

    

# Example Usage
if __name__ == '__main__':
    print('\n')
    print('ADDING DETAILS')
  
    add_department('cardio')
    add_department('opthomology')
    add_department('gynac')
    add_operating_room('cardio', 'R1')
    add_operating_room('opthomology', 'R2')
    add_doctors('siva','siva5122','aa164@#','9940025247','cardio','Surgeon','siva@gmail.com')
    add_doctors('john doe','jd22233','ppm132','889231234','gynac','General Practitioner','johndoe@gmail.com')
    add_staff('sam','9934578724','opthomology','sam@gmail.com','sam641','pdk164@#')
    add_staff('sudhan','8934142232','gynac','sudhan@gmail.com','sudhan561','abc@#$')
    print(login('siva5122','aa164@#'))
    print(login('sam641','pdk164@#'))
    #adding a patient
    add_patient('pranav','99417382','cardio','pranaav@gmail.com')
 
    add_patient('paran', '8945678920', 'cardio', 'paran@gmail.com')
   
    
    add_treatment_details('paran', 'paran@gmail.com','siva','siva@gmail.com', 'Routine checkup', '2024-01-10')
    #add_appointment('paran','paran@gmail.com', 'siva','siva@gmail.com', '2023-12-19', '20:00')
    add_surgery('paran','paran@gmail.com','siva','siva@gmail.com', 'R2', '2023-12-22','appendicitis')

    add_treatment_details('pranav','pranaav@gmail.com','siva','siva@gmail.com' ,'Prescription for flu', '2024-02-10')

    
    add_outpatient('paran','paran@gmail.com', '2024-01-22', 'siva','siva@gmail.com','13:20')
    #to check doctor availablity u can use this
    #add_outpatient('pranav','pranaav@gmail.com', '2024-01-25', 'siva','siva@gmail.com','13:20')
    add_inpatient('pranav','pranaav@gmail.com', '2023-12-22', 'R1','siva','siva@gmail.com','2024-01-30')
    print('\n')
    print('VIEW IN ADMIN PAGE')

    print(viewstaff())
    print(viewdoctor())
    print(viewdepartments())
    print(viewor())
    print('\n')
    print('DELETE IN ADMIN PAGE')
 
    #delete operations
    delor('R1','cardio')
    delstaff('sudhan','sudhan@gmail.com')
    deldoc('john doe','johndoe@gmail.com')
    print('\n')
    print('VIEWS IN ADMIN PAGE AFTER DELETING TO CHECK IF DETAILS HAVE BEEN SUCCESSFULLY DELETED')

    print(viewstaff())
    print(viewdoctor())
    print(viewdepartments())
    print(viewor())
    print('\n')
    print('UPDATES IN ADMIN PAGE')

    #update operations
    updateor('R2','R3','opthomology')
    print(viewor())
    print(viewdepartments())
    # Update Operating Room
    updateor('R2', 'R3', 'opthomology')
    print(viewor())
    # Update Doctor
    updatedoc('siva@gmail.com', 'siva_updated@gmail.com','9876543220',)
    print(viewdoctor())
    # Update Staff
    updatestaff('sam@gmail.com','samupdated@gmail.com', '9876543220', 'gynac')
    print('\n')
    print('VIEWS BY STAFF')
    print(viewstaff())       
    print(viewpat())
    print(viewinpat())
    print('\n')
    print('VIEWING TREATMENT DETAILS:')
    
    print(viewtreatmentdets('pranav','pranaav@gmail.com'))
    print('\n')
    print('VIEWING APPOINTMENT-general practitioner')
 
    print(viewcurrentappointment('siva','siva_updated@gmail.com'))
    print('\n')
    print('VIEWING SUERGERY-SURGEONS')
    
    print(viewcurrentsurgery('siva','siva_updated@gmail.com'))
    
    add_doctors('john doe','jd22233','ppm132','889231234','gynac','General Practitioner','johndoe@gmail.com')
    add_patient('rakirakirai','8949676','cardio','t@g.c')

    add_inpatient('rakirakirai','t@g.c','2023-12-22','fc2','john doe','johndoe@gmail.com','2024-01-22')
    print(viewinpat())

    a = add_inpatient('test', 'trialmail@g.c', '2023-12-22', 'f123', 'john doe', 'johndoe@gmail.com' ,'2035-07-25')
    print(a)

    add_doctors('pranesh','pdk164','1234','889231234','cardio','Surgeon','tigcock@gmail.com')
    add_surgery('paran','paran@gmail.com','pranesh','tigcock@gmail.com','R3','2023-12-22','lalla')
    print(viewcurrentsurgery('pranesh','tigcock@gmail.com'))
    delor('R10','cardio')