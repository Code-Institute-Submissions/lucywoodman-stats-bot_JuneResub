import time
import datetime as dt
from statbotic.database import data


class Date:
    """
    Class for creating date instances.

    * Methods: range_end, validate.
    * Static Methods: pretty_date, simple_date.
    """

    def __init__(self):
        self.__date = ''

    # A getter function
    @property
    def date(self):
        return self.__date

    # A setter function
    @date.setter
    def date(self, input_date):
        """
        Check input date matches date format as required.
        Assign variable to self.

        * @arg(str) input_date -- passed from parent function.
        * @raises(ValueError) -- when format doesn't match date format.
        """
        try:
            date_obj = dt.datetime.strptime(input_date, '%Y-%m-%d')
        except ValueError:
            print('** The input did not match the date format. **')
            time.sleep(2)
        else:
            self.__date = date_obj

    def range_end(self, user_input):
        """
        Create a date using self + extra number of days.

        * @arg(int) user_input -- passed from parent function.
        * @return(date)
        """
        self.rng_end = self.__date + dt.timedelta(days=user_input)
        return self.rng_end

    def validate(self, *range):
        """
        Count documents in the database between two dates.

        * @arg(list) *range -- list of dates passed from parent function.
        * @raises(LookupError) -- when no documents found in database.
        """
        try:
            if not data.stats.count_documents({
                    "date": {'$gte': range[0], '$lte': range[1]}}):
                raise LookupError
        except LookupError:
            print(f'I don\'t have any data for {Date.pretty_date(range[0])}')
        else:
            print('Data found...')
            return True

    @staticmethod
    def pretty_date(date):
        """
        Convert the date to be prettier and easier to read.

        * @return(str) -- pretty date string
        """
        return date.strftime('%A, %d %B %Y')

    @staticmethod
    def simple_date(date):
        """
        Convert the date to be simpler for file names.

        * @return(str) -- simple date string
        """
        return date.strftime('%Y-%m-%d')
