import os
from pymongo import MongoClient, errors
import certifi

if os.path.exists('env.py'):
    import env  # pylint: disable=unused-import

MONGODB_URI = os.environ.get('MONGODB_URI')

# Connect to MongoDB and set the database variables
client = MongoClient(host=MONGODB_URI,
                     tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)
data = client.supportStats
users = data.users
stats = data.stats


def test_database():
    """
    Test the database connection
    Raise an exception and exit if there are issues.
    """
    try:
        users.find_one()
    except errors.ConnectionFailure:
        print('The database says nope. Try again later.')
        exit()


def fetch_data_range(start, end):
    """
    Fetch data between two provided dates.

    Args:
    * start (date)
    * end (date)
    """
    data_range = data.stats.aggregate([
        {
            '$match': {
                'date': {
                    '$gte': start,
                    '$lte': end
                }
            }
        }
    ])
    return data_range


def aggregate_data(start, end):
    data_range = data.stats.aggregate([
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
                'Total ticket public comments': {
                    '$sum': '$comments'
                },
                'Total ticket solves': {
                    '$sum': '$solves'
                },
                'Total chats': {
                    '$sum': '$total'
                },
                'Average ticket public comments per day': {
                    '$avg': '$comments'
                },
                'Average ticket solves per day': {
                    '$avg': '$solves'
                },
                'Average chats per day': {
                    '$avg': '$total'
                },
                'Average chat wait time': {
                    '$avg': '$wait'
                },
                'Average chat CSAT for the week': {
                    '$avg': '$csat'
                }
            }
        }, {
            # Add comments per solve ratio.
            '$project': {
                'Total ticket public comments': 1,
                'Total ticket solves': 1,
                'Total chats': 1,
                'Average ticket public comments per day': 1,
                'Average ticket solves per day': 1,
                'Average chats per day': 1,
                'Average chat wait time': 1,
                'Average chat CSAT for the week': 1,
                'Average public comments per ticket solved': {
                    '$divide': [
                        '$Average ticket public comments per day',
                        '$Average ticket solves per day'
                    ]
                }
            }
        }
    ])
    return data_range
