![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome BelT26,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **August 17, 2021**

## Reminders

* Your code must be placed in the `run.py` file
* Your dependencies must be placed in the `requirements.txt` file
* Do not edit any of the other files or your code may not deploy properly





# Redundancy Calculator

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
* Reverse decisions
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


## STRUCTURE
As the original file I was working on was becoming very lengthy, to improve the readability of the code I created two more files: employee.py and hr.py so that I could group the functions relevant to the access level selected.  These functions were then imported into the run.py file. 

Google sheets are used to store and manipulate data throughout the programme. I followed the Code Institute Love Sandwiches project and used the code there as a guide for how to set up my working environment and add my credentials.

I also imported the termcolor module at the start of the file to improve the appearance of the programme in the terminal and highlight important information.  The following tutorial was used as a guide ![termcolor tutorial](https://towardsdatascience.com/prettify-your-terminal-text-with-termcolor-and-pyfiglet-880de83fda6b)


## RUN.PY
This file displays a welcome message and asks the user to select an access level. If they require access to the
HR functions they must provide the correct password within 3 attempts or they will be logged out.
The main function at the base of the file then calls either the option menu imported from employee.py or hr.py


## EMPLOYEE.PY
There functions in the employee.py file serve one of 3 purposes:  To calculates the redundancy due, submit an application or to retrieve stored data about an existing application from google sheets.

### CALCULATE REDUNDANCY
No user details are requested to access the calculator.  This was deliberate as some employees expressed a wish to be able to calculate their redundancy payout without a record being kept.

Before the calculation process begins a highlighted message informs the user that they will need access to the details on their time and attendance record.  This was emphasised to prevent the user from becoming frustrated part way through the calculation when they realised that they did not have the correct data to hand.

The figures used are specific to how the company I work at is calculating redundancy in the current tax year.  To allow the programme to be more easily adapted for another company to use at some point in the future, rather than hard code the numbers for tax, holidays etc, I created easily visible global variables which are found at the top of the file.

As the functions used to retrieve information from the user in this section require a numerical input, I created an 'is_integer' function that tries to convert the user input to an integer and return it and raises a ValueError if the input is not a number.  This function is then called by all subsequent functions that ask the user to provide a number.  



## DEPLOYMENT
I set up an account with heroku.

On the heroku site I added the following two buildpacks from the _Settings_ tab
* `heroku/python`
* `heroku/nodejs`

I created a _Config Var_ called `PORT` and set it to `8000`. For my credentials I then created another _Config Var_ called `CREDS` and pasted the JSON into the value field.

The project was then deployed through my Github repository.