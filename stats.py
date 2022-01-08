# Third party imports
import os
from pymongo import MongoClient
from datetime import date, timedelta

# Local application imports
if os.path.exists('settings.py'):
    from settings import mongodb_string

# Connect to MongoDB and set the database variables
client = MongoClient(mongodb_string)
db = client.supportStats
stats = db.stats

today = date.today()
yesterday = today - timedelta(days=1)
yesterday_str = yesterday.strftime('%A, %m %B %Y')


def yesterday_stats():
    title = f'Stats for {yesterday_str}'
    print('-' * len(title))
    print(title)
    print('-' * len(title))
    print('Tickets advanced: ')
    print('Tickets solved: ')
    print('\n')
    print('Incoming queue: ')
    print('Handoff queue: ')
    print('\n')
    print('Total chats: ')
    print('Wait time: ')
    print('Chat CSAT: ')
