-- Users Table
DROP TABLE Surgeries CASCADE CONSTRAINTS;
REM TABLE NOT USED APPOINTMENTS
DROP TABLE Appointments CASCADE CONSTRAINTS;
DROP TABLE Outpatients CASCADE CONSTRAINTS;
DROP TABLE Inpatients CASCADE CONSTRAINTS;
DROP TABLE TreatmentHistory CASCADE CONSTRAINTS;
DROP TABLE Patients CASCADE CONSTRAINTS;
DROP TABLE Staff CASCADE CONSTRAINTS;
DROP TABLE Doctors CASCADE CONSTRAINTS;
DROP TABLE OperatingRooms CASCADE CONSTRAINTS;
DROP TABLE Departments CASCADE CONSTRAINTS;
DROP TABLE Administrators CASCADE CONSTRAINTS;
DROP TABLE Users CASCADE CONSTRAINTS;
drop sequence operatingrooms;
drop sequence departmentseq;
drop sequence userseq;
drop sequence docterseq;
drop sequence staffseq;
drop sequence patientseq;
drop sequence inpatientseq;
drop sequence outpatientseq;
drop sequence appointmentseq;
drop sequence treatmenthistoryseq;
drop sequence surgeryseq;
drop sequence OperatingRoomSeq;
-- Create a sequence for Department IDs
CREATE SEQUENCE DepartmentSeq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE OperatingRoomSeq START WITH 2 INCREMENT BY 1;
CREATE SEQUENCE userseq START WITH 2 INCREMENT BY 1;
CREATE SEQUENCE docterseq START WITH 2 INCREMENT BY 1;
CREATE SEQUENCE staffseq START WITH 2 INCREMENT BY 1;
CREATE SEQUENCE inpatientseq START WITH 2 INCREMENT BY 1;
CREATE SEQUENCE outpatientseq START WITH 2 INCREMENT BY 1;
CREATE SEQUENCE appointmentseq START WITH 2 INCREMENT BY 1;
CREATE SEQUENCE treatmenthistoryseq START WITH 2 INCREMENT BY 1;
CREATE SEQUENCE surgeryseq START WITH 2 INCREMENT BY 1;
CREATE SEQUENCE patientseq START WITH 2 INCREMENT BY 1;
-- Insert data into the Departments table with the concatenated ID


CREATE TABLE Users (
    UserID VARCHAR(255) PRIMARY KEY,
    Username VARCHAR(255) UNIQUE,
    Passwords VARCHAR(255),  
    Roles VARCHAR(20) CHECK (Roles IN ('Admin', 'Staff', 'Doctor'))
);

-- Administrators Table
CREATE TABLE Administrators (
    AdministratorID VARCHAR(255) PRIMARY KEY,
    Names VARCHAR(255),
    ContactNumber VARCHAR(20),
    Email VARCHAR(255) UNIQUE,
    loginID VARCHAR(255),
    FOREIGN KEY(loginID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Departments Table
CREATE TABLE Departments (
    DepartmentID VARCHAR(255) PRIMARY KEY,
    DepartmentName VARCHAR(255) UNIQUE
);

-- Operating Rooms Table
CREATE TABLE OperatingRooms (
    RoomID VARCHAR(255) PRIMARY KEY,
    RoomNumber VARCHAR(255) NOT NULL,
    DepartmentID VARCHAR(255),
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID) ON DELETE CASCADE
);

-- Doctors Table
CREATE TABLE Doctors (
    DoctorID VARCHAR(255) PRIMARY KEY,
    Names VARCHAR(255) NOT NULL,
    ContactNumber number(20),
    DepartmentID VARCHAR(255),
    DoctorType VARCHAR(50) CHECK (DoctorType IN ('Surgeon', 'General Practitioner')),
    Email VARCHAR(255) UNIQUE,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID) ON DELETE CASCADE,
    loginID VARCHAR(255),
    FOREIGN KEY(loginID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Staff Table
CREATE TABLE Staff (
    StaffID VARCHAR(255) PRIMARY KEY,
    Names VARCHAR(255) NOT NULL,
    ContactNumber number(20),
    DepartmentID VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID) ON DELETE CASCADE,
    loginID VARCHAR(255),
    FOREIGN KEY(loginID) REFERENCES Users(UserID) ON DELETE CASCADE
);

-- Patients Table
CREATE TABLE Patients (
    PatientID VARCHAR(255) PRIMARY KEY,
    Names VARCHAR(255) NOT NULL,
    ContactNumber number(20),
    DepartmentID VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID) ON DELETE CASCADE
);

-- Treatment History Table
CREATE TABLE TreatmentHistory (
    TreatmentHistoryID VARCHAR(255) PRIMARY KEY,
    PatientID VARCHAR(255),
    DoctorID VARCHAR(255),
    TreatmentDetails VARCHAR(255),
    TreatmentDate DATE,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) ON DELETE CASCADE,
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID) ON DELETE CASCADE
);

-- Inpatients Table
CREATE TABLE Inpatients (
    InpatientID VARCHAR(255) PRIMARY KEY,
    PatientID VARCHAR(255),
    AdmissionDate DATE,
    RoomNumber VARCHAR(10),
    AssignedDoctorID VARCHAR(255),
    DischargeDate DATE,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) ON DELETE CASCADE,
    FOREIGN KEY (AssignedDoctorID) REFERENCES Doctors(DoctorID) ON DELETE CASCADE
);

-- Outpatients Table
CREATE TABLE Outpatients (
    OutpatientID VARCHAR(255) PRIMARY KEY,
    PatientID VARCHAR(255),
    AppointmentDate DATE,
    DoctorID VARCHAR(255),
    Checkin TIMESTAMP,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) ON DELETE CASCADE,
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID) ON DELETE CASCADE
);




-- Surgeries Table
CREATE TABLE Surgeries (
    SurgeryID VARCHAR(255) PRIMARY KEY,
    PatientID VARCHAR(255),
    DoctorID VARCHAR(255),
    RoomID VARCHAR(255),
    SurgeryDate DATE,
    surgeryname VARCHAR(255),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID) ON DELETE CASCADE,
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID) ON DELETE CASCADE,
    FOREIGN KEY (RoomID) REFERENCES OperatingRooms(RoomID) ON DELETE CASCADE
);

--creating admins
insert into Users values('U1','pdk',5122,'Admin');
insert into Administrators values('A1','Piriyadharshin',8939155122,'piriyadharshini.a@gmail.com','U1');


commit;

CREATE OR REPLACE TRIGGER inpatientadding
BEFORE INSERT OR UPDATE ON Inpatients
FOR EACH ROW
BEGIN
  IF :NEW.AdmissionDate < TRUNC(SYSDATE) THEN
    RAISE_APPLICATION_ERROR(-20001, 'Admission date should be either today or future dates');
  END IF;
END;
/

CREATE OR REPLACE TRIGGER outpatientadding
BEFORE INSERT OR UPDATE ON Outpatients
FOR EACH ROW
BEGIN
  IF :NEW.AppointmentDate< TRUNC(SYSDATE)  THEN
    RAISE_APPLICATION_ERROR(-20002, 'Appointment date should be either today or future dates');
  END IF;
END;
/

CREATE OR REPLACE TRIGGER treatmenthistoryadding
BEFORE INSERT OR UPDATE ON TreatmentHistory
FOR EACH ROW
BEGIN
  IF :NEW.TreatmentDate< TRUNC(SYSDATE) THEN
    RAISE_APPLICATION_ERROR(-20003, 'Treatment date should be either today or future dates');
  END IF;
END;
/



CREATE OR REPLACE TRIGGER addsurgery
BEFORE INSERT OR UPDATE ON Surgeries
FOR EACH ROW
BEGIN
  IF :NEW.SurgeryDate < TRUNC(SYSDATE) THEN
    RAISE_APPLICATION_ERROR(-20005, 'Surgery date should be after the current time.');
  END IF;
END;
/

DROP PROCEDURE addpatient;
CREATE OR REPLACE PROCEDURE addpatient(
    patientid IN VARCHAR2,
    pname IN VARCHAR2,
    contact IN NUMBER,
    deptid IN VARCHAR2,
    email IN VARCHAR2
)
AS
BEGIN
    INSERT INTO patients VALUES (
        patientid,
        pname,
        contact,
        deptid,
        email
    );
    COMMIT;
END addpatient;
/

CREATE OR REPLACE TRIGGER outpatavailabiltiy
BEFORE INSERT ON Outpatients
FOR EACH ROW
DECLARE
    v_doctor_count NUMBER;
BEGIN
    -- Check if the doctor is available for the given appointment date and check-in time
    SELECT COUNT(*)
    INTO v_doctor_count
    FROM Doctors d
    WHERE d.DoctorID = :NEW.DoctorID
      AND NOT EXISTS (
          SELECT 1
          FROM Outpatients o
          WHERE o.DoctorID = d.DoctorID
            AND o.AppointmentDate = :NEW.AppointmentDate
            AND o.checkin=:NEW.Checkin
      );

    IF v_doctor_count = 0 THEN
        RAISE_APPLICATION_ERROR(-20006, 'Doctor is not available for the given appointment date and time.');
    END IF;
END;
/
