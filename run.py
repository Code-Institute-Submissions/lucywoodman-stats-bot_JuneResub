# Third party imports
import pyfiglet

# Local application imports
from menus import Menu, Main, Sub


def welcome():
    ascii_banner = pyfiglet.figlet_format("Stats Bot!!")
    bot = r"""
         ___T_     
        | O O |    
        |__u__|    
      (m9\:::/\    
         /___\6    
          |_|      
         (ooo)
    """
    print('=' * 80)
    print('WELCOME TO:')
    print(ascii_banner + bot)


def main():
    welcome()
    Menu.generate_menu(Main)
    loggedin = Menu.run(Main)
    while loggedin:
        Menu.generate_menu(Sub)
        Menu.run(Sub)


if __name__ == '__main__':
    main()
