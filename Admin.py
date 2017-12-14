
class Staff:
    def __init__(self, name, nric, username):
        self.__name = name
        self.__nric = nric
        self.__username = username

    # Accessors

    def get_name(self):
        return self.__name

    def get_nric(self):
        return self.__nric

    def get_username(self):
        return self.__username
    # Mutators

    def set_name(self, name):
        self.__name = name

    def set_nric(self, nric):
        self.__nric = nric

    def set_username(self,username):
        self.__username = username

class Patient:
    def __init__(self, name, nric, username):
        self.__name = name
        self.__nric = nric
        self.__username = username

    # Accessors

    def get_name(self):
        return self.__name

    def get_nric(self):
        return self.__nric

    def get_username(self):
        return self.__username

    # Mutators

    def set_name(self, name):
        self.__name = name

    def set_nric(self, nric):
        self.__nric = nric

    def set_username(self, username):
        self.__username = username
