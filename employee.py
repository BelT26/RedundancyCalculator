import gspread
from google.oauth2.service_account import Credentials
from termcolor import colored


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')

SCOPED_CREDS = CREDS.with_scopes(SCOPE)

GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)

SHEET = GSPREAD_CLIENT.open('Redundancy Applications')


pending_sheet = SHEET.worksheet('pending')
approved = SHEET.worksheet('approved')
rejected = SHEET.worksheet('rejected')


def is_integer():
    while True:
        num = input('Please enter numbers only\n')      
        try:
            int(num)
        except ValueError:
            print(colored('Invalid input', 'red'))
        else:
            return int(num)
          

def get_gross_salary():
    """
    asks the user for their salary and checks that a numerical answer is
    provided
    """
    print('\nPlease input your gross annual salary.')
    print('For example 29000')
    gross_salary = is_integer()
    return gross_salary
    

def get_length_of_service():
    """
    asks the user for their length of service
    checks that a numerical answer is provided
    """
    while True:
        print('Please enter the number of years you have worked at ABC.')
        length_of_service = is_integer()
        return length_of_service


def get_age():
    """
    asks the user for their age and checks that a numerical answer is provided
    """
    while True:
        print('\nPlease enter your age on 4/10/21')
        user_age = is_integer()
        return user_age


def calculate_voluntary_extra(years_service, weekly_pay):
    """
    calculates the extra tax free payment that will be made if the user opts
    for voluntary redundancy
    """
    if years_service >= 5:
        return round(weekly_pay * 4, 2)
    else:
        return round(weekly_pay * 2, 2)


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


def get_cf_holidays():
    """
    asks the user for any holidays carried forward from the previous year and
    checks a number is provided
    """
    while True:
        print('\nPlease enter the number of holidays carried over from July 2021')
        print('Refer to the CF column of your dashboard.')
        cf_holidays = is_integer()
        return cf_holidays


def get_bought_holidays():
    """
    asks the user for any holidays bought and checks a number is provided
    """
    while True:
        print('\nPlease enter the number of extra holidays allocated in 2020')
        print('Refer to the "bought" column of your dashboard.')
        bought_hols = is_integer()
        return bought_hols


def get_taken_hols():
    """
    asks the user for any holidays taken since the start of the financial year
    and checks a number is provided
    """
    while True:
        print('\nPlease enter the number of holidays taken since 1/8/21')
        print('Refer to the "taken" column of your dashboard.')
        taken_hols = is_integer()
        return taken_hols


def get_booked_hols():
    """
    asks the user for any holidays booked to be taken before the end of
    the consultation period and checks that a number is provided
    """
    while True:
        print('\nEnter the number of holidays booked to be taken by 4/10/21')
        print('Refer to the booked column of your dashboard.')     
        booked_hols = is_integer()
        return booked_hols


def calculate_holidays(length_of_service):
    """
    calculates the number of unused holidays that the user should be paid for
    """
    holiday_entitlement = max((22 + length_of_service), 26)
    current_year_entitlement = holiday_entitlement * (9 / 52)
    cf_holidays = get_cf_holidays()
    bought_hols = get_bought_holidays()
    hols_taken = get_taken_hols()
    hols_booked = get_booked_hols()
    rem_holidays = cf_holidays + min((bought_hols - hols_taken - hols_booked), 0) + current_year_entitlement
    print(f'Total outstanding holidays: {round(rem_holidays, 2)} days/n')
    return round(rem_holidays, 2)


def calculate_holiday_pay(num_holidays, salary):
    """
    returns the holiday pay due by dividing the annual salary by the
    number of weeks in the year multiplied by the number of working days
    per week and then multiplying the figure by the number of holidays
    owed
    """
    return round(num_holidays * salary / (52 * 5), 2)


def get_overtime_hours():
    """
    checks that the user inserts a valid number
    caps the overtime at 75 hours
    """
    while True:
        print('\nPlease enter the excess hours showing on your dashboard')
        print('Enter a negative figure if time owed is less than 0')
        excess_hours = input('Please enter only the hours:\n')
        try:
            int(excess_hours)
        except ValueError:
            print('Please enter whole numbers only')
        else:
            if int(excess_hours) > 75:
                print(colored('\nThe maximum amount of overtime payable is 75 hours', 'red'))
            else:
                return int(excess_hours)


def get_overtime_minutes():
    """
    checks that the user inserts a valid number between 0 & 60
    converts the minutes into a fraction of an hour
    """
    while True:
        print('\nPlease enter the excess minutes showing on your dashboard')
        print('Please enter a negative figure if time owed is less than 0')
        excess_minutes = input('Excess minutes:\n')
        try:
            int(excess_minutes)
        except ValueError:
            print('Please enter a number')
        else:
            if int(excess_minutes) > 59 or int(excess_minutes) < -59:
                print(colored('\nThe number of minutes cannot exceed 59', 'red'))
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


name = ''
staff_data = []


def add_to_pending():
    """
    checks that a redundancy application has not already been submitted.
    advises the user of the application status if an application has already
    been made, otherwise asks the user to enter their department, pushes the
    name and department to staff_data and adds staff_data to the applications
    worksheet
    """
    global name
    global pending_sheet
    pending_names = SHEET.worksheet('pending').col_values(1)
    approved_names = SHEET.worksheet('approved').col_values(1)
    rejected_names = SHEET.worksheet('rejected').col_values(1)
    received = colored('An application in your name has already been submitted.','yellow')
    contact = colored('Please contact HR for further queries/n', 'yellow')
    if name in pending_names:
        print(received)
        print('It is currently under review')
        print(contact)
        exit()
    elif name in approved_names:
        print(received)
        print('It has already been approved')
        print(contact)
        exit()
    elif name in rejected_names:
        print(received)
        print('Your application has been rejected')
        print(contact)
        exit()
    else:
        department = input('Please enter your department:\n')
        staff_data.insert(0, name)
        staff_data.insert(1, department)
        pending_sheet.append_row(staff_data)
        print(colored('\nThank you. Application submitted', 'yellow'))
        print(colored('You will receive a response within 5 working days\n', 'yellow'))


def validate_payroll_num():
    """
    checks the staff worksheet to ensure that the name and payroll
    number entered match the details stored
    """
    global name
    staff = SHEET.worksheet('staff').col_values(1)
    pay_nums = SHEET.worksheet('staff').col_values(2)
    name_attempts = 3
    while name_attempts > 0:
        name = input('\nPlease enter your full name:\n')
        name = name.upper()
        if name in staff:
            name_ind = staff.index(name)
            payroll_attempts = 3
            while payroll_attempts > 0:
                payroll = input('\nPlease enter your payroll number:\n')
                if payroll == pay_nums[name_ind]:
                    print(colored('Access granted\n', 'green'))
                    add_to_pending()
                    break
                else:
                    payroll_attempts -= 1
                    print(colored('\nIncorrect payroll number.', 'red'))
            if payroll_attempts == 0:
                print(colored('Attempts exhausted. Access refused\n', 'red'))
                exit()
        else:
            name_attempts -= 1
            print(colored('Invalid name', 'red'))
    if name_attempts == 0:
        print(colored('Attempts exhausted. Access refused\n', 'red'))
        exit()


def check_if_applying():
    print('Do you wish to proceed with your application?')
    while True:
        apply = input('Please enter Y or N:\n')
        if apply.lower() == 'y':
            validate_payroll_num()
            break
        elif apply.lower() == 'n':
            print('\nApplication not processed')
            print('The information provided has not been stored.\n')
            exit()
        else:
            print(colored('Invalid input', 'red'))


def calculate_redundancy():
    los = get_length_of_service()
    if los < 2:
        print('You must have completed at least 2 years for redundancy.\n')
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
    vol_red = round(vol_ex + statutory + lieu + holiday_pay + overtime - tax, 2)
    total_gross = round(vol_ex + statutory + lieu + holiday_pay + overtime, 2)
    print(colored('\nYour redundancy has been calculated:\n', 'white', attrs=['bold']))
    print('=' * 54)
    print(f'\nExtra payment for voluntary redundancy: {vol_ex}')
    print(f'Statutory redundancy: {statutory}')
    print(f'Pay in lieu of notice: {lieu}')
    print(f'Unused holidays: {holiday_pay}')
    print(f'Overtime: {overtime}')
    print(f'Gross: {total_gross}')
    print(f'Total tax deductable: {tax}\n')
    print('=' * 54)
    print(colored(f'\nYou would receive {vol_red} for voluntary redundancy.\n', 'yellow', attrs=['bold']))
    global staff_data
    staff_data.extend((gross_salary, statutory, vol_ex, lieu, holiday_pay, overtime, tax, vol_red))
    check_if_applying()


def display_calc_message():
    text1 = colored('\nPlease ensure you have your payroll number and access to', 'yellow', attrs=['bold'])
    text2 = colored('your time and attendance dashboard.\n', 'yellow', attrs=['bold'])
    print(text1)
    print(text2)
    calculate_redundancy()


def view_status():
    global name
    name = input('Please enter your full name:\n')
    staff = SHEET.worksheet('staff').col_values(1)
    pending_names = SHEET.worksheet('pending').col_values(1)
    approved_names = SHEET.worksheet('approved').col_values(1)
    rejected_names = SHEET.worksheet('rejected').col_values(1)
    pay_nums = SHEET.worksheet('staff').col_values(2)
    if name in staff:
        name_ind = staff.index(name)
        payroll = input('Please enter your payroll number:\n')
        if payroll == pay_nums[name_ind]:
            access = colored('Access granted', 'green')
            print(access)
            if name in pending_names:
                print('Your application is currently under review.')
                exit()
            elif name in approved_names:
                print('Your application has been approved')
                exit()
            elif name in rejected_names:
                print('Your application has been rejected')
                exit()
            else:
                print('Your application has not been received')
                print('Would you like to submit an application?')
                apply = input('Please enter Y or N:\n')
                if apply.lower() == 'y':
                    calculate_redundancy()
                print('Please contact HR for further queries\n')
        else:
            inc_pay = colored('Incorrect payroll number. Access refused', 'red')
            print(inc_pay)
            exit()
    else:
        inv_name = colored('Invalid name. Access refused', 'red')
        print(inv_name)


def select_staff_option():
    while True:
        print('\nPlease select from the following options')
        print('1. Calculate redundancy')
        print('2. View application status')
        print('Enter Q to quit\n')
        staff_choice = input('Enter the option number here:\n')
        if staff_choice == '1':
            display_calc_message()
            break
        elif staff_choice == '2':
            view_status()
            break
        elif staff_choice.lower() == 'q':
            print(colored('\nYou have successfully logged out\n', 'yellow'))
            exit()
        else:
            print('You must select from the available options')
