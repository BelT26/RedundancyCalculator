# Redundancy Calculator

https://mtl-redundancy-calculator.herokuapp.com/

## Table of Contents
* Motivation
* Access levels
* Staff access features 
* Caluclate Redundancy
* Check status
* HR access features
* View applications
* Approve applications
* Reject applications
* Bugs and challenges
* Deployment
* Credits
* Future development possibilities


## Motivation
I work for a travel company that is currently undergoing their third round of redundancies due to the pandemic.
The possibility of voluntary redundancy will be offered to staff.
During the previous redundancy waves staff reported the following concerns about making an enquiry to HR to find out how much voluntary redundancy they would be entitled to:
* The information sent out was not detailed enough and tax was not deducted so it was unclear how much money they would receive.
* There were delays of several days before they received the information
* They would have preferred to obtain this information anonymously as they were concerned it could affect the reduncancy selection process if it were recorded that they had enquired about a voluntary payout. 

To combat these issues I created a redundancy calculator that would allow staff to immediately access their potential voluntary redundancy payout in an anonymous way.

## Planning
My first step was to set up the functions to calculate the individual elements that made up the redundancy payment
The information taken to calculate the statutory entitlement was taken from the UK government website ![statutory redundancy entitlement]https://www.gov.uk/redundancy-your-rights/redundancy-pay.
The income tax and national insurance contributions were also calculated based on the figures on the government website ![tax](https://www.gov.uk/income-tax-rates)  ![NI Contributions](https://www.gov.uk/government/publications/rates-and-allowances-national-insurance-contributions/rates-and-allowances-national-insurance-contributions)
A breakdown of how I approached the redundancy calculation can be found on the attached Excel spreadsheet ![Redundancy spreadsheet]().
I then created a function to offer the user to submit an application by saving their details to a google sheets API.
The HR functions were then put in place so that a member of HR could view, authorise or reject applications.
The final step was to allow the user the possibility to view the status of their application by creating functions that access the information stored on the google worksheets.


## Structure
As the original file I was working on was becoming very lengthy, to improve the readability of the code I created two more files: employee.py and hr.py so that I could group the functions relevant to the access level selected.  These functions were then imported into the run.py file. 

Google sheets are used to store and manipulate data throughout the programme. I followed the Code Institute Love Sandwiches project and used the code there as a guide for how to set up my working environment and add my credentials.

I also imported the termcolor module at the start of the file to improve the appearance of the programme in the terminal and highlight important information.  The following tutorial was used as a guide ![termcolor tutorial](https://towardsdatascience.com/prettify-your-terminal-text-with-termcolor-and-pyfiglet-880de83fda6b)

Flowcharts that show the logic of the programme files are provided under the individual sections.


## Run.py
This file displays a welcome message and asks the user to select an access level. If they require access to the
HR functions they must provide the correct password within 3 attempts or they will be logged out.
The main function at the base of the file then calls either the option menu imported from employee.py or hr.py


## Employee.py
There functions in the employee.py file serve one of 3 purposes:  To calculates the redundancy due, submit an application or to retrieve stored data about an existing application from google sheets.

### Reduncancy calculation
No user details are requested to access the calculator.  This was deliberate as some employees expressed a wish to be able to calculate their redundancy payout without a record being kept.

Before the calculation process begins a highlighted message informs the user that they will need access to the details on their time and attendance record.  This was emphasised to prevent the user from becoming frustrated part way through the calculation when they realised that they did not have the correct data to hand.

The figures used are specific to how the company I work at is calculating redundancy in the current tax year.  To allow the programme to be more easily adapted for another company to use at some point in the future, rather than hard code the numbers for tax, holidays etc, I created easily visible global variables which are found at the top of the file.

As the functions used to retrieve information from the user in this section require a numerical input, I created an 'is_integer' function that tries to convert the user input to an integer and return it and raises a ValueError if the input is not a number.  This function is then called by all subsequent functions that ask the user to provide a number.  

The initial output to the terminal was not particularly readable.  For a better visual experience for the user I aligned the figures using the ljust() method.  I found that this tutorial was very helpful ![W3 Schools ljust() tutorial](https://www.w3schools.com/python/ref_string_ljust.asp)

After the calculation is displayed the user is then offered the option of submitting an application. If they decide not to proceed no data is stored and they exit the programme.

### Application Submission
It is only possible to submit an application directly after receiving a calculation.  This is deliberate to prevent the user from entering inaccurate calculations.

If the user decides to proceed with their application they are asked to enter their name and their payroll number. These are then checked against the staff details on the staff worksheet of the Google API. If correct details are provided a check is then carried out to see if an application has already been submitted. If it has the user, is advised that an application has been made and informed of the status otherwise the user's details are submitted to the pending sheet of the API.

### View status
This feature offers the employee the possibility of viewing whether their application is approved, rejected or still pending. To access this feature the employee needs to provide their name and payroll number.  If the correct information is not provided within 3 attempts the programme is closed otherwise the status is retrieved by checking the details provided against the data stored on the Google worksheets.  If no matching data is found the user is informed that no application has been submitted and is given the opportunity to calculate their redundancy and submit an application.


## HR.py
Through the HR menu, authorised users are able to view, authorise and reject applications


## Bugs
The majority of problems I encountered where with the view_pending function within hr.py Although the google sheets API was updating correctly and moving the application from the pending worksheet to the rejected or approved worksheet the terminal kept redisplaying the same application.  I eventually worked out that I needed to reset the pending and num_pending variables immediately after calling the authorise or reject_appl functions


## Deployment
I set up an account with heroku.

On the heroku site I added the following two buildpacks from the _Settings_ tab
* `heroku/python`
* `heroku/nodejs`

I created a _Config Var_ called `PORT` and set it to `8000`. For my credentials I then created another _Config Var_ called `CREDS` and pasted the JSON into the value field.

The project was then deployed through my Github repository.


## Future Development Possibilities
With more time I would explore the option of adding the following features
* Add the possibility for HR to reverse decisions made when approving or rejecting applications
* Rather than display each application in chronological order when HR view them, for larger companies a list of the applications on the selected sheet and they could choose which one to view.
* At the company I work for there is currently only one person in the HR team.  For larger companies rather than just request a password for HR access I would implement a name and payroll check for the HR member as I did for the employee.  This information would be recorded before the user can access the main HR menu and would be stored and pushed to the API so that it is possible to see who has refused and authorised applications.
* In a real world scenario the information the user enters for their salary / holidays etc could be automatically validated against an employee database holding these details if they decided to submit an application
