# Local application imports
from menuhelper import MenuHelper
from menuclasses import MainMenu, SubMenu
from stats import *


def welcome():
    print('doodledy doo doo')


def main():
    welcome()
    MenuHelper.generate_menu(MainMenu)
    loggedin = MenuHelper.run(MainMenu)
    while loggedin:
        MenuHelper.generate_menu(SubMenu)
        MenuHelper.run(SubMenu)


if __name__ == '__main__':
    main()
