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


def logout():
    """
    displays a message to the user that they have been logged out and
    exits the programme
    """
    print(colored('\nYou have successfully logged out.\n', 'yellow'))
    exit()


def show_hr_menu():
    """
    asks the user to choose between three actions and returns the
    choice if valid input is provided
    """
    while True:
        print('\nPlease select from the following options:\n')
        print('1. View / authorise pending applications')
        print('2. View authorised applications')
        print('3. View rejected applications\n')
        choice = input('Please enter 1, 2 or 3 or Q to quit \n')
        if choice in ('1', '2', '3'):
            return choice
        elif choice.lower() == 'q':
            logout()
        print(colored('invalid option\n', 'red'))


def next_action():
    """
    provides the user with the option to exit the programme or return to 
    the main HR menu
    """
    while True:
        next = input('Enter Q to quit. M to return to main menu \n')
        if next.lower() == 'q':
            logout()
        elif next.lower() == 'm':
            break
        print(colored('Invalid input', 'red\n'))


def authorise(data):
    """
    deletes an application from the applications worksheet and adds it to the
    approved worksheet
    """
    global approved
    global pending_sheet
    approved.append_row(data)
    pending_sheet.delete_rows(2)
    print(colored('\nApplication authorised.\n', 'blue'))


def reject_appl(data):
    """
    deletes an application from the applications worksheet and adds it to the
    rejected worksheet
    """
    global rejected
    global pending_sheet
    rejected.append_row(data)
    pending_sheet.delete_rows(2)
    print(colored('\nApplication rejected.', 'blue'))


# variables used in the view pending and check pending functions
pend_app_ind = 1
pending = pending_sheet.get_all_values()
num_pending = len(pending)-1


def view_pending():
    """
    allows the user to view each application that is yet to be approved
    or rejected in turn.  Details of each application are displayed by zipping
    together the headings on the application worksheet with the row containing
    the info about the application.  The user has the opportunity to approve or
    reject each request.  If they do so the application is then moved to either
    the approved or the rejected worksheet.  If they choose to do neither the
    pend_app_ind  and num_pending variables are updated so that the next
    application is displayed
    """
    global pending_sheet
    global pending
    global pend_app_ind
    global num_pending
    headings = pending[0]
    first_appl = pending[pend_app_ind]
    for head, app in zip(headings, first_appl):
        print(f'{head}:{app}')
    print('\nDo you wish to approve this application?')
    approve = input('Please enter Y or N. Enter Q to quit:\n')
    if approve.lower() == 'y':
        authorise(first_appl)
    elif approve.lower() == 'q':
        logout()
    elif approve.lower() == 'n':
        print('\nDo you wish to reject this application?')
        reject = input('Please enter Y or N:\n')
        if reject.lower() == 'y':
            reject_appl(first_appl)
        elif reject.lower() == 'n':
            print(colored('\nApplication not yet processed.', 'blue'))
            pend_app_ind += 1
            num_pending -= 1
    if num_pending > 0:
        print('Next application pending approval:\n')
        view_pending()
    else:
        print('No more pending applications')
        next_action()


appr_ind = 1


def view_approved():
    """
    allows the user to view details of applications that have been approved.
    after viewing each application the user is offered the possibility of
    exiting the application or returning to the main menu if they do not wish
    to carry on viewing the applications.
    """
    global approved
    global appr_ind
    appr = approved.get_all_values()
    headings = appr[0]
    first_appl = appr[appr_ind]
    for head, app in zip(headings, first_appl):
        print(f'{head}:{app}')
    while True:
        view_next = input('\nPress N to view next, Q to quit, M for main menu.\n')
        if view_next.lower() == 'q':
            logout()
        elif view_next.lower() == 'n':
            appr_ind += 1
            if appr_ind < len(appr):
                print('Next approved application: \n')
                view_approved()
            else:
                print('No more approved applications to view \n')
                next_action()
                break
        elif view_next.lower() == 'm':
            break
        else:
            print(colored('Invalid input', 'red\n'))


rej_ind = 1


def view_rejected():
    """
    allows the user to view details of applications that have been rejected.
    after viewing each application the user is offered the possibility of
    exiting the application or returning to the main menu if they do not wish
    to carry on viewing the applications.
    """
    global rejected
    global rej_ind
    rej = rejected.get_all_values()
    headings = rej[0]
    first_appl = rej[rej_ind]
    for head, app in zip(headings, first_appl):
        print(f'{head}:{app}')
    while True:
        view_next = input('\nPress N to view next. Q to quit. M for main menu\n')
        if view_next.lower() == 'q':
            logout()
        elif view_next.lower() == 'n':
            rej_ind += 1
            if rej_ind < len(rej):
                view_rejected()
            else:
                print('No more rejected applications to view')
                next_action()
        elif view_next.lower() == 'm':
            break
        else:
            print(colored('Invalid input', 'red\n'))


def check_worksheet(status):
    """
    checks the selected worksheet and lets the user know the total
    number of applications on it. If there are no applications the user is 
    provided with the option to quit or return to the main menu otherwise
    the appropriate function is called to enable the user to view full
    details of the selected type of applications
    """
    status_data = SHEET.worksheet(status).get_all_values()
    num_apps = len(status_data)-1
    print(f'\n{num_apps} {status} application(s)')
    if num_apps > 0:
        print(f'First {status} application: \n')
        if status == 'rejected':
            view_rejected()
        elif status == 'approved':
            view_approved()
        elif status == 'pending':
            view_pending()
    else:
        print(f'No {status} applications\n')
        next_action()


def hr_main():
    """
    processes the choice returned from show_hr_menu by calling the
    check_worksheet function and passing in the appropriate argument.
    once the action has been completed allows the user to select
    their next action
    """
    while True:
        choice = show_hr_menu()
        if choice == '1':
            check_worksheet('pending')
        elif choice == '2':
            check_worksheet('approved')
        elif choice == '3':
            check_worksheet('rejected')
    next_action()
