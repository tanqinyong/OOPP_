class Food:
    def __init__(self, name, price, type, description):
        self.__name = name
        self.__price = price
        self.__type = type
        self.__description = description

    # Accessor methods

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_type(self):
        return self.__type
    
    def get_description(self):
        return self.__description

    # Mutator methods

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        self.__price = price

    def set_type(self, type):
        self.__type = type

    def set_description(self, description):
        self.__description = description
