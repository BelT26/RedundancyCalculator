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

# variables used in the view_pending and check_pending functions
viewed_app_ind = 1
pending = pending_sheet.get_all_values()
num_pending = len(pending)-1

# variables used to keep track of application being viewed in
# view_details function
rej_ind = 1
appr_ind = 1


def logout():
    """
    displays a message to the user that they have been logged out and
    exits the programme
    """
    print(colored('\nYou have successfully logged out.\n', 'yellow',
                  attrs=['bold']))
    exit()


def is_invalid():
    """
    Prints a statement in bold red type to inform the user that the information
    provided is not valid
    """
    print(colored('Invalid input\n', 'red', attrs=['bold']))


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
        is_invalid()


def next_action():
    """
    provides the user with the option to exit the programme or return to
    the main HR menu
    """
    while True:
        next = input('Enter Q to quit programme. M to return to main menu \n')
        if next.lower() == 'q':
            logout()
        elif next.lower() == 'm':
            break
        is_invalid()


def authorise(data, ind):
    """
    deletes an application from the applications worksheet and adds it to the
    approved worksheet
    """
    global approved
    global pending_sheet
    approved.append_row(data)
    ind += 1
    pending_sheet.delete_rows(ind)
    print(colored('\nApplication authorised.\n', 'cyan', attrs=['bold']))


def reject_appl(data, ind):
    """
    deletes an application from the applications worksheet and adds it to the
    rejected worksheet
    """
    global rejected
    global pending_sheet
    rejected.append_row(data)
    ind += 1
    pending_sheet.delete_rows(ind)
    print(colored('\nApplication rejected.\n', 'cyan', attrs=['bold']))


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
    global viewed_app_ind
    global num_pending
    headings = pending[0]
    appl_viewed = pending[viewed_app_ind]
    skipped_apps = 0
    for head, app in zip(headings, appl_viewed):
        head = head.ljust(15, ' ')
        print(f'{head} {app}')
    while True:
        print('\nDo you wish to approve or reject this application?')
        print('Please enter A to approve, R to reject, N to view next')
        approve = input('or M to return to the main menu:\n')
        if approve.lower() == 'a':
            authorise(appl_viewed, viewed_app_ind)
            pending = pending_sheet.get_all_values()
            num_pending = len(pending)-1
            break
        elif approve.lower() == 'r':
            reject_appl(appl_viewed, viewed_app_ind)
            pending = pending_sheet.get_all_values()
            num_pending = len(pending)-1
            break
        elif approve.lower() == 'm':
            show_hr_menu()
            break
        elif approve.lower() == 'n':
            print(colored('\nApplication not yet processed.\n', 'cyan',
                          attrs=['bold']))
            skipped_apps += 1
            break
        else:
            is_invalid()
    if (num_pending - skipped_apps) > 1:
        print('Next application pending approval:\n')
        view_pending()
    else:
        print('No more pending applications')
        next_action()


def view_details(status):
    """
    allows the user to view details of applications that have been rejected or
    approved. after viewing each application the user is offered the
    possibility of exiting the programme or returning to the main menu if they
    do not wish to carry on viewing the applications.
    """
    global rejected
    global approved
    global appr_ind
    global rej_ind
    rej = rejected.get_all_values()
    appr = approved.get_all_values()
    if status == 'rejected':
        headings = rej[0]
        first_appl = rej[rej_ind]
    elif status == 'approved':
        headings == appr[0]
        first_appl = appr[appr_ind]
    for head, app in zip(headings, first_appl):
        head = head.ljust(15, ' ')
        print(f'{head}:{app}')
    while True:
        view_next = input('\nPress N to view next. Q to quit. '
                          'M for main menu\n')
        if view_next.lower() == 'q':
            logout()
        elif view_next.lower() == 'n' and status == 'rejected':
            rej_ind += 1
            if rej_ind < len(rej):
                view_details('rejected')
            else:
                print('No more rejected applications to view')
                next_action()
                break
        elif view_next.lower() == 'n' and status == 'approved':
            appr_ind += 1
            if appr_ind < len(appr):
                view_details('approved')
            else:
                print('No more approved applications to view')
                next_action()
                break
        elif view_next.lower() == 'm':
            break
        else:
            is_invalid()


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
        if status == 'pending':
            view_pending()
        else:
            view_details(status)
    else:
        print(f'No {status} applications\n')
        next_action()


def hr_main():
    """
    processes the choice returned from show_hr_menu by calling the
    check_worksheet function and passing in the appropriate argument.
    once the action has been completed allows the user to select
    their next action.  Resets the index of the the application to
    be viewed to one in case it is not the first time that the user
    has selected the option
    """
    while True:
        global viewed_app_ind
        global appr_ind
        global rej_ind
        choice = show_hr_menu()
        if choice == '1':
            viewed_app_ind = 1
            check_worksheet('pending')
        elif choice == '2':
            appr_ind = 1
            check_worksheet('approved')
        elif choice == '3':
            rej_ind = 1
            check_worksheet('rejected')
    next_action()
