from Person import Person

class Patient(Person):
    def __init__(self, nric, name, dob, address, phone, gender, id, diet, diagnosis, nurse):
        Person.__init__(self, nric, name, dob, address, phone, gender)
        self.__id = id
        self.__diet = diet
        self.__diagnosis = diagnosis
        self.__nurse = nurse

    #Accessor methods

    def get_id(self):
        return self.__id

    def get_diet(self):
        return self.__diet

    def get_diagnosis(self):
        return self.__diagnosis

    def get_nurse(self):
        return self.__nurse

    #Mutator methods

    def set_id(self, id):
        self.__id = id

    def set_diet(self, diet):
        self.__diet = diet

    def set_diagnosis(self, diagnosis):
        self.__diagnosis = diagnosis

    def set_nurse(self, nurse):
        self.__nurse = nurse
