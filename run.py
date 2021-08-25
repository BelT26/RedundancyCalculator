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
    """
    assigns an access level to a user based on whether they select
    to log in as a staff member or  a representative from the Human 
    Resources department
    rejects any values that are not 'staff' or 'hr'
    """
    while True:
        role = input('Would you like to login as staff or HR? ')
        if role.lower() == 'hr':
            return 'admin'
        elif role.lower() == 'staff':
            return 'basic'
        print('You must select either staff or HR')


access_level = get_role()


def check_password():
    """
    if the user selects to login as HR checks that they
    know the correct password.  If the third answer fails
    user is informed that they have no more attempts left
    """
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
    """
    asks the user for their salary and checks that a numerical answer is provided
    """
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
    """
    asks the user for their length of service and checks that a numerical answer is provided
    """
    while True:
        length_of_service = input('Please enter the number of complete years you have worked at Miki Travel. ')
        try:
            int(length_of_service)
        except ValueError:
            print('Please enter whole numbers only')
        else:
            return int(length_of_service)


def get_age():
    """
    asks the user for their age and checks that a numerical answer is provided
    """
    while True:
        user_age = input('Please enter your age on 7/10/21 ')
        try:
            int(user_age)
        except ValueError:
            print('Please enter whole numbers only')
        else:
            return int(user_age)


def calculate_voluntary_extra(years_service, weekly_pay):
    """
    calculates the extra tax free payment that will be made if the user opts for
    voluntary redundancy
    """
    if years_service >= 5:
        return round(weekly_pay * 6, 2)
    else:
        return round(weekly_pay * 4, 2)


def calculate_statutory(age, years_service, weekly_pay):
    """
    calculates the statutory redundancy pay
    caps the max weekly pay at 544 and the max years considered at 20
    calculates the number of weeks entitlement based on the user's age during each
    year of service
    """
    if weekly_pay >= 544:
        weekly_statutory = 544
    else:
        weekly_statutory = weekly_pay
    if years_service >= 20:
        statutory_years = 20
    else:
        statutory_years = years_service
    starting_age = age - statutory_years
    lower_rate_years = 0
    if starting_age < 22:
        lower_rate_years = 22 - starting_age
    print(f'lower rate years: {lower_rate_years}')
    standard_rate_years = 0
    if starting_age < 41:
        if starting_age > 22:
            standard_rate_years = min(41 - starting_age, years_service)
        else:
            standard_rate_years = min(41 - 22, years_service)
    print(f'standard years: {standard_rate_years}')
    higher_rate_years = 0
    if age > 40:
        higher_rate_years = min(age-40, years_service)
    print(f'higher rate years: {higher_rate_years}')
    statutory_pay = weekly_statutory * ((lower_rate_years * 0.5) + standard_rate_years + (higher_rate_years * 1.5))
    print(f'Your statutory redundancy pay is {statutory_pay}')


def calculate_holidays(length_of_service):
    """
    calculates the number of unused holiday days that the user should be paid for
    """
    holiday_entitlement = max((22 + length_of_service), 26)
    current_year_entitlement = holiday_entitlement * (10 / 52)
    cf_holidays = int(input('Please enter the number of holidays carried over from July 2021'))
    bought_holidays = int(input('Please enter the number of holidays appearing in the "bought" column'))
    cy_holidays = int(input('Please enter the number of holidays taken since August 1st 2021'))
    rem_holidays = cf_holidays + min((bought_holidays - cy_holidays), 0) + current_year_entitlement
    return rem_holidays

def get_overtime_hours():
    """
    checks that the user inserts a valid number
    caps the overtime at 75 hours
    """
    while True: 
        excess_hours = input('Please enter the number of hours only showing on your T&A record')
        try:
            int(excess_hours)
        except ValueError:
            print('Please enter whole numbers only')
        else:
            if int(excess_hours > 75):
                print('The maximum number of overtime payable is 75 hours')
            return int(excess_hours)

def get_overtime_minutes():
    """
    checks that the user inserts a valid number between 0 & 60
    converts the minutes into a fraction of an hour
    """
    while True: 
        excess_minutes = input('Please enter the number of excess minutes showing on your T&A record')
        try:
            int(excess_minutes)
        except ValueError:
            print('Please enter a number')
        else:
            if int(excess_minutes > 59):
                print('The number of minutes cannot exceed 59')
            return int(excess_minutes) * (100 / 60)


def calculate_overtime_payment(salary):
    total_time = get_overtime_hours + get_overtime_minutes
    overtime_payment = salary / (52*37.5) * total_time
    return overtime_payment


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
    staff_age = get_age()
    calculate_statutory(staff_age, los, rounded_weekly)
    num_hols = calculate_holidays(los)
    print(f'You have {num_hols} unused holiday days')


if access_level == 'basic':
    calculate_redundancy()

