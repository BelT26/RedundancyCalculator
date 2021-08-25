import math
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
            print('Please only enter numbers')
        else:
            gross_salary = int(gross_salary)
            return gross_salary


def get_length_of_service():
    while True:
        length_of_service = input('Please enter the number of complete years you have worked at Miki Travel. ')
        try:
            int(length_of_service)
        except ValueError:
            print('Please enter whole numbers only')
        else:
            print(f'You have completed {length_of_service} years')
            return int(length_of_service)


def calculate_voluntary_extra(years, weekly_pay):
    if years >= 5:
        return weekly_pay * 6
    else:
        return weekly_pay * 4


def calculate_redundancy():
    los = get_length_of_service()
    if los < 2:
        print('You must have completed at least 2 years to be entitled to redundancy')
        return
    gross_salary = get_gross_salary()
    print(gross_salary)
    weekly_salary = gross_salary/52
    rounded_weekly = round(weekly_salary, 2)
    print(f'Your weekly salary is {rounded_weekly}')
    vol_ex = calculate_voluntary_extra(los, rounded_weekly)
    print(f'Extra for voluntary {vol_ex}')


if access_level == 'basic':
    calculate_redundancy()



