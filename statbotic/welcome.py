from clint.textui import colored
from pyfiglet import Figlet


def welcome(string):
    """
    PyFiglet and coloured string conversion
    """
    result = Figlet()
    return colored.cyan(result.renderText(string))


def stats_bot():
    """
    Displays an ascii robot.
    """
    bot = r'''                 ___T_
                | O O |
                |__u__|
              (m9\:::/\
                 /___\6
                  |_|
                 (ooo)
    '''
    return bot
