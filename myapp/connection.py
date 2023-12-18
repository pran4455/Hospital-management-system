import cx_Oracle

cx_Oracle.init_oracle_client(lib_dir=r'C:\oraclexe\app\oracle\product\11.2.0\server\bin')

connection_string = "dbmsthird/test@localhost:1521/XE"

connection = cx_Oracle.connect(connection_string)

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
        print(user_id,doctor_id)
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
        print(user_id,staff_id)
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
    cursor=connection.cursor()

    cursor.execute('select UserID,roles from users where username=:username and passwords=:password',username=username,password=password)

    try:
        UserID,roles=cursor.fetchone()

        if roles=='Doctor':
            cursor.execute('Select DoctorType from Doctors where Loginid=:UserID',UserID=UserID)
            doctertype=cursor.fetchone()
            cursor.close()
            return UserID,doctertype[0]
        cursor.close()
        return UserID,roles

    except:
         return False

'''
ADD operations 
done by staff
-add patient
-add treatmentHistory,
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

        # Insert into OperatingRooms table
        cursor.execute("""
            INSERT INTO patients (patientid, names, contactnumber,departmentid,email)
            VALUES (:id, :names, :contact,:deptid,:email)
        """, id=patient_id, names=pname,contact=contact, deptid=department_id[0],email=email)

        cursor.close()
        connection.commit()
        print('patient successfully added')
        return True
    
    except:
        return False


def add_inpatient(patient_name,email,admission_date, room_number, assigned_doctor_name,doc_email, discharge_date):
    cursor = connection.cursor()

    # Get the next value from the InpatientSeq
    cursor.execute("SELECT inpatientseq.NEXTVAL FROM DUAL")
    inpatient_id = 'IP' + str(cursor.fetchone()[0])

    cursor.execute("SELECT patientID from patients where names=:patient_name and email=:email", patient_name=patient_name,email=email)
    patient_id = cursor.fetchone()
    if not patient_id:
        return False

    # Look up the Doctor ID based on the provided Doctor Name
    cursor.execute("SELECT DoctorID FROM Doctors WHERE Names = :doctor_name and email=:dremail", doctor_name=assigned_doctor_name,dremail=doc_email)
    doctor_id = cursor.fetchone()

    if not doctor_id:
        return False

    # Insert into Inpatients table with bind variables
    cursor.execute("""
        INSERT INTO Inpatients (InpatientID, PatientID, AdmissionDate, RoomNumber, AssignedDoctorID, DischargeDate)
        VALUES (:inpatient_id, :patient_id,TO_DATE(:admission_date,'YYYY-MM-DD'), :room_number, :doctor_id,TO_DATE(:discharge_date,'YYYY-MM-DD'))
    """, inpatient_id=inpatient_id, patient_id=patient_id[0], admission_date=admission_date,
       room_number=room_number, doctor_id=doctor_id[0], discharge_date=discharge_date)

    cursor.close()
    connection.commit()

    print('inpatient added successfully')

def add_outpatient(patient_name,email,appointment_date, doctor_name,docemail,checkin,checkout):
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
        INSERT INTO Outpatients (OutpatientID, PatientID, AppointmentDate, DoctorID,Checkin,Checkout)
        VALUES (:outpatient_id, :patient_id, TO_DATE(:appointment_date,'YYYY-MM-DD'), :doctor_id,TO_TIMESTAMP(:checkin,'HH24:MI'),TO_TIMESTAMP(:checkout,'HH24:MI'))
    """, outpatient_id=outpatient_id, patient_id=patient_id[0], appointment_date=appointment_date, doctor_id=doctor_id[0],checkin=checkin,checkout=checkout)

    cursor.close()
    connection.commit()

    print(f'Outpatient "{patient_name}" added successfully.')
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

def add_appointment(patient_name, email,doctor_name,docemail, appointment_date, appointment_time):
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

def add_surgery(patient_name,email,doctor_name,docemail, room_number, surgery_date, surgeryname):
    cursor = connection.cursor()

    # Look up the Doctor ID based on the provided Doctor Name
    cursor.execute("SELECT DoctorID FROM Doctors WHERE Names = :doctor_name and email=:docemail", doctor_name=doctor_name,docemail=docemail)
    doctor_id = cursor.fetchone()
    cursor.execute("SELECT PatientID FROM patients WHERE Names = :patient_name and email=:email", patient_name=patient_name,email=email)
    patient_id = cursor.fetchone()

    if not doctor_id:
        return False

    # Look up the Room ID based on the provided Room Number
    cursor.execute("SELECT RoomID FROM OperatingRooms WHERE RoomNumber = :room_number", room_number=room_number)
    room_id = cursor.fetchone()

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

# Example Usage
if __name__ == '__main__':
    
    # add_department('cardio')
    # add_department('opthomology')
    # add_operating_room('cardio', 'R1')
    # add_operating_room('opthomology', 'R2')
    # add_doctors('siva','siva5122','aa164@#','9940025247','cardio','Surgeon','siva@gmail.com')
    # add_staff('sam','9934578724','opthomology','sam@gmail.com','sam641','pdk164@#')
    # print(login('siva5122','aa164@#'))
    # print(login('sam641','pdk164@#'))
    # #adding a patient
    # add_patient('pranav','99417382','cardio','pranaav@gmail.com')
 
    # add_patient('paran', '8945678920', 'cardio', 'paran@gmail.com')
   
    
    # add_treatment_details('paran', 'paran@gmail.com','siva','siva@gmail.com', 'Routine checkup', '2024-01-10')
    # add_appointment('paran','paran@gmail.com', 'siva','siva@gmail.com', '2024-01-25', '20:00')
    # add_surgery('paran','paran@gmail.com','siva','siva@gmail.com', 'R2', '2024-02-01','appendicitis')

    # add_treatment_details('pranav','pranaav@gmail.com','siva','siva@gmail.com' ,'Prescription for flu', '2024-02-10')

    
    # add_outpatient('paran','paran@gmail.com', '2024-01-20', 'siva','siva@gmail.com','13:20', '14:00')
    # add_inpatient('pranav','pranaav@gmail.com', '2024-01-15', 'R1','siva','siva@gmail.com','2024-01-30')

    print('test')