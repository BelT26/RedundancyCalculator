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

# variable used in the view_pending and check_pending functions
pending = pending_sheet.get_all_values()


# variables used to keep track of application being viewed in
# view_rejected, view_approved functions.
# values are reset in hr_main
rej_ind = 1
appr_ind = 1
pend_app_ind = 1
skipped_apps = 0
num_pending = len(pending)-1


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
    no_input = True
    while no_input:
        print('\nPlease select from the following options:\n')
        print('1. View / authorise pending applications')
        print('2. View authorised applications')
        print('3. View rejected applications\n')
        choice = input('Please enter 1, 2 or 3 or Q to quit \n')
        if choice in ('1', '2', '3'):
            no_input = False
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
    global pend_app_ind
    global num_pending
    global skipped_apps
    headings = pending[0]
    appl_viewed = pending[pend_app_ind]
    for head, app in zip(headings, appl_viewed):
        head = head.ljust(15, ' ')
        print(f'{head} {app}')
    while True:
        print('\nDo you wish to approve or reject this application?')
        print('Please enter A to approve, R to reject, V to view next')
        approve = input('or M to return to the main menu:\n')
        if approve.lower() == 'a':
            authorise(appl_viewed, pend_app_ind)
            pending = pending_sheet.get_all_values()
            num_pending = len(pending)-1
            break
        elif approve.lower() == 'r':
            reject_appl(appl_viewed, pend_app_ind)
            pending = pending_sheet.get_all_values()
            num_pending = len(pending)-1
            break
        elif approve.lower() == 'm':
            hr_main()
            return
        elif approve.lower() == 'v':
            print(colored('\nApplication not yet processed.\n', 'cyan',
                          attrs=['bold']))
            skipped_apps += 1
            pend_app_ind += 1
            break
        else:
            is_invalid()
    if (num_pending - skipped_apps) > 0:
        print('Next application pending approval:\n')
        view_pending()
    else:
        print('No more pending applications')
        next_action()


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
    keep_viewing = True
    while keep_viewing:
        view_next = input('\nPress N to view next, Q to quit, '
                          'M for main menu.\n')
        if view_next.lower() == 'q':
            print(colored('\nYou have successfully logged out.\n', 'yellow'))
            exit()
        elif view_next.lower() == 'n':
            rej_ind += 1
            if rej_ind < len(rej):
                view_rejected()
            else:
                print('\nNo more rejected applications to view')
                keep_viewing = False
                next_action()
        elif view_next.lower() == 'm':
            keep_viewing = False
            hr_main()
            break
        else:
            print(colored('Invalid input', 'red\n'))


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
    keep_viewing = True
    while keep_viewing:
        view_next = input('\nPress V to view next, Q to quit, M for main '
                          'menu.\n')
        if view_next.lower() == 'q':
            print(colored('\nYou have successfully logged out.\n', 'yellow'))
            exit()
        elif view_next.lower() == 'v':
            appr_ind += 1
            if appr_ind < len(appr):
                print('Next approved application: \n')
                view_approved()
            else:
                print('\nNo more approved applications to view \n')
                keep_viewing = False
                next_action()
                break
        elif view_next.lower() == 'm':
            keep_viewing = False
            hr_main()
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
        elif status == 'approved':
            view_approved()
        else:
            view_rejected()
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
        global pend_app_ind
        global appr_ind
        global rej_ind
        global skipped_apps
        global num_pending
        user_choice = show_hr_menu()
        if user_choice == '1':
            skipped_apps = 0
            pend_app_ind = 1
            num_pending = len(pending)-1
            check_worksheet('pending')
        elif user_choice == '2':
            appr_ind = 1
            check_worksheet('approved')
        elif user_choice == '3':
            rej_ind = 1
            check_worksheet('rejected')
    next_action()
