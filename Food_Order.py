class FoodOrder:
    def __init__(self, foodname):
        self.__food_id = ""
        self.__foodname = foodname

        self.__price = 0

    # Accessor methods

    def get_food_id(self):
        return self.__foodid


    def get_foodname(self):
        return self.__foodname

    def get_price(self):
        return self.__price

    def get_quantity(self):
        return self.__quantity

    # Mutator methods
    def set_foodid(self,foodid):
        self.__foodid = foodid

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_price(self,price):
        self.__price = price

