class Payment_Info:
    def __init__(self, type, card_type, card_number, card_name, card_expiry, card_cvc):
        self.__type = type
        self.__card_type = card_type
        self.__card_number = card_number
        self.__card_name = card_name
        self.__card_expiry = card_expiry
        self.__card_cvc = card_cvc

    #Accessor methods
    def get_type(self):
        return self.__type

    def get_card_type(self):
        return self.__card_type

    def get_card_number(self):
        return self.__card_number

    def get_card_name(self):
        return self.__card_name

    def get_card_expiry(self):
        return self.__card_expiry

    def get_card_cvc(self):
        return self.__card_cvc

    #Mutator methods
    def set_type(self, type):
        self.__type = type

    def set_card_type(self, card_type):
        self.__card_type = card_type

    def set_card_number(self, card_number):
        self.__card_number = card_number

    def set_card_name(self, card_name):
        self.__card_name = card_name

    def set_card_expiry(self, card_expiry):
        self.__card_expiry = card_expiry

    def set_card_cvc(self, card_cvc):
        self.__card_cvc = card_cvc
