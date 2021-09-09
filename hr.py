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


def show_hr_menu():
    while True:
        print('Please select from the following options:')
        print('1. View / authorise pending applications')
        print('2. View authorised applications')
        print('3. View rejected applications')
        choice = input('Please enter 1, 2 or 3 or Q to quit \n')
        if choice in ('1', '2', '3'):
            return choice
        elif choice.lower() == 'q':
            exit()
        print(colored('invalid option\n', 'red'))


pending_sheet = SHEET.worksheet('applications')
approved = SHEET.worksheet('approved')
rejected = SHEET.worksheet('rejected')


def next_action():
    while True:
        next = input('Enter Q to quit. M to return to main menu \n')
        if next.lower() == 'q':
            print('You have been successfully logged out \n')
            exit()
        elif next.lower() == 'm':
            show_hr_menu()
            break
        print(colored('Invalid input', 'red\n'))


def authorise(data):
    global approved
    global pending_sheet
    print('Authorising application.')
    approved.append_row(data)
    pending_sheet.delete_rows(2)


def reject_appl(data):
    print('Rejecting application.')
    global rejected
    global pending_sheet
    rejected.append_row(data)
    pending_sheet.delete_rows(2)


def view_pending():
    global pending_sheet
    pending = pending_sheet.get_all_values()
    headings = pending[0]
    first_appl = pending[1]
    for head, app in zip(headings, first_appl):
        print(f'{head}:{app}')
    print('Do you wish to approve this application?')
    approve = input('Please enter Y or N. Enter Q to quit:\n')
    if approve.lower() == 'y':
        authorise(first_appl)
    elif approve.lower() == 'q':
        exit()
    else:
        print('Do you wish to reject this application?')
        reject = input('Please enter Y or N:\n')
        if reject.lower() == 'y':
            reject_appl(first_appl)
    num_pending = len(pending)-2
    print(f'{num_pending} application(s) pending approval')
    if num_pending > 0:
        view_pending()
    else:
        print('No more pending applications')
        next_action()


def check_pending():
    pending = SHEET.worksheet('applications').get_all_values()
    num_pending = len(pending)-1
    print(f'\n{num_pending} application(s) pending approval')
    if num_pending > 0:
        print('Retrieving details of first pending application... \n')
        view_pending()
    else:
        print('No pending applications')
        next_action()


appr_ind = 1


def view_approved():
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
            exit()
        elif view_next.lower() == 'n':
            appr_ind += 1
            if appr_ind < len(appr):
                print('Next approved application: \n')
                view_approved()
            else:
                sprint('No more approved applications to view')


def check_approved():
    approved = SHEET.worksheet('approved').get_all_values()
    num_approved = len(approved)-1
    print(f'\n{num_approved} approved application(s)')
    if num_approved > 0:
        print('First application: \n')
        view_approved()
    else:
        print('No approved applications')


ind = 1


def view_rejected():
    global rejected
    global ind
    rej = rejected.get_all_values()
    headings = rej[0]
    first_appl = rej[ind]
    for head, app in zip(headings, first_appl):
        print(f'{head}:{app}')
    view_next = input('\nPress N to view next. Q to quit\n')
    if view_next.lower() == 'q':
        exit()
    elif view_next.lower() == 'n':
        ind += 1
        if ind < len(rej):
            view_rejected()
        else:
            print('No more rejected applications to view')


def check_rejected():
    rejected = SHEET.worksheet('rejected').get_all_values()
    num_rejected = len(rejected)-1
    print(f'\n{num_rejected} rejected application(s)')
    if num_rejected > 0:
        print('First application: \n')
        view_rejected()
    else:
        print('No rejected applications')


def hr_main():
    choice = show_hr_menu()
    if choice == '1':
        check_pending()
    elif choice == '2':
        check_approved()
    elif choice == '3':
        check_rejected()
    

hr_main()

    

        