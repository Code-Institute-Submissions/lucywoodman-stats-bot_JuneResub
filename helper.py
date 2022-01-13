# Third party imports
import os
from pymongo import MongoClient, errors
from tabulate import tabulate
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

class Title():
    def __init__(self, title):
        self.title = title

    def display(self):
        print('-' * len(self.title))
        print(self.title)
        print('-' * len(self.title))


def test_database():
    """
    * Tests the db connection
    * Raises an exception and exits if there are issues.
    """
    try:
        users.find_one()
    except errors.ConnectionFailure:
        print('The database says no. Try again later.')
        exit()


def user_continue(question):
    """
    * Asks the user if they'd like view or input more stats.
    * @raises(ValueError) -- If the input does not match y or n.
    * @return(bool) -- True for y, False for n.
    """
    while True:
        user_input = input(question)
        try:
            user_input.lower()
            if user_input not in ('y', 'n'):
                raise ValueError('The input did not match "y" or "n".')
        except ValueError:
            print('The input did not match "y" or "n".')
        else:
            return True if user_input == 'y' else False

def create_lists(data):
    temp_list = list(data)
    stats_list = []
    key_list = []
    for i in temp_list:
        for value in i.values():
            if value != "null":
                stats_list.append(value)
        for key in i.keys():
            if key != "_id":
                key_list.append(key)
    return key_list, stats_list

def print_stats(title, data):
    """
    * Create a table of stats for the given week.
    * @arg(obj) date -- the date object passed from stats_weekly().
    * @arg(list) key_list -- the list of keys from the aggregator.
    * @arg(list) stats_list -- the list of stats from the database.
    """
    # Convert the stats values to rounded floats to help table alignment.
    stats_list = [float(x) for x in data[1]]
    stats_list = [round(x, 1) for x in data[1]]
    # Merge the lists for tabulate.
    table_list = [list(x) for x in zip(data[0], stats_list)]

    # Generate header.
    print('-' * len(title))
    print(title)
    print('-' * len(title))

    # Print the list as a table.
    print(tabulate(table_list, tablefmt="fancy_grid", numalign="decimal"))


def aggregate_data(start, end):
    data = db.stats.aggregate([
        {
            # Fetch the data between the starting and ending dates.
            '$match': {
                'date': {
                    '$gte': start,
                    '$lte': end
                }
            }
        }, {
            # Group the data and calculate the column totals.
            '$group': {
                '_id': 'null',
                'Total tickets advanced': {
                    '$sum': '$t_advanced'
                },
                'Total ticket public comments': {
                    '$sum': '$t_pub_comments'
                },
                'Total tickets solved': {
                    '$sum': '$t_solved'
                },
                'Total chats': {
                    '$sum': '$c_total'
                },
                'Average ticket public comments per day': {
                    '$avg': '$t_pub_comments'
                },
                'Average tickets solved per day': {
                    '$avg': '$t_solved'
                },
                'Average chats per day': {
                    '$avg': '$c_total'
                },
                'Average chat wait time': {
                    '$avg': '$c_wait'
                },
                'Average chat CSAT for the week': {
                    '$avg': '$c_csat'
                }
            }
        }, {
            # Add comments per solve ratio.
            '$project': {
                'Total tickets advanced': 1,
                'Total ticket public comments': 1,
                'Total tickets solved': 1,
                'Total chats': 1,
                'Average ticket public comments per day': 1,
                'Average tickets solved per day': 1,
                'Average chats per day': 1,
                'Average chat wait time': 1,
                'Average chat CSAT for the week': 1,
                'Average public comments per ticket solved': {
                    '$divide': [
                        '$Average ticket public comments per day',
                        '$Average tickets solved per day'
                    ]
                }
            }
        }
    ])

    return data
