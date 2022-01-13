# Third party imports
import os
import datetime as dt
from pymongo import MongoClient
import certifi

# Local application imports
if os.path.exists('env.py'):
    import env  # pylint: disable=unused-import
MONGODB_URI = os.environ.get('MONGODB_URI')
# Connect to MongoDB and set the database variables
client = MongoClient(host=MONGODB_URI,
                     tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
db = client.supportStats
users = db.users
stats = db.stats

class Date():
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

    def validate(self):
        if not db.stats.count_documents({
            "date": {'$gte': self.start, '$lte': self.end}}):
            print(f'I don\'t have any stats for w/c {Date.pretty_date(range_start)}')
        else:
            print('stats found')

    @staticmethod
    def pretty_date(date):
        """
        * Converts the date to be prettier and easier to read.
        * @return(str) -- pretty date string
        """
        return date.strftime('%A, %d %B %Y')


# test_date = Date()
# test_date.date = input('Insert a date: ')

# print(test_date.date)