import os
from pathlib import Path
from bson.json_util import dumps
from tabulate import tabulate
from statbotic.title import Title


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
                raise ValueError(
                    '\n** The input did not match "y" or "n" **\n')
        except ValueError as e:
            print(e)
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
    os.system('clear')
    header = Title(title)
    header.display()

    # Print the list as a table.
    print(tabulate(table_list, tablefmt="fancy_grid", numalign="decimal"))


def create_json(data, filename):
    os.system('clear')
    full_path = os.path.dirname(os.path.abspath(__file__))
    parent_directory = Path(full_path).parent.as_posix()
    directory = f'{parent_directory}/exports/'
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as jsonf:
        json_string = dumps(data, indent=4)
        jsonf.write(json_string)
    print('\nFile successfully saved!')
    print(f'The data has been saved to: {path}')
