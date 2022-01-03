# Third party imports
import os
from pymongo import MongoClient

# Local application imports
if os.path.exists('settings.py'):
    from settings import username, password, mongodb_string

client = MongoClient(mongodb_string)

db = client.gettingStarted
people = db.people

personDocument = {
    "name": {"first": "Alan", "last": "Turing"},
    "contribs": ["Turing machine", "Turing test", "Turingery"],
    "views": 1250000
}

people.insert_one(personDocument)
person = people.find_one({"name.last": "Turing"})
print(person)
