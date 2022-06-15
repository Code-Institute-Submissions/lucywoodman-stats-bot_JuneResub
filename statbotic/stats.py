class AddData:
    """
    * Class used by the Stats class.
    * Creates properties from variables.
    """

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, type=None) -> object:
        return obj.__dict__.get(self.name) or 0

    def __set__(self, obj, value) -> None:
        obj.__dict__[self.name] = value


class Stats:
    """
    * Class for creating stats instances.
    * Uses the AddData class to create properties,
    * and saves values to the properties.
    """
    date = AddData()
    comments = AddData()
    solves = AddData()
    total = AddData()
    wait = AddData()
    csat = AddData()
