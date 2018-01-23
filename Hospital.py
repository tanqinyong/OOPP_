class Hospital():
    def __init__(self, name):
        self.__patient_id = ""
        self.__name = name

    def get_patient_id(self):
        return self.__patient_id
    def set_patient_id(self, patient_id):
        self.__patient_id = patient_id

    def get_name(self):
        return self.__name
    def set_name(self, name):
        self.__name = name


# This is for Patients!
class Admin_Work(Hospital):
    def __init__(self, name, nric, dob, email, address, gender, occupation, income, bloodtype, race, phone_no, emergency_contact_no, emergency_contact_address, emergency_contact_relationship, maritalstatus, username, password, image_name):
        super().__init__(name)
        self.__nric = nric
        self.__dob = dob
        self.__email = email
        self.__address = address
        self.__gender = gender
        self.__occupation = occupation
        self.__income = income
        self.__bloodtype = bloodtype
        self.__race = race
        self.__phone_no = phone_no
        self.__emergency_contact_no = emergency_contact_no
        self.__emergency_contact_address = emergency_contact_address
        self.__emergency_contact_relationship = emergency_contact_relationship
        self.__maritalstatus = maritalstatus
        self.__username = username
        self.__password = password
        self.__image_name = image_name

    def get_image_name(self):
        return self.__image_name
    def set_image_name(self, image_name):
        self.__image_name = image_name

    def get_nric(self):
        return self.__nric
    def set_nric(self, nric):
        self.__nric = nric

    def get_dob(self):
        return self.__dob
    def set_dob(self, dob):
        self.__dob = dob

    def get_email(self):
        return self.__email
    def set_email(self, email):
        self.__email = email

    def get_address(self):
        return self.__address
    def set_address(self, address):
        self.__address = address

    def get_gender(self):
        return self.__gender
    def set_gender(self, gender):
        self.__gender = gender

    def get_occupation(self):
        return self.__occupation
    def set_occupation(self, occupation):
        self.__occupation = occupation

    def get_income(self):
        return self.__income
    def set_income(self, income):
        self.__income = income

    def get_bloodtype(self):
        return self.__bloodtype
    def set_bloodtype(self, bloodtype):
        self.__bloodtype = bloodtype

    def get_race(self):
        return self.__race
    def set_race(self, race):
        self.__race = race

    def get_phone_no(self):
        return self.__phone_no
    def set_phone_no(self, phone_no):
        self.__phone_no = phone_no

    def get_emergency_contact_no(self):
        return self.__emergency_contact_no
    def set_emergency_contact_no(self, emergency_contact_no):
        self.__emergency_contact_no = emergency_contact_no

    def get_emergency_contact_address(self):
        return self.__emergency_contact_address
    def set_emergency_contact_address(self, emergency_contact_address):
        self.__emergency_contact_address = emergency_contact_address

    def get_emergency_contact_relationship(self):
        return self.__emergency_contact_relationship
    def set_emergency_contact_relationship(self, emergency_contact_relationship):
        self.__emergency_contact_relation = emergency_contact_relationship

    def get_maritalstatus(self):
        return self.__maritalstatus
    def set_maritalstatus(self, maritalstatus):
        self.__maritalstatus = maritalstatus

    def get_username(self):
        return self.__username
    def set_username(self, username):
        self.__username = username

    def get_password(self):
        return self.__password
    def set_passoword(self, password):
        self.__password = password


# This is to edit Patients
class Edit_Patient(Hospital):
    def __init__(self, name, illness, patientdesc, medicinedesc, med1, med2, med3, time, image_name, ward):
        super().__init__(name)
        self.__illness = illness
        self.__patientdesc = patientdesc
        self.__medicinedesc = medicinedesc
        self.__med1 = med1
        self.__med2 = med2
        self.__med3 = med3
        self.__time = time
        self.__image_name = image_name
        self.__ward = ward

    def get_image_name(self):
        return self.__image_name
    def set_image_name(self, image_name):
        self.__image_name = image_name

    def get_ward(self):
        return self.__ward
    def set_ward(self, ward):
        self.__ward = ward

    def get_time(self):
        return self.__time

    def set_time(self, time):
        self.__time = time

    def get_illness(self):
        return self.__illness

    def set_illness(self, illness):
        self.__illness = illness

    def get_patientdesc(self):
        return self.__patientdesc

    def set_patientdesc(self, patientdesc):
        self.__patientdesc = patientdesc

    def get_medicinedesc(self):
        return self.__medicinedesc

    def set_medicinedesc(self, medicinedesc):
        self.__medicinedsec = medicinedesc

    def get_med1(self):
        return self.__med1

    def set_med1(self, med1):
        self.__med1 = med1

    def get_med2(self):
        return self.__med2

    def set_med2(self, med2):
        self.__med2 = med2

    def get_med3(self):
        return self.__med3

    def set_med3(self, med3):
        self.__med3 = med3


# This is for staff
class Staff(Hospital):
    def __init__(self, name, nric, username, password, image_name, ward, dob, email, address, gender, phone_no):
        super().__init__(name)
        self.__username = username
        self.__password = password
        self.__nric = nric
        self.__image_name = image_name
        self.__ward = ward
        self.__dob = dob
        self.__email = email
        self.__address = address
        self.__gender = gender
        self.__phone_no = phone_no

    def get_nric(self):
        return self.__nric

    def set_nric(self, nric):
        self.__nric = nric

    def get_username(self):
        return self.__username

    def set_username(self, username):
        self.__username = username

    def get_password(self):
        return self.__password

    def set_password(self, password):
        self.__password = password

    def get_image_name(self):
        return self.__image_name

    def set_image_name(self,image_name):
        self.__image_name=image_name

    def get_ward(self):
        return self.__ward

    def set_ward(self,ward):
        self.__ward = ward

    def get_dob(self):
        return self.__dob

    def set_dob(self, dob):
        self.__dob = dob

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_address(self):
        return self.__address

    def set_address(self, address):
        self.__address = address

    def get_gender(self):
        return self.__gender

    def set_gender(self, gender):
        self.__gender = gender

    def get_phone_no(self):
        return self.__phone_no

    def set_phone_no(self, phone_no):
        self.__phone_no = phone_no

class NurseCall:
    def __init__(self, reason,user_id):
        self.__reason = reason
        self.__id = user_id

    # Accessor methods
    def get_reason(self):
        return self.__reason

    def get_user_id(self):
        return self.__id

    # Mutator methods
    def set_reason(self, reason):
        self.__reason = reason
