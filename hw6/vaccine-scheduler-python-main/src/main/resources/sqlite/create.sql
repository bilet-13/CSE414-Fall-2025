CREATE TABLE Caregivers (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Patients (
    Username varchar(255),
    Salt BINARY(16),
    Hash BINARY(16),
    PRIMARY KEY (Username)
);

CREATE TABLE Availabilities (
    Time date,
    Username varchar(255) REFERENCES Caregivers,
    PRIMARY KEY (Time, Username)
);

CREATE TABLE Vaccines (
    Name varchar(255),
    Doses int,
    PRIMARY KEY (Name)
);

CREATE TABLE Appointments (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Time date,
    Dose_name varchar(255),
    Patient_name varchar(255),
    Caregiver_name varchar(255),
    Foreign KEY (Dose_name) REFERENCES Vaccines(Name),
    Foreign KEY (Patient_name) REFERENCES Patients(Username),
    Foreign KEY (Caregiver_name) REFERENCES Caregivers(Username),
    UNIQUE (TIME, Dose_name, Patient_name)
);
