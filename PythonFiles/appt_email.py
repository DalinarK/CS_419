#
#             Author: Michael Marven
#       Date Created: 02/17/16
# Last Date Modified: 02/17/16
#          File Name: appt_email.py
#           Overview: A module with classes and functions to send emails and
#                     calendar appointments 
#
#                     Adapted from programming examples at these websites:
#                     http://naelshiab.com/tutorial-send-email-python/
#                     http://valermicle.blogspot.com/2009/02/i-was-searching-for-documentations-on.html
#                     http://www.baryudin.com/blog/sending-outlook-appointments-python.html
#                     https://docs.python.org/2.6/index.html
#
#
#

import smtplib
import sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

class EmailMsg(object):
    
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
    #   Method: sendEmail()
    #
    #    Entry: Strings for email subject and email body text
    #
    #     Exit: Email is sent
    #
    #  Purpose: Send an email using the parameters defined when the object 
    #           was created and the subject and body parameters of the method
    #
    #
    #   #   #   #   #   #   #   #
    def sendEmail(self, subj, body):
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
        
class CalAppt(EmailMsg):
    
    # Class constructor
    def __init__(self, fromaddr, toaddr, srvadd, port, pwd):
        EmailMsg.__init__(self, fromaddr, toaddr, srvadd, port, pwd):
        self.fromaddr = fromaddr
        self.toaddr = toaddr
        self.srvadd = srvadd
        self.port = port
        self.pwd = pwd
        
    
        
    #   #   #   #   #   #   #   #
    #
    #   Method: sendAppt()
    #
    #    Entry: Strings for email subject, email body text, and student's email;
    #           Formatted date/time for start and end date/time
    #
    #     Exit: Calendar appointment is sent
    #
    #  Purpose: Send a calendar appointment using the parameters defined when 
    #           the object was created and the subject and body parameters of 
    #           the method
    #
    #
    #   #   #   #   #   #   #   #
    def sendAppt(self, subj, body, start, end, student_email):
        # Define calendar content; iCal date format: YYYYMMDDTHHMMSSZ - T 
        # separates the date from the time and Z terminates
        # TODO: Write function to convert date/time; Dates passed to function
        # should be hard coded strings for testing
        # TODO: UID should be a unique id that is generated; Hard coded for test
        def __calContent = ("BEGIN:VCALENDAR\n"
                            "METHOD:REQUEST\n"
                            "PRODID: BCP - Meeting\n"
                            "VERSION:2.0\n"
                            "BEGIN:VEVENT\n"
                            "DTSTAMP:" + start + "\n"
                            "DTSTART:" + start + "\n"
                            "DTEND:" + end + "\n"
                            "SUMMARY:" + self.subj + "\n"
                            "UID:324\n"
                            "ATTENDEE;"
                            "ROLE=REQ-PARTICIPANT;"
                            "PARTSTAT=NEEDS-ACTION;"
                            "RSVP=TRUE:MAILTO:" + student_email + "\n"
                            "ORGANIZER:MAILTO:" + student_email + "\n"
                            "LOCATION:OSU Office\n" +
                            "DESCRIPTION:" + self.body + "\n"
                            "SEQUENCE:0\n"
                            "PRIORITY:5\n"
                            "CLASS:PUBLIC\n"
                            "STATUS:CONFIRMED\n"
                            "TRANSP:OPAQUE\n"
                            "BEGIN:VALARM\n"
                            "ACTION:DISPLAY\n"
                            "DESCRIPTION:REMINDER\n"
                            "TRIGGER;RELATED=START:-PT00H15M00S\n"
                            "END:VALARM\n"
                            "END:VEVENT\n"
                            "END:VCALENDAR"
                           )
                           
        # Build email
        msg = MIMEMultipart("alternative")
        msg['From'] = self.fromaddr
        msg['To'] = self.toaddr
        msg['Subject'] = subj
        msg["Content-class"] = "urn:content-classes:calendarmessage"
        
        # Build first MIME body part with simple text description of appt
        msg.attach(MIMEText(self.body))
        
        # Build second MIME body part with iCal information
        part = MIMEBase('text', "calendar", method="REQUEST")
        part.set_payload(__calContent)
        encoders.encode_base64(part)
        part.add_header("Content-class", "urn:content-classes:calendarmessage")
        msg.attach(part)
        
        
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
        
        
    