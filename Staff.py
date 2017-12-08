import Person

class Staff(Person.Person):
    def __init__(self, nric, name, dob, address, phone, gender, id, patient):
        super().__init__(nric, name, dob, address, phone, gender)
        self.__id = id
        self.__patient = patient

    #Accessor methods

    def get_id(self):
        return self.__id

    def get_patient(self):
        return self.__patient

    #Mutator methods

    def set_id(self, id):
        self.__id = id

    def set_diet(self, patient):
        self.__diet = patient