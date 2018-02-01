class FoodOrder:
    def __init__(self, foodname, days, patient_id, indian, malay, chinese, western, international):
        self.__foodname = foodname
        self.__days = days
        self.__patient_id = patient_id
        self.__indian = indian
        self.__malay = malay
        self.__chinese = chinese
        self.__western = western
        self.__international = international

    # Accessor methods
    def get_foodname(self):
        return self.__foodname

    def get_days(self):
        return self.__days

    def get_patient_id(self):
        return self.__patient_id

    def get_indian(self):
        return self.__indian

    def get_malay(self):
        return self.__malay

    def get_chinese(self):
        return self.__chinese

    def get_western(self):
        return self.__western

    def get_international(self):
        return self.__international

    # Mutator methods
    def set_foodname(self,foodname):
        self.__foodname = foodname

    def set_days(self,days):
        self.__days = days

    def set_patient_id(self,patient_id):
        self.__patient_id = patient_id

    def set_indian(self,indian):
        self.__indian = indian

    def set_malay(self,malay):
        self.__malay = malay

    def set_chinese(self,chinese):
        self.__chinese = chinese

    def set_western(self,western):
        self.__western = western

    def set_international(self,international):
        self.__international = international




