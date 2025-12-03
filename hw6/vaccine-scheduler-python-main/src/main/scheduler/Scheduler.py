from typing import final
from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from model.Appointment import Appointment
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import sqlite3
import datetime


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    if len(tokens) != 3:
        print("Create patient failed")
        return

    username = tokens[1]
    password = tokens[2]

    if not is_strong_password(password):
        print('Create patient failed, please use a strong password (8+ char, at least one upper and one lower, at least one letter and one number, and at least one special character, from "!", "@", "#", "?")')
        return

    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    patient = Patient(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        patient.save_to_db()
    except sqlite3.Error as e:
        print("Create patient failed")
        return
    except Exception as e:
        print("Create patient failed")
        return
    print("Created user", username)


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]

    if not is_strong_password(password):
        print('Create caregiver failed, please use a strong password (8+ char, at least one upper and one lower, at least one letter and one number, and at least one special character, from "!", "@", "#", "?")')
        return
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except sqlite3.Error as e:
        print("Failed to create user.")
        return
    except Exception as e:
        print("Failed to create user.")
        return
    print("Created user", username)

def is_strong_password(password):
    if len(password) < 8:
        return False

    special_characters = "!@#?"
    # print("Checking password strength for:", password)

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in special_characters for c in password)


    # print(f"Password check - Upper: {has_upper}, Lower: {has_lower}, Digit: {has_digit}, Special: {has_special}")

    return has_upper and has_lower and has_digit and has_special

def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(select_username, (username,))
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            cm.close_connection()
            return row['Username'] is not None
    except sqlite3.Error as e:
        print("Error occurred when checking username")
        cm.close_connection()
        return True
    except Exception as e:
        print("Error occurred when checking username")
        cm.close_connection()
        return True
    cm.close_connection()
    return False

def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = ?"
    try:
        cursor = conn.cursor()
        cursor.execute(select_username, (username,))
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            cm.close_connection()
            return row['Username'] is not None
    except sqlite3.Error as e:
        print("Error occurred when checking username")
        cm.close_connection()
        return True
    except Exception as e:
        print("Error occurred when checking username")
        cm.close_connection()
        return True
    cm.close_connection()
    return False

def login_patient(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in, try again")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login patient failed")
        return

    username = tokens[1]
    password = tokens[2]

    patient = None
    try:
        patient = Patient(username, password=password).get()
    except sqlite3.Error as e:
        print("Login patient failed")
        return
    except Exception as e:
        print("Login patient failed")
        return

    # check if the login was successful
    if patient is None:
        print("Login patient failed")
    else:
        print("Logged in as " + username)
        current_patient = patient



def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except sqlite3.Error as e:
        print("Login failed.")
        return
    except Exception as e:
        print("Login failed.")
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None: 
        print("Please login first")
        return
    
    if len(tokens) != 2:
        print("Please try again")
        return

    try:
        available_caregivers = find_available_caregivers(tokens[1])
        caregivers_str = "\n".join(available_caregivers)

    except sqlite3.Error as e:
        # print("ssqltei 3 caregive")
        print("Please try again")
        return
    except Exception as e:
        # print(f"exception occurred: {e}")
        # print("try again 3 caregive")
        print("Please try again")
        return

    try:
        available_vaccines = find_available_vaccines()
        available_vaccines_str = "\n".join([f"{name} {doses}" for name, doses in available_vaccines.items()])

    except sqlite3.Error as e:
        print("Please try again")
        return
    except Exception as e:
        print("Please try again")
        return

    print("Caregivers:")
    print(caregivers_str) if caregivers_str else print("No caregivers available")
    print("Vaccines:")
    print(available_vaccines_str) if available_vaccines_str else print("No vaccines available")
    

def find_available_caregivers(date):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_available_caregivers = "SELECT * FROM Availabilities WHERE Date(Time) = ? ORDER BY Username"
    available_caregivers = []

    try:
        cursor = conn.cursor()
        cursor.execute(select_available_caregivers, (date,))
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            available_caregivers.append(row["Username"])
    except Exception as e:
        # print("Error occurred when checking username")
        raise e
    finally:
        cm.close_connection()

    return available_caregivers

def find_available_vaccines():
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_available_vaccines = "SELECT * FROM Vaccines"
    available_vaccines = {}
    try:
        cursor = conn.cursor()
        cursor.execute(select_available_vaccines)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            available_vaccines[row["Name"]] = row["Doses"]
    except Exception as e:
        raise e

    finally:
        cm.close_connection()

    return available_vaccines



def reserve(tokens):
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first")
        return
    elif current_patient is None:
        print("Please login as a patient")
        return
    
    if len(tokens) != 3:
        print("Please try again")
        return

    date = tokens[1]
    dose_name = tokens[2]

    available_caregivers = find_available_caregivers(date)
    if len(available_caregivers) == 0:
        print("No caregiver is available")
        return

    reserve_caregiver = available_caregivers[0]

    available_vaccines = find_available_vaccines()
    available_doses = available_vaccines.get(dose_name, 0)
    if available_doses == 0:
        print("Not enough available doses")
        return

    make_reservation(date, dose_name, reserve_caregiver)
    

def make_reservation(date, dose_name, reserve_caregiver):
    cm = ConnectionManager()
    conn = cm.create_connection()

    insert_appointment = "INSERT INTO Appointments (Time, Dose_name, Patient_name, Caregiver_name) VALUES (?, ?, ?, ?);" 
    decrement_dose = "UPDATE Vaccines SET Doses = Doses - 1 WHERE Name = ? AND Doses > 0;"
    delete_availability = "DELETE FROM Availabilities WHERE Username = ? AND Date(Time) = ?;"

    try:
        with conn:
            cursor = conn.cursor()

            cursor.execute((insert_appointment), (date, dose_name, current_patient.get_username(), reserve_caregiver))

            appointment_id = cursor.lastrowid

            cursor.execute(decrement_dose, (dose_name,))
            if cursor.rowcount == 0:
                raise sqlite3.Error("Not enough available doses")

            cursor.execute(delete_availability, (reserve_caregiver, date))

            print(f"Appointment ID {appointment_id}, Caregiver username {reserve_caregiver}")
       
    except sqlite3.Error as e:
        print("Please try again")
        return
    except Exception as e:
        print("Please try again")
        raise e
    finally:
        cm.close_connection()

   
def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format yyyy-mm-dd
    date_tokens = date.split("-")
    year = int(date_tokens[0])
    month = int(date_tokens[1])
    day = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except sqlite3.Error as e:
        print("Upload Availability Failed")
        return
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        return
    print("Availability uploaded!")


def cancel(tokens):
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first")
        return
    
    if len(tokens) != 2:
        print("Please try again")
        return

    appointment_id = tokens[1]
    appointment = select_appointment(appointment_id)

    if appointment is None:
        print(f"Appointment ID {appointment_id} does not exist")
        return

    try:
        cancel_appointment(appointment)
        print(f"Appointment ID {appointment_id} has been successfully canceled")
    except Exception as e:
        print(f"error {e}")
        print("Please try again")
        return

def select_appointment(appointment_id):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_appointment = "SELECT * FROM Appointments WHERE Id = ?;" 

    try:
        with conn:
            cursor = conn.cursor()

            cursor.execute(select_appointment, (appointment_id, ))
            result = cursor.fetchone()

            if result is not None:
                appointment = Appointment(Id=result["Id"], time=result["Time"], vaccine_name=result["Dose_name"], patient_username=result["Patient_name"], caregiver_username=result["Caregiver_name"])
                return appointment
       
    except sqlite3.Error as e:
        # print(f"error {e}")
        print("Please try again")
        return None
    except Exception as e:
        # print(f"error {e}")
        print("Please try again")
        raise e
    finally:
        cm.close_connection()
    return None

def cancel_appointment(appointment):
    cm = ConnectionManager()
    conn = cm.create_connection()

    aid = appointment.get_id()
    dose_name = appointment.get_dose_name()
    date = appointment.get_time()
    reserve_caregiver = appointment.get_caregiver_name()

    delete_appointment = "DELETE FROM Appointments WHERE Id = ?;" 
    increament_dose = "UPDATE Vaccines SET Doses = Doses + 1 WHERE Name = ?;"
    insert_availability = "INSERT INTO Availabilities (Username, Time) VALUES (?, ?);"

    try:
        with conn:
            cursor = conn.cursor()

            cursor.execute(delete_appointment, (aid,))

            cursor.execute(increament_dose, (dose_name,))

            cursor.execute(insert_availability, (reserve_caregiver, date))
            return 
    except Exception as e:
        # print(f"error {e}")
        raise e

def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except sqlite3.Error as e:
        print("Error occurred when adding doses")
        return
    except Exception as e:
        print("Error occurred when adding doses")
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except sqlite3.Error as e:
            print("Error occurred when adding doses")
            return
        except Exception as e:
            print("Error occurred when adding doses")
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except sqlite3.Error as e:
            print("Error occurred when adding doses")
            return
        except Exception as e:
            print("Error occurred when adding doses")
            return
    print("Doses updated!")


def show_appointments(tokens):
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Please login first")
        return
    elif len(tokens) != 1:
        print("Please try again")
        return

    cm = ConnectionManager()
    conn = cm.create_connection()
    user_name = current_caregiver.get_username() if current_caregiver is not None else current_patient.get_username()
    column_name = "Caregiver_name" if current_caregiver is not None else "Patient_name"

    select_appointments = f"SELECT * FROM Appointments WHERE {column_name} = ?"
    appointments = []

    try:
        cursor = conn.cursor()
        cursor.execute(select_appointments, (user_name,))
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            name = row["Patient_name"] if current_caregiver is not None else row["Caregiver_name"]
            appointment = f'{row["Id"]} {row["Dose_name"]} {row["Time"]} {name}'
            appointments.append(appointment)
        if len(appointments) == 0:
            print("No appointments scheduled")
        else:
            appointments_str = "\n".join(appointments)
            print(appointments_str)
    except Exception as e:
        # print("Error occurred when checking username")
        raise e
    finally:
        cm.close_connection()


def logout(tokens):
    try:
        if len(tokens) != 1:
            print("Please try again")
            return

        global current_caregiver
        global current_patient
        if current_caregiver is None and current_patient is None:
            print("Please login first")
            return

        current_caregiver = None
        current_patient = None
        print("Successfully logged out")

    except Exception as e:
        print("Please try again")
        

def start():
    stop = False
    print("*** Please enter one of the following commands ***")
    print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
    print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
    print("> logout")  # // TODO: implement logout (Part 2)
    print("> quit")
    print()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        # response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == "cancel":
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")


if __name__ == "__main__":
    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
