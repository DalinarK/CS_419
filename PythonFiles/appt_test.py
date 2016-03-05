#
#             Author: Michael Marven
#       Date Created: 02/18/16
# Last Date Modified: 02/18/16
#          File Name: appt_test.py
#           Overview: A script to test the appt_email module CalAppt class 
#
#                     Note: The Gmail account must have "Allow less secure apps"
#                     set to ON. Go to Gmail>Settings>Accounts and Import>
#                     Other Google Account settings>Connected apps & sites>
#                     Allow less secure apps
#
#
#

from appt_email import CalAppt

# Declare variables
from_addr = "weaselmuncher@gmail.com"
to_addr = "gophermuncher@gmail.com"
server = 'smtp.gmail.com'
server_port = 587
email_pwd = "419FinalProject" # TODO: Move this to config.py module

email_subj = "Advising Signup with McGrath, D Kevin confirmed for REDACTED"
email_body = ("Advising Signup with McGrath, D Kevin confirmed\n"
              "Name: REDACTED\n"
              "Email: REDACTED@oregonstate.edu\n"
              "Date: Wednesday, November 21st, 2012\n"
              "Time: 1:00pm - 1:15pm\n"
             )
start_dtim = "20160315T223000Z"
end_dtim = "20160315T230000Z"
# start_dtim = "20160315T153000"
# end_dtim = "20160315T160000"
student_email = "marvenm@oregonstate.edu"

# Create CalAppt object

test1 = CalAppt(from_addr, to_addr, server, server_port, email_pwd)

# Send Calendar appt

test1.sendAppt(email_subj, email_body, start_dtim, end_dtim, student_email)

# Print confirmation

print "Email sucesfully sent."
