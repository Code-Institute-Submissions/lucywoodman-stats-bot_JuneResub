# Third party imports
import os
from pymongo import MongoClient

# Local application imports
if os.path.exists('settings.py'):
    from settings import mongodb_string
from menuhelper import MenuHelper
from menuclasses import MainMenu, SubMenu

# Connect to MongoDB and set the database variables
client = MongoClient(mongodb_string)
db = client.supportStats
users = db.users
stats = db.stats


def welcome():
    while True:
        print('doodledy doo doo')
        break


def main():
    MenuHelper.generate_menu(MainMenu)
    MenuHelper.run(MainMenu)


if __name__ == '__main__':
    main()
