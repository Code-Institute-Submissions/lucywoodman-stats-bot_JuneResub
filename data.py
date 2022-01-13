class AddData():
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, type=None) -> object:
        return obj.__dict__.get(self.name) or 0

    def __set__(self, obj, value) -> None:
        obj.__dict__[self.name] = value

class Stats():
    date = AddData()
    advanced = AddData()
    comments = AddData()
    solved = AddData()
    q_start = AddData()
    q_end = AddData()
    total = AddData()
    wait = AddData()
    csat = AddData()
