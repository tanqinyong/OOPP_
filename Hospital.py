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
    def __init__(self, name, nric, dob, email, address, gender, occupation, income, bloodtype, race, phone_no, emergency_contact_no,
                 emergency_contact_address, emergency_contact_relationship, maritalstatus, username, password, image_name):
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

    def set_image_name(self, ward):
        self.__ward = ward

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
    def __init__(self, name, illness, patientdesc, time, image_name, ward):
        super().__init__(name)
        self.__illness = illness
        self.__patientdesc = patientdesc
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

class Medicine:
    def __init__(self, medName, medDesc, medDosage, sideEffect, medTime, medInterval):
        self.__medName = medName
        self.__medDesc = medDesc
        self.__medDosage = medDosage
        self.__sideEffect = sideEffect
        self.__medTime = medTime
        self.__medInterval = medInterval
        self.__med_id = ""

    def get_medName(self):
        return self.__medName

    def set_medName(self, medName):
        self.__medName = medName

    def get_medDesc(self):
        return self.__medDesc

    def set_medDesc(self, medDesc):
        self.__medDesc = medDesc

    def get_medDosage(self):
        return self.__medDosage

    def set_medDosage(self, medDosage):
        self.__medDosage = medDosage

    def get_sideEffect(self):
        return self.__sideEffect

    def set_sideEffect(self, sideEffect):
        self.__sideEffect = sideEffect

    def get_medTime(self):
        return self.__medTime

    def set_medTime(self, medTime):
        self.__medTime = medTime

    def get_medInterval(self):
        return self.__medInterval

    def set_medInterval(self, medInterval):
        self.__medInterval = medInterval

    def get_med_id(self):
        return self.__med_id

    def set_med_id(self, med_id):
        self.__med_id = med_id

        # staff = Staff(v["name"], v["nric"], v["gender"],  v["dob"], v["email"], v["phone_no"], v["address"], v['username'], v['password'], v['image_name'], v['ward'])

# This is for staff
class Staff:
    def __init__(self, name, nric, gender, dob,  email, phone_no, address, username, password, image_name):
        # super().__init__(name, nric, username, password, image_name, ward, dob, email, address, gender, phone_no)
        self.__name = name
        self.__nric = nric
        self.__gender = gender
        self.__dob = dob
        self.__email = email
        self.__phone_no = phone_no
        self.__address = address
        self.__image_name = image_name
        self.__username = username
        self.__password = password
        self.__staffid = ''
        # self.__ward = ward

    def set_staffid(self, staffid):
        self.__staffid = staffid

    def get_staffid(self):
        return self.__staffid

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

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

    # def get_ward(self):
    #     return self.__ward
    #
    # def set_ward(self,ward):
    #     self.__ward = ward

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
