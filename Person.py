import datetime

class Person:
    def __init__(self, nric, name, dob, address, phone, gender):
        self.__nric = nric
        self.__name = name
        self.__dob = dob
        self.__address = address
        self.__phone = phone
        self.__gender = gender

    #Accessor methods

    def get_age(self):
        time = datetime.datetime.now()
        dob_list = self.__dob.split("/") or self.__dob.split(".") or self.__dob.split()
        return time.year - dob_list[2]

    def get_nric(self):
        return self.__nric

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    def get_address(self):
        return self.__address

    def get_phone(self):
        return self.__phone

    def get_gender(self):
        return self.__gender

    #Mutator methods

    def set_nric(self, nric):
        self.__nric = nric

    def set_name(self, name):
        self.__name = name

    def set_address(self, address):
        self.__address = address

    def set_phone(self, phone):
        self.__phone = phone

    def set_gender(self, gender):
        self.__gender = gender
