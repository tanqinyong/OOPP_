import Person

class Staff(Person.Person):
    def __init__(self, nric, name, dob, address, phone, gender, id, password, type, position):
        super().__init__(nric, name, dob, address, phone, gender)
        self.__id = id
        self.__password = password
        self.__type = type
        self.__position = position

    #Accessor methods

    def get_id(self):
        return self.__id

    def get_password(self):
        return self.__password

    def get_type(self):
        return self.__type

    def get_position(self):
        return self.__position

    #Mutator methods

    def set_id(self, id):
        self.__id = id

    def set_password(self, password):
        self.__password = password

    def set_type(self, type):
        self.__type = type

    def set_position(self, position):
        self.__position = position

