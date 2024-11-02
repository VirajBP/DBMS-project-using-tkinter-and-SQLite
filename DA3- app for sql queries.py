import sqlite3
import tkinter as tk
from tkinter import messagebox, scrolledtext

conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS department (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL,
    location TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS doctor (
    doctor_id INTEGER PRIMARY KEY,
    doctor_name TEXT NOT NULL,
    specialization TEXT,
    joining_date DATE NOT NULL,
    department_id INTEGER,
    FOREIGN KEY(department_id) REFERENCES department(department_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS patient (
    patient_id INTEGER PRIMARY KEY,
    patient_name TEXT,
    date_of_birth DATE,
    contact_number INTEGER,
    emergency_contact INTEGER,
    patient_address_state TEXT,
    patient_address_district TEXT,
    patient_address_city TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS appointment (
    appointment_id INTEGER PRIMARY KEY,
    appointment_date DATE,
    appointment_time TEXT,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_status TEXT NOT NULL,
    FOREIGN KEY(patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY(doctor_id) REFERENCES doctor(doctor_id)       
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS treatment (
    treatment_id INTEGER PRIMARY KEY,
    treatment_name TEXT,
    patient_id INTEGER,
    doctor_id INTEGER,
    treatment_date DATE NOT NULL,
    treatment_description TEXT,
    FOREIGN KEY(patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY(doctor_id) REFERENCES doctor(doctor_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS prescription (
    prescription_id INTEGER PRIMARY KEY,
    treatment_id INTEGER,
    medication_name TEXT,
    dosage_quantity INTEGER,
    duration INTEGER,
    FOREIGN KEY(treatment_id) REFERENCES treatment(treatment_id)    
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS operated_by (
    department_id INTEGER,
    doctor_id INTEGER,
    FOREIGN KEY(department_id) REFERENCES department(department_id),
    FOREIGN KEY(doctor_id) REFERENCES doctor(doctor_id)       
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS schedules (
    doctor_id INTEGER,
    appointment_id INTEGER,
    FOREIGN KEY(doctor_id) REFERENCES doctor(doctor_id),
    FOREIGN KEY(appointment_id) REFERENCES appointment(appointment_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS receives (
    patient_id INTEGER,
    treatment_id INTEGER,
    FOREIGN KEY(patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY(treatment_id) REFERENCES treatment(treatment_id)       
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS issued_by (
    prescription_id INTEGER,
    treatment_id INTEGER,
    FOREIGN KEY(prescription_id) REFERENCES prescription(prescription_id),
    FOREIGN KEY(treatment_id) REFERENCES treatment(treatment_id)      
)
''')

conn.commit()

def show_add_window():
    table = table_selection.get()
    clear_entries()
    reset_to_initial_state()
    enable_fields()
    if table == "Department":
        show_department_entry()
    elif table == "Doctor":
        show_doctor_entry()
    elif table == "Patient":
        show_patient_entry()
    elif table == "Appointment":
        show_appointment_entry()
    elif table == "Treatment":
        show_treatment_entry()
    elif table == "Prescription":
        show_prescription_entry()

def show_department_entry():
    entry_label.config(text="Add Department")
    for i, label in enumerate(fields["Department"]["labels"]):
        label.grid(row=i + 2, column=0, sticky="e")
        fields["Department"]["entries"][i].grid(row=i + 2, column=1, padx=5, pady=5)
    btn_add.config(command=add_department)

def show_doctor_entry():
    entry_label.config(text="Add Doctor")
    for i, label in enumerate(fields["Doctor"]["labels"]):
        label.grid(row=i + 2, column=0, sticky="e")
        fields["Doctor"]["entries"][i].grid(row=i + 2, column=1, padx=5, pady=5)
    btn_add.config(command=add_doctor)

def show_patient_entry():
    entry_label.config(text="Add Patient")
    for i, label in enumerate(fields["Patient"]["labels"]):
        label.grid(row=i + 2, column=0, sticky="e")
        fields["Patient"]["entries"][i].grid(row=i + 2, column=1, padx=5, pady=5)
    btn_add.config(command=add_patient)

def show_appointment_entry():
    entry_label.config(text="Add Appointment")
    for i, label in enumerate(fields["Appointment"]["labels"]):
        label.grid(row=i + 2, column=0, sticky="e")
        fields["Appointment"]["entries"][i].grid(row=i + 2, column=1, padx=5, pady=5)
    btn_add.config(command=add_appointment)

def show_treatment_entry():
    entry_label.config(text="Add Treatment")
    for i, label in enumerate(fields["Treatment"]["labels"]):
        label.grid(row=i + 2, column=0, sticky="e")
        fields["Treatment"]["entries"][i].grid(row=i + 2, column=1, padx=5, pady=5)
    btn_add.config(command=add_treatment)

def show_prescription_entry():
    entry_label.config(text="Add prescription")
    for i, label in enumerate(fields["Prescription"]["labels"]):
        label.grid(row=i + 2, column=0, sticky="e")
        fields["Prescription"]["entries"][i].grid(row=i + 2, column=1, padx=5, pady=5)
    btn_add.config(command=add_prescription)

def add_department():
    department_id = entry_department_id.get()
    department_name = entry_department_name.get()
    location = entry_location.get()
    try:
        cursor.execute('''
            INSERT INTO department (department_id, department_name, location)
            VALUES (?, ?, ?)
        ''', (department_id, department_name, location))
        conn.commit()
        messagebox.showinfo("Success", "Department added successfully!")
        btn_add.config(command=show_add_window)
        reset_to_initial_state()
        list_records("Department")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Department ID must be unique.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_doctor():
    doctor_id = entry_doctor_id.get()
    doctor_name = entry_doctor_name.get()
    specialization = entry_specialization.get()
    joining_date = entry_joining_date.get()
    department_id = entry_doctor_department_id.get()
    try:
        cursor.execute('''
            INSERT INTO doctor (doctor_id, doctor_name, specialization, joining_date, department_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (doctor_id, doctor_name, specialization, joining_date, department_id))
        conn.commit()
        messagebox.showinfo("Success", "Doctor added successfully!")
        btn_add.config(command=show_add_window)
        reset_to_initial_state()
        list_records("Doctor")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Doctor ID must be unique.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_patient():
    patient_id = entry_patient_id.get()
    patient_name = entry_patient_name.get()
    date_of_birth = entry_date_of_birth.get()
    contact_number = entry_contact_number.get()
    emergency_contact = entry_emergency_contact.get()
    patient_address_state = entry_patient_address_state.get()
    patient_address_district = entry_patient_address_district.get()
    patient_address_city = entry_patient_address_city.get()
    try:
        cursor.execute('''
            INSERT INTO patient (patient_id, patient_name, date_of_birth, contact_number, emergency_contact, patient_address_state, patient_address_district, patient_address_city)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (patient_id, patient_name, date_of_birth, contact_number, emergency_contact, patient_address_state, patient_address_district, patient_address_city))
        conn.commit()
        messagebox.showinfo("Success", "Patient added successfully!")
        btn_add.config(command=show_add_window)
        reset_to_initial_state()
        list_records("Patient")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Patient ID must be unique.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_appointment():
    appointment_id = entry_appointment_id.get()
    appointment_date = entry_appointment_date.get()
    appointment_time = entry_appointment_time.get()
    patient_id = entry_appointment_patient_id.get()
    doctor_id = entry_appointment_doctor_id.get()
    appointment_status = entry_appointment_status.get()
    
    try:
        cursor.execute('''
            INSERT INTO appointment (appointment_id, appointment_date, appointment_time, patient_id, doctor_id, appointment_status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (appointment_id, appointment_date, appointment_time, patient_id, doctor_id, appointment_status))
        conn.commit()
        messagebox.showinfo("Success", "Appointment added successfully!")
        btn_add.config(command=show_add_window)
        reset_to_initial_state()
        list_records("Appointment")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Appointment ID must be unique.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def add_treatment():
    treatment_id = entry_treatment_id.get()
    treatment_name = entry_treatment_name.get()
    patient_id = entry_treatment_patient_id.get()
    doctor_id = entry_treatment_doctor_id.get()
    treatment_date = entry_treatment_date.get()
    treatment_description = entry_treatment_description.get()
    
    try:
        cursor.execute('''
            INSERT INTO treatment (treatment_id, treatment_name, patient_id, doctor_id, treatment_date, treatment_description)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (treatment_id, treatment_name, patient_id, doctor_id, treatment_date, treatment_description))
        conn.commit()
        messagebox.showinfo("Success", "Treatment added successfully!")
        btn_add.config(command=show_add_window)
        reset_to_initial_state()
        list_records("Treatment")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Treatment ID must be unique.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def add_prescription():
    prescription_id = entry_prescription_id.get()
    treatment_id = entry_prescription_treatment_id.get()
    medication_name = entry_prescription_medication_name.get()
    dosage_quantity = entry_prescription_dosage_quantity.get()
    duration = entry_prescription_duration.get()
    
    try:
        cursor.execute('''
            INSERT INTO prescription (prescription_id, treatment_id, medication_name, dosage_quantity, duration)
            VALUES (?, ?, ?, ?, ?)
        ''', (prescription_id, treatment_id, medication_name, dosage_quantity, duration))
        conn.commit()
        messagebox.showinfo("Success", "Prescription added successfully!")
        btn_add.config(command=show_add_window)
        reset_to_initial_state()
        list_records("Prescription")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Prescription ID must be unique.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def list_records(table):
    text_area.delete(1.0, tk.END)
    cursor.execute(f'SELECT * FROM {table.lower()}')
    records = cursor.fetchall()
    
    if records:
        for record in records:
            text_area.insert(tk.END, str(record) + '\n')
    else:
        text_area.insert(tk.END, "No records found.")


def clear_entries():
    table = table_selection.get()
    if table in fields:
        for entry in fields[table]["entries"]:
            entry.delete(0, tk.END)


def enable_fields():
    for entry in (entry_department_id, entry_department_name, entry_location,
                  entry_doctor_id, entry_doctor_name, entry_specialization, entry_joining_date, entry_doctor_department_id,
                  entry_patient_id, entry_patient_name, entry_date_of_birth, entry_contact_number,
                  entry_emergency_contact, entry_patient_address_state, entry_patient_address_district, entry_patient_address_city):
        entry.config(state=tk.NORMAL)


def reset_to_initial_state():
    table = table_selection.get()
    clear_entries()
    for label in fields[table]["labels"]:
        label.grid_remove()
    entry_label.config(text="")
    for entry in fields[table]["entries"]:
        entry.grid_remove()
    entry_label.config(text="")


def execute_query():
    query = entry_query.get("1.0", tk.END).strip()
    try:
        cursor.execute(query)
        records = cursor.fetchall()
        text_area_query_results.delete(1.0, tk.END)
        if records:
            for record in records:
                text_area_query_results.insert(tk.END, str(record) + '\n')
        else:
            text_area_query_results.insert(tk.END, "No records found or no output from query.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", str(e))


def delete_record():
    table = table_selection.get()
    delete_query = f"DELETE FROM {table}"
    cursor.execute(delete_query)
    conn.commit()
    text_area.insert(tk.END, f"All records deleted from {table}.\n")


root = tk.Tk()
root.title("Department, Doctor, and Patient Management App")
btn_delete = tk.Button(root, text="Delete Record", command=delete_record)
btn_delete.grid(row=3, column=2, pady=5)

table_selection = tk.StringVar(value="Department")
tk.Label(root, text="Select Table:").grid(row=0, column=1)
tk.OptionMenu(root, table_selection, "Department", "Doctor", "Patient", "Appointment", "Treatment", "Prescription").grid(row=0, column=2, padx=10, pady=10)

label_department_id = tk.Label(root, text="Department ID:")
label_department_name = tk.Label(root, text="Department Name:")
label_location = tk.Label(root, text="Location:")

entry_department_id = tk.Entry(root)
entry_department_name = tk.Entry(root)
entry_location = tk.Entry(root)

label_doctor_id = tk.Label(root, text="Doctor ID:")
label_doctor_name = tk.Label(root, text="Doctor Name:")
label_specialization = tk.Label(root, text="Specialization:")
label_joining_date = tk.Label(root, text="Joining Date (YYYY-MM-DD):")
label_doctor_department_id = tk.Label(root, text="Department ID:")

entry_doctor_id = tk.Entry(root)
entry_doctor_name = tk.Entry(root)
entry_specialization = tk.Entry(root)
entry_joining_date = tk.Entry(root)
entry_doctor_department_id = tk.Entry(root)

label_patient_id = tk.Label(root, text="Patient ID:")
label_patient_name = tk.Label(root, text="Patient Name:")
label_date_of_birth = tk.Label(root, text="Date of Birth (YYYY-MM-DD):")
label_contact_number = tk.Label(root, text="Contact Number:")
label_emergency_contact = tk.Label(root, text="Emergency Contact:")
label_patient_address_state = tk.Label(root, text="Address State:")
label_patient_address_district = tk.Label(root, text="Address District:")
label_patient_address_city = tk.Label(root, text="Address City:")

entry_patient_id = tk.Entry(root)
entry_patient_name = tk.Entry(root)
entry_date_of_birth = tk.Entry(root)
entry_contact_number = tk.Entry(root)
entry_emergency_contact = tk.Entry(root)
entry_patient_address_state = tk.Entry(root)
entry_patient_address_district = tk.Entry(root)
entry_patient_address_city = tk.Entry(root)

label_appointment_id = tk.Label(root, text="Appointment ID:")
label_appointment_date = tk.Label(root, text="Appointment Date (YYYY-MM-DD):")
label_appointment_time = tk.Label(root, text="Appointment Time:")
label_appointment_patient_id = tk.Label(root, text="Patient ID:")
label_appointment_doctor_id = tk.Label(root, text="Doctor ID:")
label_appointment_status = tk.Label(root, text="Appointment Status:")

entry_appointment_id = tk.Entry(root)
entry_appointment_date = tk.Entry(root)
entry_appointment_time = tk.Entry(root)
entry_appointment_patient_id = tk.Entry(root)
entry_appointment_doctor_id = tk.Entry(root)
entry_appointment_status = tk.Entry(root)

label_treatment_id = tk.Label(root, text="Treatment ID:")
label_treatment_name = tk.Label(root, text="Treatment Name:")
label_treatment_patient_id = tk.Label(root, text="Patient ID:")
label_treatment_doctor_id = tk.Label(root, text="Doctor ID:")
label_treatment_date = tk.Label(root, text="Treatment Date (YYYY-MM-DD):")
label_treatment_description = tk.Label(root, text="Treatment Description:")

entry_treatment_id = tk.Entry(root)
entry_treatment_name = tk.Entry(root)
entry_treatment_patient_id = tk.Entry(root)
entry_treatment_doctor_id = tk.Entry(root)
entry_treatment_date = tk.Entry(root)
entry_treatment_description = tk.Entry(root)

label_prescription_id = tk.Label(root, text="Prescription ID:")
label_prescription_treatment_id = tk.Label(root, text="Treatment ID:")
label_prescription_medication_name = tk.Label(root, text="Medication Name:")
label_prescription_dosage_quantity = tk.Label(root, text="Dosage Quantity:")
label_prescription_duration = tk.Label(root, text="Duration:")

entry_prescription_id = tk.Entry(root)
entry_prescription_treatment_id = tk.Entry(root)
entry_prescription_medication_name = tk.Entry(root)
entry_prescription_dosage_quantity = tk.Entry(root)
entry_prescription_duration = tk.Entry(root)

fields = {
    "Department": {
        "labels": [label_department_id, label_department_name, label_location],
        "entries": [entry_department_id, entry_department_name, entry_location]
    },
    "Doctor": {
        "labels": [label_doctor_id, label_doctor_name, label_specialization, label_joining_date, label_doctor_department_id],
        "entries": [entry_doctor_id, entry_doctor_name, entry_specialization, entry_joining_date, entry_doctor_department_id]
    },
    "Patient": {
        "labels": [label_patient_id, label_patient_name, label_date_of_birth, label_contact_number, label_emergency_contact, label_patient_address_state, label_patient_address_district, label_patient_address_city],
        "entries": [entry_patient_id, entry_patient_name, entry_date_of_birth, entry_contact_number, entry_emergency_contact, entry_patient_address_state, entry_patient_address_district, entry_patient_address_city]
    },
    "Appointment": {
        "labels": [label_appointment_id, label_appointment_date, label_appointment_time, label_appointment_patient_id, label_appointment_doctor_id, label_appointment_status],
        "entries": [entry_appointment_id, entry_appointment_date, entry_appointment_time, entry_appointment_patient_id, entry_appointment_doctor_id, entry_appointment_status]
    },
    "Treatment": {
        "labels": [label_treatment_id, label_treatment_name, label_treatment_patient_id, label_treatment_doctor_id, label_treatment_date, label_treatment_description],
        "entries": [entry_treatment_id, entry_treatment_name, entry_treatment_patient_id, entry_treatment_doctor_id, entry_treatment_date, entry_treatment_description]
    },
    "Prescription": {
        "labels": [label_prescription_id, label_prescription_treatment_id, label_prescription_medication_name, label_prescription_dosage_quantity, label_prescription_duration],
        "entries": [entry_prescription_id, entry_prescription_treatment_id, entry_prescription_medication_name, entry_prescription_dosage_quantity, entry_prescription_duration]
    }
}

btn_add = tk.Button(root, text="Add Record", command=show_add_window)
btn_add.grid(row=1, column=2, columnspan=2, pady=15)

entry_label = tk.Label(root, text="")
entry_label.grid(row=1, column=0, columnspan=2)

text_area = scrolledtext.ScrolledText(root, width=60, height=10)
text_area.grid(row=12, column=1, columnspan=2)

btn_list = tk.Button(root, text="List Records", command=lambda: list_records(table_selection.get()))
btn_list.grid(row=2, column=2, pady=5)

tk.Label(root, text="Enter your SQL Query:").grid(row=13, column=1, columnspan=3)
entry_query = scrolledtext.ScrolledText(root, width=60, height=5)
entry_query.grid(row=14, column=1, columnspan=2)

btn_execute_query = tk.Button(root, text="Execute Query", command=execute_query)
btn_execute_query.grid(row=15, column=0, columnspan=3)

text_area_query_results = scrolledtext.ScrolledText(root, width=60, height=10)
text_area_query_results.grid(row=16, column=1, columnspan=2)

root.mainloop()
conn.close()