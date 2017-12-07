class Medicine:
    def __init__(self, name, dosage, price, description):
        self.__name = name
        self.__dosage = dosage
        self.__price = price
        self.__description = description

    #Accessor methods

    def get_name(self):
        return self.__name

    def get_dosage(self):
        return self.__dosage

    def get_price(self):
        return self.__price

    def get_description(self):
        return self.__description

    #Mutator methods

    def set_name(self, name):
        self.__name = name

    def set_dosage(self, dosage):
        self.__dosage = dosage

    def set_price(self, price):
        self.__price = price

    def set_description(self, description):
        self.__description = description
