import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')

SCOPED_CREDS = CREDS.with_scopes(SCOPE)

GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

SHEET = GSPREAD_CLIENT.open('Redundancy Applications')

applications = SHEET.worksheet('applications')

data = applications.get_all_values()

print('Welcome to the Miki Travel Voluntary redundancy calculator.')


def get_role():
    while True:
        role = input('Would you like to login as staff or HR? ')
        if role.lower() == 'hr':
            return 'admin'
        elif role.lower() == 'staff':
            return 'basic'
        print('You must select either staff or HR')


access_level = get_role()

print(f"You have selected {access_level} access")


def check_password():
    attempts = 3
    while attempts > 0:
        password = input('Please enter your password to access the redundancy database: ')
        if password == '#MTL':
            print('correct password')
            break
        else:
            attempts -= 1
            print('incorrect password')
    print('Password attempts exhausted')


if access_level == 'admin':
    check_password()


def get_gross_salary():
    while True:
        gross_salary = input('Please input your gross annual salary. Eg 29000. ')
        try:
            int(gross_salary)
        except ValueError:
            print('You must only input numbers')
        else:
            gross_salary = int(gross_salary)
            return gross_salary


if access_level == 'basic':
    gross_salary = get_gross_salary()
    print(gross_salary)
