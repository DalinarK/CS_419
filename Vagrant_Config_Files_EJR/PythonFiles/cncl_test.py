#
#             Author: Michael Marven, Dustin Dinh, Erik Ratcliffe
#       Date Created: 03/04/16
# Last Date Modified: 03/04/16
#          File Name: cncl_test.py
#           Overview: A script to test the appt_email module CalAppt class 
#
#                     Note: The Gmail account must have "Allow less secure apps"
#                     set to ON. Go to Gmail>Settings>Accounts and Import>
#                     Other Google Account settings>Connected apps & sites>
#                     Allow less secure apps
#
#
#

from appt.appt_email import CalAppt

# Declare variables
from_addr = "EMAIL ADDRESS"
to_addr = "EMAIL ADDRESS"
server = 'smtp.gmail.com'
server_port = 587
email_pwd = "FROM EMAIL PASSWORD" # TODO: Move this to config.py module

email_subj = "Advising Signup Cancellation"
email_body = ("Advising Signup with McGrath, D Kevin CANCELLED\n"
              "Name: REDACTED\n"
              "Email: REDACTED@oregonstate.edu\n"
              "Date: Wednesday, November 21st, 2012\n"
              "Time: 1:00pm - 1:15pm\n"
             )
appointment_id = "324"
start_dtim = "20160316T153000Z"
end_dtim = "20160316T160000Z"
student_email = "marvenm@oregonstate.edu"

# Create CalAppt object

test1 = CalAppt(from_addr, to_addr, server, server_port, email_pwd)

# Send Calendar appt

test1.sendCncl(email_subj, email_body, appointment_id, start_dtim, end_dtim, student_email)

# Print confirmation

print "Email sucesfully sent."
