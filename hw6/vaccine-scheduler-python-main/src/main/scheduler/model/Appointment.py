import sqlite3
import sys
sys.path.append("../util/*")
sys.path.append("../db/*")
from util.Util import Util
from db.ConnectionManager import ConnectionManager


class Appointment:
    def __init__(self, Id, time=None, caregiver_username=None, patient_username=None, vaccine_name=None):
        self.Id = Id
        self.time = time
        self.caregiver_username = caregiver_username
        self.patient_username = patient_username
        self.vaccine_name = vaccine_name

    def get_id(self):
        return self.Id
    
    def get_dose_name(self):
        return self.vaccine_name

    def get_time(self):
        return self.time

    def get_caregiver_name(self):
        return self.caregiver_username
    # def get_username(self):

class AppointmentRepository:
    def __init__(self):
        self.appointments = []

    # getters
    def get(self, patient_username, caregiver_username):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()
        
        get_appointment_details = "SELECT * FROM Appointments" 
        if patient_username:
            get_appointment_details += " WHERE Patient_name = ?"
        elif caregiver_username:
            get_appointment_details += " WHERE Caregiver_name = ?"
        name = patient_username if patient_username else caregiver_username
        try:
            cursor.execute(get_appointment_details, (name,))
            appointments = []
            for row in cursor:
                appointment = Appointment(
                    Id=row['Id'],
                    time=row['Time'],
                    caregiver_username=row['Caregiver_name'],
                    patient_username=row['Patient_name'],
                    vaccine_name=row['Vaccine_name']
                )
                appointments.append(appointment)
            self.appointments = appointments
            return self.appointments
        except sqlite3.Error as e:
            raise e
        finally:
            cm.close_connection()
        return None

    #     return self.username

    # def get_salt(self):
    #     return self.salt

    # def get_hash(self):
    #     return self.hash

