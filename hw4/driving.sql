CREATE TABLE InsuranceCo (
  name  VARCHAR(30) PRIMARY KEY,
  phone VARCHAR(20)
);

CREATE TABLE Person (
  SSN   INT PRIMARY KEY,
  name  VARCHAR(30),
  phone VARCHAR(20)
);

CREATE TABLE Driver (
  driverID INT PRIMARY KEY,
  SSN      INT NOT NULL,
  FOREIGN KEY (SSN) REFERENCES Person(SSN)
);

CREATE TABLE ProfessionalDriver (
  driverID        INT PRIMARY KEY,
  medicalHistory  VARCHAR(300),
  FOREIGN KEY (driverID) REFERENCES Driver(driverID)
);

CREATE TABLE NonProfessionalDriver (
  driverID    INT PRIMARY KEY,
  FOREIGN KEY (driverID) REFERENCES Driver(driverID)
);

CREATE TABLE Vehicle (
  licensePlate      VARCHAR(30) PRIMARY KEY,
  year              INT,
  maxLiability      DOUBLE PRECISION,
  SSN               INT,             
  InsuranceCo_name  VARCHAR(30),    
  FOREIGN KEY (SSN)              REFERENCES Person(SSN),
  FOREIGN KEY (InsuranceCo_name) REFERENCES InsuranceCo(name)
);

CREATE TABLE Car (
  licensePlate VARCHAR(30) PRIMARY KEY,
  make         VARCHAR(30),
  FOREIGN KEY (licensePlate) REFERENCES Vehicle(licensePlate)
);

CREATE TABLE Truck (
  licensePlate VARCHAR(30) PRIMARY KEY,
  capacity     INT,
  FOREIGN KEY (licensePlate) REFERENCES Vehicle(licensePlate)
);

CREATE TABLE Drives (
  driverID     INT ,
  licensePlate VARCHAR(30),
  PRIMARY KEY (driverID, licensePlate),
  FOREIGN KEY (driverID)     REFERENCES NonProfessionalDriver(driverID) ,
  FOREIGN KEY (licensePlate) REFERENCES Car(licensePlate)               
);

CREATE TABLE Operates (
  driverID     INT ,
  licensePlate VARCHAR(30),
  PRIMARY KEY (driverID, licensePlate),
  FOREIGN KEY (driverID)     REFERENCES ProfessionalDriver(driverID) ,
  FOREIGN KEY (licensePlate) REFERENCES Truck(licensePlate)          
);

/*
b.
The relationship "Insures" is represented by the foreign key InsuranceCo_name in the Vehicle table. We can find the insurance company by join vehicles with insurance companies on that attribute.
c.
The representation of drives is by the Drives table, which links NonProfessionalDriver and Car through their driverID and licensePlate primary keys.
The representation of operates is by the Operates table, which links ProfessionalDriver and Truck through driverID and licensePlate primary keys.


*/
