class Edit_Patient():
    def __init__(self, name, illness, patientdesc, medicinedesc, med1, med2, med3):
        self.__name = name
        self.__illness = illness
        self.__patientdesc = patientdesc
        self.__medicinedesc = medicinedesc
        self.__med1 = med1
        self.__med2 = med2
        self.__med3 = med3

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_illness(self):
        return self.__illness

    def set_illness(self, illness):
        self.__illness = illness

    def get_patientdesc(self):
        return self.__patientdesc

    def set_patientdesc(self, patientdesc):
        self.__patientdesc = patientdesc

    def get_medicinedesc(self):
        return self.__medicinedesc

    def set_medicinedesc(self, medicinedesc):
        self.__medicinedsec = medicinedesc

    def get_med1(self):
        return self.__med1

    def set_med1(self, med1):
        self.__med1 = med1

    def get_med2(self):
        return self.__med2

    def set_med2(self, med2):
        self.__med2 = med2

    def get_med3(self):
        return self.__med3

    def set_med3(self, med3):
        self.__med3 = med3