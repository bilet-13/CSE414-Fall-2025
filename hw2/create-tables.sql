CREATE TABLE Carriers (
  cid VARCHAR(8) PRIMARY KEY,
  cname VARCHAR(100)
);

CREATE TABLE Aircraft_Types (
  atid VARCHAR(7)  PRIMARY KEY,
  mfr  VARCHAR(40),
  model VARCHAR(30),
  num_engines INT,
  num_seats INT NOT NULL,  
  weight_class VARCHAR(7),
  avg_speed_mph INT
);

CREATE TABLE N_Numbers (
  n_number VARCHAR(6)  PRIMARY KEY,
  serial_number VARCHAR(30),
  mfr_mdl_code VARCHAR(7),
  year_mfr VARCHAR(4),
  name VARCHAR(50),
  street VARCHAR(40),
  street2 VARCHAR(40),
  city VARCHAR(20),
  state VARCHAR(2),
  zip_code VARCHAR(10),
  region VARCHAR(1),
  county VARCHAR(3),
  country VARCHAR(2),
  FOREIGN KEY (mfr_mdl_code) REFERENCES Aircraft_Types(atid)
);

CREATE TABLE Cancellation_Codes (
  ccid VARCHAR(1)  PRIMARY KEY,
  description VARCHAR(20)
);

CREATE TABLE Flights (
  fid INT PRIMARY KEY,
  year INT,
  month INT,
  day_of_month INT,
  day_of_week INT,
  cid VARCHAR(8),
  tail_num VARCHAR(6),
  op_carrier_flight_num INT,
  origin VARCHAR(3),
  origin_city VARCHAR(40),
  origin_state VARCHAR(2),
  dest VARCHAR(3),
  dest_city VARCHAR(40),
  dest_state VARCHAR(2),
  sched_dep_time INT,
  dep_time INT,
  dep_delay REAL,
  sched_arr_time INT,
  arr_time INT,
  arr_delay REAL,
  cancelled INT,
  cancellation_code VARCHAR(1),  
  duration_mins INT,
  distance_mi INT,
  price INT,
  FOREIGN KEY (cid) REFERENCES Carriers(cid),
  FOREIGN KEY (tail_num) REFERENCES N_Numbers(n_number)
);

PRAGMA foreign_keys = ON;
