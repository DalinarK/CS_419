#
#             Author: Michael Marven
#       Date Created: 02/17/16
# Last Date Modified: 02/18/16
#          File Name: email_test.py
#           Overview: A script to test the appt_email module classes 
#
#                     Note: The Gmail account must have "Allow less secure apps"
#                     set to ON. Go to Gmail>Settings>Accounts and Import>
#                     Other Google Account settings>Connected apps & sites>
#                     Allow less secure apps
#
#
#

from appt_email import EmailMsg

# Declare variables
from_addr = "EMAIL ADDRESS"
to_addr = "EMAIL ADDRESS"
server = 'smtp.gmail.com'
server_port = 587
email_pwd = "EMAIL PASSWORD" # TODO: Move this to config.py module

email_subj = "Test of new Python script for sending email"
email_body = "This is a new test"

# Create EmailMsg object

test1 = EmailMsg(from_addr, to_addr, server, server_port, email_pwd)

# Send email

test1.sendEmail(email_subj, email_body)

# Print confirmation

print "Email sucesfully sent."
