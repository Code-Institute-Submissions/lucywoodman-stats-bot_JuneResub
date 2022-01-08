# Local application imports
from menuhelper import MenuHelper
from menuclasses import MainMenu, SubMenu
from stats import *


def welcome():
    while True:
        print('doodledy doo doo')
        break


def main():
    MenuHelper.generate_menu(MainMenu)
    loggedin = MenuHelper.run(MainMenu)
    if loggedin:
        MenuHelper.generate_menu(SubMenu)
        MenuHelper.run(SubMenu)


if __name__ == '__main__':
    # main()
    yesterday_stats()
