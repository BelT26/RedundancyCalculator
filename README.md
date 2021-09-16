# Redundancy Calculator

https://mtl-redundancy-calculator.herokuapp.com/

## Author: Helen Taylor  
## Version 1.0.0

![site preview](https://github.com/BelT26/RedundancyCalculator/blob/main/assets/employee_menu.PNG)

## Table of Contents
* [Motivation](#motivation)
* [Planning](#planning)
* [Structure](#structure)
* [Data Model](#data-model)
* [Run.py](#run-file)
* [Employee.py](#employee-file)
    * [Redundancy calculation](#redundancy-calculation) 
    * [Application submission](#application-submission)
    * [View Status](#view-status)
* [HR.py](#hr-file)
    * [Pending applications](#pending-applications)
    * [View approved and rejected applications](#view-approved-and-rejected-applications)
* [Bugs](#bugs)
* [Testing](#testing)
* [Deployment](#deployment)
* [Credits](#credits)
* [Future development possibilities](#future-development-possibilities)


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
A breakdown of how I approached the redundancy calculation can be found on the attached Excel spreadsheet [Redundancy spreadsheet](https://github.com/BelT26/RedundancyCalculator/blob/main/assets/Redundancy%20spreadsheet.xlsx).
I then created a function to offer the user to submit an application by saving their details to a google sheets API.
The HR functions were then put in place so that a member of HR could view, authorise or reject applications.
The final step was to allow the user the possibility to view the status of their application by creating functions that access the information stored on the google worksheets.


## Structure
As the original file I was working on was becoming very lengthy, to improve the readability of the code I created two more files: employee.py and hr.py so that I could group the functions relevant to the access level selected.  These functions were then imported into the run.py file. 

Google sheets are used to store and manipulate data throughout the programme. I followed the Code Institute Love Sandwiches project and used the code there as a guide for how to set up my working environment and add my credentials.

I also imported the termcolor module at the start of the file to improve the appearance of the programme in the terminal and highlight important information.  The following tutorial was used as a guide ![termcolor tutorial](https://towardsdatascience.com/prettify-your-terminal-text-with-termcolor-and-pyfiglet-880de83fda6b)

Flowcharts that show the logic of the programme files are provided under the individual sections.


## Data Model
I chose to use a Google sheets API as the data model for my project.
The API is composed of 4 worksheets.
The 'staff' worksheet is used to store the names and payroll numbers of company employess and is used to validate details provided by users when they select to proceed with a redundancy application or view their application status. 
![staff worksheet](https://github.com/BelT26/RedundancyCalculator/blob/main/assets/api_staff_list.PNG)
The other 3 worksheets are used to store the details of the applications submitted. They are named 'pending', 'approved' and 'rejected'. They all have the same format. HR members can manipulate the data to move an application from the 'pending' sheet to either the 'approved' or 'rejected' sheet.
![approved worksheet](https://github.com/BelT26/RedundancyCalculator/blob/main/assets/application_details.PNG)


## Run file
This file displays a welcome message and asks the user to select an access level. If they require access to the
HR functions they must provide the correct password within 3 attempts or they will be logged out.
The main function at the base of the file then calls either the option menu imported from employee.py or hr.py


## Employee file
There functions in the employee.py file serve one of 3 purposes:  To calculates the redundancy due, submit an application or to retrieve stored data about an existing application from google sheets.

To submit an application or view it's status please use the name REBECCA LANE and the payroll number 2783.
Alternative logins can be found on the Google staff worksheet although some have already submitted applications!


### Reduncancy calculation
No user details are requested to access the calculator.  This was deliberate as some employees expressed a wish to be able to calculate their redundancy payout without a record being kept.

Before the calculation process begins a highlighted message informs the user that they will need access to the details on their time and attendance record.  This was emphasised to prevent the user from becoming frustrated part way through the calculation when they realised that they did not have the correct data to hand. ![employee time and attendance dashboard example (colors are not significant)](https://github.com/BelT26/RedundancyCalculator/blob/main/assets/holiday_dashboard.png)

The figures used are specific to how the company I work at is calculating redundancy in the current tax year.  To allow the programme to be more easily adapted for another company to use at some point in the future, rather than hard code the numbers for tax, holidays etc, I created easily visible global variables which are found at the top of the file.

As the functions used to retrieve information from the user in this section require a numerical input, I created an 'is_integer' function that tries to convert the user input to an integer and return it and raises a ValueError if the input is not a number.  This function is then called by all subsequent functions that ask the user to provide a number.  

The company I work for has slightly unusual procedure for holidays brought forward from the previous holiday year. 'Bought' holidays are those that were awarded in the past for working extra days, these holidays must be used before the end of the consultation period or they will be lost.  Normal holidays that were not used in the previous holiday year and were carried over will be paid if the employee does not take them before the end of the consultation.  Because of these complexities I added a calculation of the holidays owed once the holiday information had been provided. ![holidays owed](https://github.com/BelT26/RedundancyCalculator/blob/main/assets/holidays.PNG)

The initial output to the terminal was not particularly readable.  For a better visual experience for the user I aligned the figures using the ljust() method.  ![calculation example](https://github.com/BelT26/RedundancyCalculator/blob/main/assets/calculation.PNG)
I found that this tutorial was very helpful in implementing the ljust method: ![W3 Schools ljust() tutorial](https://www.w3schools.com/python/ref_string_ljust.asp)

After the calculation is displayed the user is then offered the option of submitting an application. If they decide not to proceed no data is stored and they exit the programme.


### Application Submission
It is only possible to submit an application directly after receiving a calculation.  This is deliberate to prevent the user from entering inaccurate calculations.

If the user decides to proceed with their application they are asked to enter their name and their payroll number. These are then checked against the staff details on the staff worksheet of the Google API. If correct details are provided, a check is then carried out to see if an application has already been submitted. If it has the user, is advised that an application has been made and informed of the status otherwise the user's details are submitted to the pending sheet of the API.


### View status
This feature offers the employee the possibility of viewing whether their application is approved, rejected or still pending. To access this feature the employee needs to provide their name and payroll number.  If the correct information is not provided within 3 attempts the programme is closed otherwise the status is retrieved by checking the details provided against the data stored on the Google worksheets.  If no matching data is found the user is informed that no application has been submitted and is given the opportunity to calculate their redundancy and submit an application.


## HR file
The password to access the HR menu is #MTL
Through the HR menu, authorised users are able to view, approve and reject applications.
![HR Menu](https://github.com/BelT26/RedundancyCalculator/blob/main/assets/hr_menu.PNG)


### Pending Applications
If the user selects this option they are shown each of the pending applications in turn. After each application is displayed the user has the options of approving or rejecting it, moving on to view the next application or returning to the main menu.

If they choose to approve or reject the application the details are removed from the 'pending' worksheet and stored instead in either the 'approved' or 'rejected' worksheet. 
[Pending application](https://github.com/BelT26/RedundancyCalculator/blob/main/assets/pending.PNG)


### View Approved and Rejected Applications
The user is shown the details of each of the approved or rejected applications in turn. After each application they are offered the choice of viewing the next application, quitting the programme or returning to the main HR menu. Once all applications have been viewed they can either quit or access the main HR menu.


## Bugs
The majority of problems I encountered where with the view_pending function within hr.py Although the google sheets API was updating correctly and moving the application from the pending worksheet to the rejected or approved worksheet the terminal kept redisplaying the same application.  I eventually worked out that I needed to reset the pending and num_pending variables immediately after calling the authorise or reject_appl functions

The use of nested while loops caused me some issues in the view approved and view rejected functions in hr.py. Although the if and elif conditions were breaking out of the inner loop the outer loop kept running.  To rectify this I created a variable called 'keep_viewing' and modified its value from True to false the user input provided meant that it was necessary to breakout of the outer loop.


## Testing

No issues were present when the code was passed through the PEP8 validator.

I carried out multiple manual checks to validate numerous possible combinations of user input.

My colleagues who were considering applying for voluntary redundancy checked the figures of my calculator against those provided by HR and confirmed that they matched.


## Deployment
This project was deployed using the Code Institute's mock terminal for Heroku.
I created a _Config Var_ called `PORT` and set it to `8000`. For my credentials I then created another _Config Var_ called `CREDS` and pasted the JSON into the value field.

Steps for deployment:
* Fork or clone this repository
* Create a new Heroku App
* Add the following two buildpacks from the _Settings_ tab
    * `heroku/python`
    * `heroku/nodejs`
* Link the Heroku App to the repository
* Click on deploy


## Credits
* The process used to set up my development environment and the code used to link my project to the API were taken from the Code Institute Love Sandwiches walkthrough project.
* The information taken to calculate the statutory entitlement was taken from the UK government website [statutory redundancy entitlement](https://www.gov.uk/redundancy-your-rights/redundancy-pay).
* The income tax and national insurance contributions were also calculated based on the figures on the UK government website [tax](https://www.gov.uk/income-tax-rates)  [NI Contributions](https://www.gov.uk/government/publications/rates-and-allowances-national-insurance-contributions/rates-and-allowances-national-insurance-contributions)


## Future Development Possibilities
With more time I would explore the option of adding the following features
* Add the possibility for HR to reverse decisions made when approving or rejecting applications
* Rather than display each application in chronological order when HR view them, for larger companies a list of the applications on the selected sheet and they could choose which one to view.
* At the company I work for there is currently only one person in the HR team.  For larger companies rather than just request a password for HR access I would implement a name and payroll check for the HR member as I did for the employee.  This information would be recorded before the user can access the main HR menu and would be stored and pushed to the API so that it is possible to see who has refused and authorised applications.
* In a real world scenario the information the user enters for their salary / holidays etc could be automatically validated against an employee database holding these details if they decided to submit an application
