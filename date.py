# Third party imports
import datetime as dt

# Local application imports
from helper import db

class Date:
    def __init__(self):
        self.__date = ''

    # A getter function
    @property
    def date(self):
        return self.__date

    # A setter function
    @date.setter
    def date(self, input_date):
        try:
            date_obj = dt.datetime.strptime(input_date, '%Y-%m-%d')
        except ValueError:
            print('The input did not match the date format.')
        else:
            self.__date = date_obj

    def wk_start(self):
        self.wk_start = self.__date - dt.timedelta(days=self.__date.weekday())
        return self.wk_start

    def wk_end(self):
        self.wk_end = self.wk_start + dt.timedelta(days=6)
        return self.wk_end

    def validate(self, *range):
        if not db.stats.count_documents({
            "date": {'$gte': range[0], '$lte': range[1]}}):
            print(f'I don\'t have any data for {Date.pretty_date(range[0])}')
        else:
            print('Data found...')

    @staticmethod
    def pretty_date(date):
        """
        * Converts the date to be prettier and easier to read.
        * @return(str) -- pretty date string
        """
        return date.strftime('%A, %d %B %Y')
        