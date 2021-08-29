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
        password = input('Please enter your password: ')
        if password == '#MTL':
            print('correct password')
            return True
        else:
            attempts -= 1
            print('incorrect password')
    print('Password attempts exhausted')
    return False

pending = SHEET.worksheet('applications').get_all_values()
headings = pending[0]
first_appl = pending[1]
approved = SHEET.worksheet('approved')

def view_pending():
    global pending
    global headings
    global first_appl
    for head, app in zip(headings, first_appl):
        print(f"{head}: {app}")
    print('Do you wish to approve this application?')
    approve = input('Please enter Y or N: ')
    if approve.lower() == 'y':
        authorise(first_appl)
    else:
        print('Do you wish to reject this application?')
        reject = input('Please enter Y or N')
        if reject.lower() == 'y':
            reject(first_appl)


def authorise(data):
    global approved
    print('Authorising application.')
    approved.append_row(data)
    pending.batch_clear(first_appl)


def reject(data):
    print('Rejecting application.')
    rejection_worksheet = SHEET.worksheet('rejected')
    rejection_worksheet.append_row(data)





if access_level == 'admin':
    if check_password():
        pending = SHEET.worksheet('applications').get_all_values()
        num_pending = len(pending)-1
        print(f'{num_pending} application(s) pending approval')
        print('Do you wish to view the pending application(s)?')
        while True:
            view = input('Please enter Y or N')
            if view.lower() == 'y':
                print('First pending application:')
                view_pending()
                break
            elif apply.lower() == 'n':
                print('Would you like to access other data?')
                break
            else:
                print('You must enter Y or N')


def get_gross_salary():
    """
    asks the user for their salary and checks that a numerical answer is
    provided
    """
    while True:
        print('Please input your gross annual salary.')
        gross_salary = input('Enter numbers only. EG 29000: ')
        try:
            int(gross_salary)
        except ValueError:
            print('Please only enter numbers')
        else:
            gross_salary = int(gross_salary)
            return gross_salary


def get_length_of_service():
    """
    asks the user for their length of service
    checks that a numerical answer is provided
    """
    while True:
        print('Please enter the number of years you have worked at MTL.')
        length_of_service = input('Number of years: ')
        try:
            int(length_of_service)
        except ValueError:
            print('Please enter whole numbers only.')
        else:
            return int(length_of_service)


def get_age():
    """
    asks the user for their age and checks that a numerical answer is provided
    """
    while True:
        print('Please enter your age on 7/10/21')
        user_age = input('Age: ')
        try:
            int(user_age)
        except ValueError:
            print('Please enter whole numbers only')
        else:
            return int(user_age)


def calculate_voluntary_extra(years_service, weekly_pay):
    """
    calculates the extra tax free payment that will be made if the user opts
    for voluntary redundancy
    """
    if years_service >= 5:
        return round(weekly_pay * 6, 2)
    else:
        return round(weekly_pay * 4, 2)


def calculate_statutory(age, years_service, weekly_pay):
    """
    calculates the statutory redundancy pay
    caps the max weekly pay at 544 and the max years considered at 20
    calculates the number of weeks entitlement based on the user's age during
    each year of service
    """
    if weekly_pay >= 544:
        weekly_stat = 544
    else:
        weekly_stat = weekly_pay
    if years_service >= 20:
        statutory_years = 20
    else:
        statutory_years = years_service
    starting_age = age - statutory_years
    low_rate_yrs = 0
    if starting_age < 22:
        low_rate_yrs = 22 - starting_age
    high_rate_yrs = 0
    if age > 41:
        high_rate_yrs = min(age-41, statutory_years)
    std_rate_yrs = 0
    if starting_age < 41:
        if starting_age > 22:
            std_rate_yrs = min(41 - starting_age, statutory_years)
        elif age > 41:
            std_rate_yrs = statutory_years - high_rate_yrs
        else:
            std_rate_yrs = min(41 - 22, statutory_years - low_rate_yrs)
    # print(f'lower rate years: {low_rate_yrs}')
    # print(f'standard years: {std_rate_yrs}')
    # print(f'higher rate years: {high_rate_yrs}')
    years = (low_rate_yrs * 0.5) + std_rate_yrs + (high_rate_yrs * 1.5)
    stat_pay = weekly_stat * years
    return stat_pay


def calculate_pay_in_lieu(salary, years_service):
    """
    returns the amount of pay the user would receive in lieu of notice
    if the years worked are 5 or more, returns 1 week's pay per year
    if the years worked are less than 5 defaults to 1 month's pay
    """
    if years_service > 4:
        return round((salary / 52) * years_service, 2)
    return round((salary / 12), 2)


def calculate_holidays(length_of_service):
    """
    calculates the number of unused holidays that the user should be paid for
    """
    holiday_entitlement = max((22 + length_of_service), 26)
    current_year_entitlement = holiday_entitlement * (10 / 52)
    print('Please enter the number of holidays carried over from July 2021')
    cf_holidays = int(input('Refer to the CF column of your dashboard: '))
    print('Please enter the number of extra holidays allocated in 2020')
    bought_hols = int(input('Refer to the bought column of your dashboard: '))
    print('Please enter the number of holidays taken since 1/8/21')
    hols_taken = int(input('Refer to the taken column of your dashboard: '))
    print('Please enter the number of holidays booked to be taken by 30/9/21')
    hols_booked = int(input('Refer to the booked column of your dashboard: '))
    rem_holidays = cf_holidays + min((bought_hols - hols_taken - hols_booked), 0) + current_year_entitlement
    return round(rem_holidays, 2)


def calculate_holiday_pay(num_holidays, salary):
    return round(num_holidays * salary / (52 * 5), 2)


def get_overtime_hours():
    """
    checks that the user inserts a valid number
    caps the overtime at 75 hours
    """
    while True:
        print('Please enter the excess hours showing on your dashboard')
        excess_hours = input('Please enter only complete hours: ')
        try:
            int(excess_hours)
        except ValueError:
            print('Please enter whole numbers only')
        else:
            if int(excess_hours) > 75:
                print('The maximum number of overtime payable is 75 hours')
            else:
                return int(excess_hours)


def get_overtime_minutes():
    """
    checks that the user inserts a valid number between 0 & 60
    converts the minutes into a fraction of an hour
    """
    while True:
        print('Please enter the excess minutes showing on your dashboard')
        print('Please enter a negative figure if time owed is less than 0')
        excess_minutes = input('Excess minutes: ')
        try:
            int(excess_minutes)
        except ValueError:
            print('Please enter a number')
        else:
            if int(excess_minutes) > 59:
                print('The number of minutes cannot exceed 59')
            elif int(excess_minutes) == 0:
                return 0
            else:
                return int(excess_minutes) / 60


def calculate_overtime_payment(salary):
    """
    calculates the overtime payment due based on the validated number
    of hours and minutes returned by get_overtime_hours and
    get_overtime_minutes functions.
    the standard working week is 37.5 hours
    """
    hours = get_overtime_hours()
    if hours == 75:
        minutes = 0
    else:
        minutes = get_overtime_minutes()
    total_time = hours + minutes
    overtime_payment = salary / (52*37.5) * total_time
    return overtime_payment


def calculate_tax(salary, overtime, pay_in_lieu, holidays):
    standard_rate_tax = 0
    higher_rate_tax = 0
    highest_rate_tax = 0
    taxable_sum = (salary/12) + overtime + pay_in_lieu + holidays - (12570/12)
    if taxable_sum < 0:
        return 0
    elif taxable_sum < (37700/12):
        standard_rate_tax = taxable_sum * 0.2
        return standard_rate_tax
    else:
        standard_rate_tax = (37700/12) * 0.2
        if taxable_sum < (137430/12):
            higher_rate_tax = (taxable_sum - 37700/12) * 0.4
            return standard_rate_tax + higher_rate_tax
        else:
            higher_rate_tax = (99730/12) * 0.4
            highest_rate_tax = (taxable_sum - 137430/12) * 0.45
            return standard_rate_tax + higher_rate_tax + highest_rate_tax


staff_data = []


def calculate_redundancy():
    los = get_length_of_service()
    if los < 2:
        print('You must have completed at least 2 years for redundancy.')
        exit()
    gross_salary = get_gross_salary()
    weekly_salary = gross_salary/52
    vol_ex = round(calculate_voluntary_extra(los, weekly_salary), 2)
    staff_age = get_age()
    statutory = round(calculate_statutory(staff_age, los, weekly_salary), 2)
    lieu = calculate_pay_in_lieu(gross_salary, los)
    num_hols = calculate_holidays(los)
    holiday_pay = calculate_holiday_pay(num_hols, gross_salary)
    overtime = round(calculate_overtime_payment(gross_salary), 2)
    tax = round(calculate_tax(gross_salary, overtime, lieu, holiday_pay), 2)
    std_red = round(statutory + lieu + holiday_pay + overtime - tax, 2)
    vol_red = std_red + vol_ex
    print(f'\nEx gratia payment for voluntary redundancy: {vol_ex}')
    print(f'Statutory redundancy: {statutory}')
    print(f'Pay in lieu of notice: {lieu}')
    print(f'Unused holidays: {holiday_pay}')
    print(f'Overtime: {overtime}')
    print(f'Total tax deductable: {tax}\n')
    print(f'You would receive {vol_red} for voluntary redundancy.')
    print(f'Your non-voluntary redundancy payment would be {std_red}.\n')
    global staff_data
    staff_data.extend((gross_salary, statutory, vol_ex, lieu, holiday_pay, overtime, tax, vol_red, 'pending'))


def check_if_applying():
    print('Do you wish to proceed with your application?')
    while True:
        apply = input('Please enter Y or N: ')
        if apply.lower() == 'y':
            print('Processing application')
            return True
        elif apply.lower() == 'n':
            print('Application not processed')
            return False
        else:
            print('You must enter Y or N')


def update_applications_worksheet(data):
    print('Updating worksheet')
    applications_worksheet = SHEET.worksheet('applications')
    applications_worksheet.append_row(data)


if access_level == 'basic':
    print('Please ensure you have your payroll number and access to your')
    print('time and attendance records. \n')
    calculate_redundancy()
    application = check_if_applying()
    if application:
        name = input('Please enter your full name: ')
        department = input('Please enter your department: ')
        staff_data.insert(0, name)
        staff_data.insert(1, department)
        update_applications_worksheet(staff_data)
