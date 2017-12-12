class NurseCall:
    def __init__(self, patientname, wardnumber, urgency, reason, nursename):
        self.__patientname = patientname
        self.__wardnumber = wardnumber
        self.__urgency = urgency
        self.__reason = reason
        self.__nursename = nursename

    # Accessor methods

    def get_patientname(self):
        return self.__patientname

    def get_wardnumber(self):
        return self.__wardnumber

    # Mutator methods

    def set_urgency(self, urgency):
        self.__urgency = urgency

    def set_reason(self, reason):
        self.__reason = reason

    def set_nursename(self, nursename):
        self.__nursename = nursename
