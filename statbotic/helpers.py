import os
from pathlib import Path
from bson.json_util import dumps
from tabulate import tabulate
from statbotic.title import Title


def user_continue(question):
    """
    Ask the user if they'd like to continue the current action.

    * @args(str) question -- passed from parent function.
    * @raises(ValueError) -- when input does not match y or n.
    * @return(bool) -- true for y, false for n.
    """
    while True:
        # Ask the question.
        user_input = input(question)
        try:
            # Convert the user input to lowercase.
            user_input.lower()
            # Check if user input either y or n.
            # Raise error if not, else return boolean.
            if user_input not in ('y', 'n'):
                raise ValueError(
                    '\n** The input did not match "y" or "n" **\n')
        except ValueError as e:
            print(e)
        else:
            return True if user_input == 'y' else False


def create_lists(data):
    """
    Convert MondoDB cursor object into a temp list.
    Move keys to one list, and values to another.

    * @arg(cursor) data -- passed from view_stats().
    * @return(list) key_list -- list of data keys.
    * @return(list) stats_list -- list of data values.
    """
    # Convert cursor object to a list.
    temp_list = list(data)
    # Create two empty lists.
    stats_list = []
    key_list = []
    for i in temp_list:
        # Move values to stats_list
        for value in i.values():
            if value != "null":
                stats_list.append(value)
        # Move keys to key_list
        for key in i.keys():
            if key != "_id":
                key_list.append(key)
    return key_list, stats_list


def print_stats(title, data):
    """
    Create a table of stats for the given date range.

    * @arg(str) title -- passed from view_stats().
    * @arg(list) data -- passed from view_stats().
    """
    # Convert the stats values to rounded floats to help table alignment.
    stats_list = [float(x) for x in data[1]]
    stats_list = [round(x, 1) for x in data[1]]
    # Merge the lists for tabulate.
    table_list = [list(x) for x in zip(data[0], stats_list)]

    # Make space and generate the header.
    os.system('clear')
    header = Title(title)
    header.display()

    # Print the list as a table.
    print(tabulate(table_list, tablefmt="fancy_grid", numalign="decimal"))


def create_json(data, filename):
    """
    Find path to exports directory.
    Save exported data to JSON file.

    * @arg(list) data -- passed from export_stats().
    * @arg(str) filename -- passed from export_stats().
    """
    os.system('clear')
    # Find the full path to the current directory, then it's parent.
    full_path = os.path.dirname(os.path.abspath(__file__))
    parent_directory = Path(full_path).parent.as_posix()
    # Create a path to the exports directory.
    directory = f'{parent_directory}/exports/'
    # Add the directory path to the filename.
    path = os.path.join(directory, filename)
    # Export the data and save to a JSON file.
    with open(path, 'w', encoding='utf-8') as jsonf:
        json_string = dumps(data, indent=4)
        jsonf.write(json_string)
    # User feedback when complete.
    print('\nFile successfully saved!')
    print(f'The data has been saved to: {path}')
