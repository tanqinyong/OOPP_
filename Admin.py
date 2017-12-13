#
class Staff:
    def __init__(self,username,password):
        self.__username = username
        self.__password = password

    # Accessors

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    # Mutators

    def set_username(self,username):
        self.__username = username

    def set_password(self,password):
        self.__password = password


class Patient:
    def __init__(self,username,password):
        self.__username = username
        self.__password = password

    # Accessors

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    # Mutators

    def set_username(self,username):
        self.__username = username

    def set_password(self,password):
        self.__password = password
