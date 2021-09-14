import gspread
from google.oauth2.service_account import Credentials
from termcolor import colored
import employee
import hr


# code taken from Love Sandwiches project to connect Python with the API
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')

SCOPED_CREDS = CREDS.with_scopes(SCOPE)

GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

SHEET = GSPREAD_CLIENT.open('Redundancy Applications')

# global variables used in functions reference data in google worksheet
pending_sheet = SHEET.worksheet('pending')
approved = SHEET.worksheet('approved')
rejected = SHEET.worksheet('rejected')

# welcome message displayed when file is run
welcome = colored('Welcome to the ABC voluntary redundancy calculator.',
                  'cyan', attrs=['bold'])


def get_role():
    """
    assigns an access level to a user based on whether they select
    to log in as an employee or  a representative from the Human
    Resources department
    rejects any values that are not 'employee' or 'hr'
    """
    print('\nPlease select your access level.')
    while True:
        role = input('Please enter either "e" for employee or "h" for HR:\n')
        if role.lower() == 'h':
            return 'admin'
        elif role.lower() == 'e':
            return 'basic'
        print(colored('\nInvalid input\n', 'red'))


def check_password():
    """
    if the user selects to login as HR checks that they
    know the correct password.  If the third answer fails
    user is informed that they have no more attempts left
    """
    attempts = 3
    while attempts > 0:
        password = input('\nPlease enter your password:\n')
        if password == '#MTL':
            print(colored('\nCorrect password', 'green'))
            return True
        else:
            attempts -= 1
            print(colored('\nIncorrect password', 'red'))
    print('Password attempts exhausted')
    return False


def main():
    """
    prints a welcome message to the user and calls the get_role function.
    dependent on the input provided when get_roll is called, shows the
    options for employees or checks that the user has the password to access
    the HR options and displays them if the correct password is provided
    """
    print(welcome)
    access_level = get_role()
    if access_level == 'admin':
        if check_password():
            hr.hr_main()
    if access_level == 'basic':
        employee.select_staff_option()


main()
