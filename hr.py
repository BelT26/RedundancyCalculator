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

pending_sheet = SHEET.worksheet('applications')
approved = SHEET.worksheet('approved')
rejected = SHEET.worksheet('rejected')


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
            print(colored('\nYou have successfully logged out.\n', 'yellow'))
            exit()
        print(colored('invalid option\n', 'red'))


def next_action():
    """
    provides the user with the option to exit the programme or return to 
    the main HR menu
    """
    while True:
        next = input('Enter Q to quit. M to return to main menu \n')
        if next.lower() == 'q':
            print(colored('\nYou have successfully logged out.\n', 'yellow'))
            exit()
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
        print(colored('\nYou have successfully logged out.\n', 'yellow'))
        exit()
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


def check_pending():
    """
    checks the applications worksheet to see how many applications
    have yet to be rejected or approved and lets the user know how
    many there are.  If there are no pending applications the user
    is provided with the option to quit or return to the main menu
    otherwise the view_pending function is called to allow the user
    to view the applications
    """
    global pending
    global num_pending
    print(f'\n{num_pending} application(s) pending approval')
    if num_pending > 0:
        print('Retrieving details of first pending application... \n')
        view_pending()
    else:
        print('No pending applications')
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
            print(colored('\nYou have successfully logged out.\n', 'yellow'))
            exit()
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


def check_approved():
    """
    checks the approved worksheet to see how many applications
    have been approved and lets the user know the total.
    If there are no approved applications the user is provided
    with the option to quit or return to the main menu otherwise
    the view_approved function is called to allow the user
    to view the applications
    """
    approved = SHEET.worksheet('approved').get_all_values()
    num_approved = len(approved)-1
    print(f'\n{num_approved} approved application(s)')
    if num_approved > 0:
        print('First application: \n')
        view_approved()
    else:
        print('No approved applications')
        next_action()


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
            print(colored('\nYou have successfully logged out.\n', 'yellow'))
            exit()
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


def check_rejected():
    """
    checks the rejected worksheet to see how many applications
    have been rejected and lets the user know the total.
    If there are no refected applications the user is provided
    with the option to quit or return to the main menu otherwise
    the view_rejected function is called to allow the user
    to view the applications
    """
    rejected = SHEET.worksheet('rejected').get_all_values()
    num_rejected = len(rejected)-1
    print(f'\n{num_rejected} rejected application(s)')
    if num_rejected > 0:
        print('First rejected application: \n')
        view_rejected()
    else:
        print('No rejected applications')
        next_action()


def hr_main():
    """
    processes the choice returned from show_hr_menu. 
    once the action has been completed allows the user
    to select their next action
    """
    while True:
        choice = show_hr_menu()
        if choice == '1':
            check_pending()
        elif choice == '2':
            check_approved()
        elif choice == '3':
            check_rejected()
    next_action()
