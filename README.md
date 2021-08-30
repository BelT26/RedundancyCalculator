![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome BelT26,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **August 17, 2021**

## Reminders

* Your code must be placed in the `run.py` file
* Your dependencies must be placed in the `requirements.txt` file
* Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

-----
Happy coding!


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
* Future deployment possibilities


## Motivation
I work for a travel company that is currently undergoing their third round of redundancies due to the pandemic.
The possibility of voluntary redundancy will be offered to staff.
During the previous redundancy waves staff reported the following concerns about making an enquiry to HR to find out how much voluntary redundancy they would be entitled to:
* The information sent out was not detailed enough and tax was not deducted so it was unclear how much money they would receive.
* There were delays of several days before they received the information
* They would have preferred to obtain this information anonymously as they were concerned it could affect the reduncancy selection process if it were recorded that they had enquired about a voluntary payout. 

To combat these issues I created a redundancy calculator that would allow staff to immediately access their potential voluntary redundancy payout in an anonymous way.

## Access levels