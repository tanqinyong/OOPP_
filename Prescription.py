class Prescription:
    def __init__(self, patientname, date, medication, strength, symptom, quantity, doctorname, instruction):
        self.__patientname = patientname
        self.__date = date
        self.__medication = medication
        self._strength = strength  # e.g. 100mg (total amt of medicine)
        self.__symptom = symptom  # e.g. for nausea
        self.__quantity = quantity  # e.g. 50ml 3 times a day/ 2 tablets per day
        self.__doctorname = doctorname
        self.__instruction = instruction

    # Accessor methods

    def get_name(self):
        return self.__name

    def get_date(self):
        return self.__date

    def get_symptom(self):
        return self.__symptom

    def get_doctorname(self):
        return self.__doctorname

    # Mutator methods

    def set_medication(self, medication):
        self.__medication = medication

    def set_strength(self, strength):
        self.__strength = stength

    def set_quantity(self, quantity):
        self.__quantity = quantity

    def set_instruction(self, instruction):
        self.__instruction = instruction
