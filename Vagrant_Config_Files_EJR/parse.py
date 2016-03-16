import os.path
import sys
#sys.path.insert(0, '../../../vagrant/PythonFiles/')
sys.path.append(os.path.expanduser('~') + '/.appt') # for ~/.appt/credentials.py
from credentials import *
import re
import datetime
import sqlite3 as lite
from appt.appt_email import CalAppt

UTCconversiontime = 7

print("Starting python script")

# fileStream = open("pythoncreatedfile", 'w')

# fileStream.write('swag \n')
# for line in sys.stdin:
# 	fileStream.write (line),

# Stores input into a variable
inputVar = sys.stdin.read()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: Find advisor first name and last and store it in variables
# If there is a middle name it will also get parsed out. If the number of names
# is greater than 3 or less than 2 then the first and last name will be the first and last elements
# in the parsed name list.
# Variables created: 	
# 	advisorFirstName
# 	advisorLastName
# 	[advisorMiddleName]
# 	advisorEmail
# Notes: When performing any operation, make sure that advisorMiddleName actually exists
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Creates the filter
expressionObject = re.compile('Advising Signup with (.*)\s(confirmed|CANCELLED)')
# Executes the filter on inputVar and stores it in object matchObject then stores the result into 
# nameLine variable
matchObject = expressionObject.search(inputVar)
nameLine = matchObject.group(1)
print "filter pulled: " + nameLine
emailType = matchObject.group(2)
print "email type: " + emailType
# Creates second filter used to split up the names and executes split()
expressionObject = re.compile('\W+')
nameList = expressionObject.split(nameLine)

print "length of nameList: " + str(len(nameList))

if len(nameList) == 2:
	# print "found two names"
	advisorFirstName = nameList[1]
	advisorLastName = nameList[0]
	advisorMiddleName = ""
elif len(nameList) == 3:
	# print "found three names"
	advisorFirstName = nameList[2]
	advisorLastName = nameList[0]
	advisorMiddleName = nameList[1]
# If there are multiple names, only save the last name of the set
else:
	# print "found less than or more than one name"
	advisorFirstName = nameList[-1]
	advisorLastName = nameList[0]

print "first name: " + advisorFirstName
print "last name: " + advisorLastName
if len(nameList) == 3:
	print "middle name: " + advisorMiddleName

# finds the advisor's email
expressionObject = re.compile('To: (.*)')
matchObject = expressionObject.search(inputVar)
nameLine = matchObject.group(1)
print "advisor email: " + nameLine
advisorEmail = nameLine

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#Purpose: Find name of appointment maker
#Parses out the first and last name
# If there is a middle name it will also get parsed out. If the number of names
# is greater than 3 or less than 2 then the first and last name will be the first and last elements
# in the parsed name list.
# Variables created: 	
# 	appointeeFirstName
# 	appointeeLastName
# 	[appointeeMiddleName]
# Notes: When performing any operations on appointeeMiddleName make sure it actually exists
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

expressionObject = re.compile('Name: (.*)')
matchObject = expressionObject.search(inputVar)
nameLine = matchObject.group(1)
print "filter pulled: " + nameLine	
expressionObject = re.compile('\W+')
nameList = expressionObject.split(nameLine)
print "name length is " + str(len(nameList))

if len(nameList) == 3:
	appointeeFirstName = nameList[1]
	appointeeLastName = nameList[0]
	appointeeMiddleName = ""
elif len(nameList) == 4:
	appointeeFirstName = nameList[1]
	appointeeLastName = nameList[0]
	appointeeMiddleName = nameList[2]
# If there are multiple names, only save the last name of the set
else:
	print "name length not 3 or 2"
	appointeeFirstName = nameList[0]
	appointeeLastName = nameList[-1]

print "Student first name: " + appointeeFirstName
print "Student last name: " + appointeeLastName
if len(nameList) == 4:
	print "middle name: " + appointeeMiddleName

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: parse out the user's email
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
expressionObject = re.compile('Email:\s*(.*)\s*')
matchObject = expressionObject.search(inputVar)	
appointeeEmail = matchObject.group(1)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: parse out the date and store it in the date variable
# Variables created: month (int), day (int), year(int)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

expressionObject = re.compile('Date: (.*,.*,.*)')
matchObject = expressionObject.search(inputVar)	
expressionObject = re.compile('\W+')
nameLine = matchObject.group(1)
dateList = expressionObject.split(nameLine)

dateString = nameLine
# print dateList
month = dateList[1]
year = dateList[3]
day = dateList[2]
# only keep the numbers and remove the suffixes like 'st' 'nd' etc
expressionObject = re.compile('\d*')
matchObject = expressionObject.search(day)	
day = matchObject.group()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: parse out the start and end hours
# Variables created: startHour (int) startMinute endHour (int) endMinute
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

expressionObject = re.compile('Time:\s+(\d*:\d*[p|m|a]+)\s+-\s+(\d*:\d*[p|m|a]+)')
matchObject = expressionObject.search(inputVar)	
startTime = matchObject.group(1)
endTime = matchObject.group(2)

print "startTime" + startTime
print "endTime" + endTime

# Get the hours for startTime
# Check to see if the time is in PM and remove it + add 12 hours
expressionObject = re.compile('pm')
result = expressionObject.search(startTime)

if result is not None: 
	if result.group() == 'pm':
		# remove the pm from startTime
		print "found pm replacing"
		startTime = expressionObject.sub("", startTime) 
		# add 12 hours
		expressionObject = re.compile('\d*')
		matchObject =expressionObject.search(startTime)
		startHour = matchObject.group()
		startHour = (int(startHour) + 12)%24
		startHour = str(startHour)

# Check to see if the time is in AM and remove it
expressionObject = re.compile('am')
result = expressionObject.search(startTime)
if result is not None:
	if result.group() == 'am':
		# remove the pm from startTime
		print "found am replacing"
		startTime = expressionObject.sub("", startTime)
		expressionObject = re.compile('\d*')
		matchObject =expressionObject.search(startTime)
		startHour = matchObject.group()

# Get the minutes startTime
expressionObject = re.compile(':(\d\d)')
print startTime
matchObject = expressionObject.search(startTime)
startMinute = matchObject.group(1)

# print "Start Hour is " + startHour + " Start Minutes is " + startMinute

# Get the hours for endTime
# Check to see if the time is in PM and remove it + add 12 hours
expressionObject = re.compile('pm')
result = expressionObject.search(endTime)

if result is not None:
	if result.group() == 'pm':
		# remove the pm from endTime
		print "found pm replacing"
		endTime = expressionObject.sub("", endTime) 
		# add 12 hours
		expressionObject = re.compile('\d*')
		matchObject =expressionObject.search(endTime)
		endHour = matchObject.group()
		endHour = (int(endHour) + 12)%24
		endHour = str(endHour)
# Check to see if the time is in AM and remove it
expressionObject = re.compile('am')
result = expressionObject.search(endTime)
if result is not None: 
	if result.group() == 'am':
		# remove the pm from endTime
		print "found am replacing"
		endTime = expressionObject.sub("", endTime)
		expressionObject = re.compile('\d*')
		matchObject =expressionObject.search(startTime)
		endHour = matchObject.group()

# Get the minutes endTime
expressionObject = re.compile(':(\d\d)')
matchObject = expressionObject.search(endTime)
endMinute = matchObject.group(1)

print "start Hour: " + startHour + " start Minute: " + startMinute
print "end Hour: " + endHour + " end Minute: " + endMinute

# construct start date
startDateString = startHour  + " " + startMinute + " " + day + " " + month + " " + year
startDate = datetime.datetime.strptime(startDateString, "%H %M %d %B %Y")

endDateString = endHour + " " + endMinute + " " + day + " " + month + " " + year
endDate = datetime.datetime.strptime(endDateString, "%H %M %d %B %Y")

startDateString = startDate.strftime('%H %M %d %B %Y')
endDateString = endDate.strftime('%H %M %d %B %Y')
# print startDate.strftime('%H %M %d %B %Y')

# Convert time into iCal format for start time
startHour = startDate.strftime('%H')
print "start hour is " + startHour
# convert to UTC by adding 8
# startHour = str((UTCconversiontime + int(startHour))%24)
# turn a single hour digit into a double digit time
if len(startHour) == 1:
	startHour = "0" + startHour
print "converted start hour is " + startHour
# get minutes
startMinuteString = startDate.strftime ('%M')
print "Start Minute " + startMinuteString
# Get year/month/day
#startYMD = startDate.strftime('%Y%m%d')
isoStartYMD = startDate.strftime('%Y%m%d')
startYMD = startDate.strftime('%Y-%m-%d')
print "start Date" + startDateString


# Convert time into ical format for end time
if len(endHour) == 1:
	endHour = "0" + endHour
print "converted end hour is " + endHour
# Get minutes
endMinuteString = endDate.strftime ('%M')
print "End Minute " + endMinuteString
# Get year/month/day
#endYMD = endDate.strftime('%Y%m%d')
isoEndYMD = endDate.strftime('%Y%m%d')
endYMD = endDate.strftime('%Y-%m-%d')
print "End Date" + endDateString
endHour = endDate.strftime('%H')
print "end hour is " + endHour

#startDateString = startYMD+"T"+startHour+ startMinuteString +"00"
isoStartDateString = isoStartYMD+"T"+startHour+ startMinuteString +"00"
startDateString = startYMD + " " + str(startHour) + ":" + str(startMinuteString) + ":" + "00"
#endDateString = endYMD+"T"+str(endHour)+ endMinuteString +"00"
isoEndDateString = isoEndYMD+"T"+str(endHour)+ endMinuteString +"00"
endDateString = endYMD + " " + str(endHour) + ":" + str(endMinuteString) + ":" + "00"
print "Start: " + startDateString + "\nEnd: " + endDateString



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: Checks to make sure that the advisor and the appointee exist in the DB. 
# If not, they will be added to the student and appointment tables. 
# It will then add or remove an appointment based on the emailType variable.
# Uses variables: advisorFirstName, advisorLastName, advisorMiddleName, appointeeFirstName, 
# appointeeLastName, appointeeMiddleName, startDate, endDate, insertionID
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

db_path = os.path.expanduser('~')
db_path += '/.appt/appt.db'
con = lite.connect(db_path)
#con = lite.connect('../../../vagrant/appt.db')

if emailType == 'confirmed':
	print "Adding Appointment"

	with con:
		cur = con.cursor() 
		cur.execute("PRAGMA foreign_keys = 1")

		# Check to see if advisor exists in system get their ID key
		cur.execute("SELECT advisor_id, email_address FROM advisor WHERE email_address = " + "'" + advisorEmail +"'")
		rows = cur.fetchone()

		# Retrieve the advisor's ID
		# If not then add them to the system then retrieve the new ID
		if rows:
			advisorId = rows[0]
			print advisorId
		else:
			print "Advisor does not exist. Adding Advisor!"
			cur.execute ("INSERT INTO advisor (first_name, last_name, middle_name, email_address) VALUES ( ?, ?, ?, ?)", (advisorFirstName, advisorLastName, advisorMiddleName, advisorEmail))
			cur.execute("SELECT advisor_id, email_address FROM advisor WHERE email_address = " + "'" + advisorEmail +"'")
			rows = cur.fetchone()
			advisorId = rows[0]
			print "advisor ID: " + str(advisorId)
		# Check to see if student exists in system get their ID key
		cur.execute("SELECT student_id, email_address FROM student WHERE email_address = " + "'" + appointeeEmail +"'")
		rows = cur.fetchone()

		# Retrieve the student's ID
		# If not the add them to the system then retrieve the new ID
		if rows:
			studentId = rows[0]
			print studentId
		else:
			print "Student does not exist. Adding Student!"
			cur.execute ("INSERT INTO student (first_name, last_name, middle_name, email_address) VALUES ( ?, ?, ?, ?)", (appointeeFirstName, appointeeLastName, appointeeMiddleName, appointeeEmail))
			cur.execute("SELECT student_id, email_address FROM student WHERE email_address = " + "'" + appointeeEmail +"'")
			rows = cur.fetchone()
			studentId = rows[0]
			print "student ID: " + str(studentId)

		# Check to see if appointment already exists before adding it:
		print "checking to see if appointment exists"
		cur.execute("SELECT date_time_end FROM appointment WHERE date_time_end = " + "'" + endDateString +"'")
		rows = cur.fetchone()
		if rows:
			print "result of query " + rows[0] + "end date is " + endDateString
			# Double check to make sure that the rows do match
			if (rows[0] != endDateString):
				cur.execute("INSERT INTO appointment (fk_advisor_id, fk_student_id, date_time_start, date_time_end) VALUES (?, ?, ?, ?)", (advisorId, studentId, startDateString, endDateString))
			else:
				print "There already is an existing appointment on the books!"
		else:
			cur.execute("INSERT INTO appointment (fk_advisor_id, fk_student_id, date_time_start, date_time_end) VALUES (?, ?, ?, ?)", (advisorId, studentId, startDateString, endDateString))

		print "the id of the just inserted row is " + str(cur.lastrowid)
		insertionID = cur.lastrowid

if emailType == 'CANCELLED':
	with con:
		sendCancelEmail = "false";
		cur = con.cursor() 
		cur.execute("PRAGMA foreign_keys = 1")

		print "Removing Appointments"
		cur.execute("SELECT id, fk_student_id, date_time_start, date_time_end FROM appointment WHERE date_time_start = " + "'" + startDateString +"'")
		rows = cur.fetchone()

		# Make sure that there is an appointment with the right time
		if rows:
			# Make sure that the student cancelling the appointment is the actual student is correct
			appointmentID = rows[0]
			studentForeignKey = rows[1]
			print "Student foreign key is " + studentForeignKey
			cur.execute("SELECT email_address FROM student WHERE student_id = " + "'" + studentForeignKey +"'")
			rows2 = cur.fetchone()
			actualEmail = rows2[0]
			print "requesting student " + appointeeEmail 
			print " vs actual email " + actualEmail
			if appointeeEmail == actualEmail:
				print "canelling email"
				cur.execute("DELETE FROM appointment WHERE id = " + "'" + str(appointmentID) + "'")
				sendCancelEmail = "true"
			else:
				print "emails did not match! Appointment cancellation will not proceed"	
			

		else:
			print "No appointment in database!"


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: Sends an iCal Email that either notifies the user of an appointment or cancellation of appointment
# Inputs: 	emailusername, emailpassword
# 			advisorEmail, advisorLastName, advisorMiddleName, advisorLastName, appointeeFirstName, appointeeMiddleName, appointeeLastName
# 			isoStartDateString, isoEndDateString
# 			appointeeEmail
# 			dateString
# Output: 	Sends a MIME email in ical format with the calender information
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
if emailType == 'confirmed' and insertionID is not None:
	# Declare variables
	print "username is " + emailusername
	print "password is " + emailpassword
	print "advisor email is" + advisorEmail
	from_addr = emailusername
	to_addr = advisorEmail
	server = 'smtp.gmail.com'
	server_port = 587
	email_pwd = emailpassword # TODO: Move this to config.py module

	# email_subj = " test "
	email_subj = "Advising Appointment with " + advisorLastName + ", " + advisorMiddleName + " " + advisorFirstName + " confirmed for " + appointeeLastName + ", " + appointeeMiddleName + " " + appointeeFirstName

	print email_subj

	# find the unmodified time for the email
	expressionObject = re.compile('Time:\s+(.*)')
	matchObject = expressionObject.search(inputVar)	
	unmodifiedTime = matchObject.group(1)

	email_body = ("Advising Appointment with " + advisorLastName + ", " + advisorMiddleName + " " + advisorFirstName+ " confirmed\n"
	              "Name: " + appointeeLastName + ", " + appointeeMiddleName + " " + appointeeFirstName + "\n"
	              "Email: " + appointeeEmail + "\n"
	              "Date: " + dateString + "\n"
	              "Time: "+ unmodifiedTime + "\n\n\n"
  	              "Please contact support@engr.oregonstate.edu if you experience problems\n"
	             )

	print email_body

	student_email = appointeeEmail
	# Create CalAppt object

	test1 = CalAppt(from_addr, to_addr, server, server_port, email_pwd)

	# Send Calendar appt

	#test1.sendAppt(email_subj, email_body, str(insertionID), startDateString, endDateString, student_email)
	test1.sendAppt(email_subj, email_body, str(insertionID), isoStartDateString, isoEndDateString, student_email)

	# Print confirmation

	print "Appointment Email successfully sent."

if emailType == 'CANCELLED' and sendCancelEmail == 'true':
	# Declare variables
	print "username is " + emailusername
	print "password is " + emailpassword
	print "advisor email is" + advisorEmail
	from_addr = emailusername
	to_addr = advisorEmail
	server = 'smtp.gmail.com'
	server_port = 587
	email_pwd = emailpassword # TODO: Move this to config.py module

	# email_subj = " test "
	email_subj = "Advising Appointment CANCELLED"

	print email_subj

	# find the unmodified time for the email
	expressionObject = re.compile('Time:\s+(.*)')
	matchObject = expressionObject.search(inputVar)	
	unmodifiedTime = matchObject.group(1)

	email_body = ("Advising Appointment with " + advisorLastName + ", " + advisorMiddleName + " " + advisorFirstName+ " CANCELLED\n"
	              "Name: " + appointeeLastName + ", " + appointeeMiddleName + " " + appointeeFirstName + "\n"
	              "Email: " + appointeeEmail + "\n"
	              "Date: " + dateString + "\n"
	              "Time: "+ unmodifiedTime + "\n\n\n"
	              "Please contact support@engr.oregonstate.edu if you experience problems\n"
	             )

	print email_body

	student_email = appointeeEmail
	# Create CalAppt object

	test1 = CalAppt(from_addr, to_addr, server, server_port, email_pwd)

	# Send Calendar appt

	#test1.sendCncl(email_subj, email_body, str(appointmentID), startDateString, endDateString, student_email)
	test1.sendCncl(email_subj, email_body, str(appointmentID), isoStartDateString, isoEndDateString, student_email)

	# Print confirmation

	print "Appointment Cancellation successfully sent to" + advisorEmail
