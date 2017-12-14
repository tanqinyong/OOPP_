class comment:
    def __init__(self, name, comment):
        self.__name = name
        self.__comment = comment

    # Accessors

    def get_name(self):
        return self.__name

    def get_comment(self):
        return self.__comment

    # Mutators

    def set_name(self, name):
        self.__name = name

    def set_comment(self, comment):
        self.__comment = comment
