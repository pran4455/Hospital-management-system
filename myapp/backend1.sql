-- Users Table
DROP TABLE Surgeries CASCADE CONSTRAINTS;
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
-- Create a sequence for Department IDs
CREATE SEQUENCE DepartmentSeq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE OperatingRoomSeq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE userseq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE docterseq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE staffseq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE patientseq START WITH 1 INCREMENT BY 1;
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
    FOREIGN KEY(loginID) REFERENCES Users(UserID)
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
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- Doctors Table
CREATE TABLE Doctors (
    DoctorID VARCHAR(255) PRIMARY KEY,
    Names VARCHAR(255) NOT NULL,
    ContactNumber number(20),
    DepartmentID VARCHAR(255),
    DoctorType VARCHAR(50) CHECK (DoctorType IN ('Surgeon', 'General Practitioner')),
    Email VARCHAR(255) UNIQUE,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID),
    loginID VARCHAR(255),
    FOREIGN KEY(loginID) REFERENCES Users(UserID)
);

-- Staff Table
CREATE TABLE Staff (
    StaffID VARCHAR(255) PRIMARY KEY,
    Names VARCHAR(255) NOT NULL,
    ContactNumber number(20),
    DepartmentID VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID),
    loginID VARCHAR(255),
    FOREIGN KEY(loginID) REFERENCES Users(UserID)
);

-- Patients Table
CREATE TABLE Patients (
    PatientID VARCHAR(255) PRIMARY KEY,
    Names VARCHAR(255) NOT NULL,
    ContactNumber number(20),
    DepartmentID VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    FOREIGN KEY (DepartmentID) REFERENCES Departments(DepartmentID)
);

-- Treatment History Table
CREATE TABLE TreatmentHistory (
    TreatmentHistoryID VARCHAR(255) PRIMARY KEY,
    PatientID VARCHAR(255),
    DoctorID VARCHAR(255),
    TreatmentDetails VARCHAR(255),
    TreatmentDate DATE,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
);

-- Inpatients Table
CREATE TABLE Inpatients (
    InpatientID VARCHAR(255) PRIMARY KEY,
    PatientID VARCHAR(255),
    AdmissionDate DATE,
    RoomNumber VARCHAR(10),
    AssignedDoctorID VARCHAR(255),
    DischargeDate DATE,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (AssignedDoctorID) REFERENCES Doctors(DoctorID)
);

-- Outpatients Table
CREATE TABLE Outpatients (
    OutpatientID VARCHAR(255) PRIMARY KEY,
    PatientID VARCHAR(255),
    AppointmentDate DATE,
    DoctorID VARCHAR(255),
    Checkin TIMESTAMP,
    Checkout TIMESTAMP,
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID)
);

-- Appointments Table
CREATE TABLE Appointments (
    AppointmentID VARCHAR(255) PRIMARY KEY,
    DoctorID VARCHAR(255),
    PatientID VARCHAR(255),
    AppointmentDate DATE,
    AppointmentTime TIMESTAMP,
    CONSTRAINT chk_AppointmentTime CHECK (
        EXTRACT(HOUR FROM AppointmentTime) >= 9 AND 
        EXTRACT(HOUR FROM AppointmentTime) < 12 AND 
        (EXTRACT(HOUR FROM AppointmentTime) <> 12 OR EXTRACT(MINUTE FROM AppointmentTime) = 0) OR
        EXTRACT(HOUR FROM AppointmentTime) >= 13 AND 
        EXTRACT(HOUR FROM AppointmentTime) < 17
    ),
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID),
    FOREIGN KEY (PatientID) REFERENCES Patients(PatientID)
);


-- Surgeries Table
CREATE TABLE Surgeries (
    SurgeryID VARCHAR(255) PRIMARY KEY,
    DoctorID VARCHAR(255),
    RoomID VARCHAR(255),
    SurgeryDate DATE,
    FOREIGN KEY (DoctorID) REFERENCES Doctors(DoctorID),
    FOREIGN KEY (RoomID) REFERENCES OperatingRooms(RoomID)
);

--creating admins
insert into Users values('U1','pdk',5122,'Admin');
insert into Administrators values('A1','Piriyadharshin',8939155122,'piriyadharshini.a@gmail.com','U1');


commit;