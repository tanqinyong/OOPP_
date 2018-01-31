class FoodOrder:
    def __init__(self, foodname, days, patient_id):
        self.__foodname = foodname
        self.__days = days
        self.__patient_id = patient_id

    # Accessor methods
    def get_foodname(self):
        return self.__foodname

    def get_days(self):
        return self.__days

    def get_patient_id(self):
        return self.__patient_id

    # Mutator methods
    def set_foodname(self,foodname):
        self.__foodname = foodname

    def set_days(self,days):
        self.__days = days

    def set_patient_id(self,patient_id):
        self.__patient_id = patient_id


