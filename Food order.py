class FoodOrder:
    def __init__(self, foodname, patientname, quantity, totalprice, waitingtime):
        self.__foodname = foodname
        self.__patientname = patientname
        self.__quantity = quantity
        self.__totalprice = totalprice
        self.__waitingtime = waitingtime

    # Accessor methods

    def get_patientname(self):
        return self.__patientname

    def get_foodname(self):
        return self.__foodname

    def get_price(self):
        return self.__price

    # Mutator methods

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_totalprice(self, totalprice):
        self.__totalprice = totalprice

    def set_waitingtime(self, waitingtime):
        self.__waitingtime = waitingtime
