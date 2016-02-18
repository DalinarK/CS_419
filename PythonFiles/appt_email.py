#
#             Author: Michael Marven
#       Date Created: 02/17/16
# Last Date Modified: 02/17/16
#          File Name: appt_email.py
#           Overview: A module with classes to send test emails and calendar
#                     appointments 
#
#
#

import smtplib
import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class TestEmail(object):
    
    # Class constructor
    
    def __init__(self, fromaddr, toaddr, srvadd, port, pwd): 
        self.fromaddr = fromaddr
        self.toaddr = toaddr
        self.srvadd = srvadd
        self.port = port
        self.pwd = pwd
    
    # Get methods
    def getFromAdd(self): 
        return self.fromaddr
    
    def getToAdd(self):
        return self.toaddr
        
    def getSrvAdd(self):
        return self.srvadd
        
    def getPort(self):
        return self.port
        
    def getPwd(self):
        return self.pwd
        
    #   #   #   #   #   #   #   #
    #
    #   Method: sendTestEmail()
    #
    #    Entry: Email subject and email body text
    #
    #     Exit: Email is sent
    #
    #  Purpose: Send a test email using the parameters defined when the object 
    #           was created and the subject and body parameters of the method
    #
    #
    #   #   #   #   #   #   #   #
    def sendTestEmail(self, subj, body):
        # Build email
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = self.toaddr
        msg['Subject'] = subj
         
        msg.attach(MIMEText(body, 'plain'))
        
        # Try connecting to server
        try:
            server = smtplib.SMTP(self.srvadd, self.port)
            server.starttls()
            server.login(self.fromaddr, self.pwd)
        except: 
            print "Error connecting to server:", sys.exc_info()[0]
        
        # Send email
        text = msg.as_string()
        server.sendmail(self.fromaddr, self.toaddr, text)
        server.quit()
        
        
    