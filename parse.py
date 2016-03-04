import sys
import re
import datetime
import sqlite3 as lite

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
	advisorMiddleName = None
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
expressionObject = re.compile('Delivered-To: (.*)')
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

if len(nameList) == 2:
	appointeeFirstName = nameList[1]
	appointeeLastName = nameList[0]
	appointeeMiddleName = None
elif len(nameList) == 3:
	appointeeFirstName = nameList[2]
	appointeeLastName = nameList[0]
	appointeeMiddleName = nameList[1]
# If there are multiple names, only save the last name of the set
else:
	print "name length not 3 or 2"
	appointeeFirstName = nameList[0]
	appointeeLastName = nameList[-1]

print "Student first name: " + appointeeFirstName
print "Student last name: " + appointeeLastName
if len(nameList) == 3:
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
		startHour = int(startHour) + 12
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
		endHour = int(endHour) + 12
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
print startDate.strftime('%H %M %d %B %Y')


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: Checks to make sure that the advisor and the appointee exist in the DB. 
# If not, they will be added to the student and appointment tables. 
# It will then add or remove an appointment based on the emailType variable.
# Uses variables: advisorFirstName, advisorLastName, advisorMiddleName, appointeeFirstName, 
# appointeeLastName, appointeeMiddleName, startDate, endDate 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
con = lite.connect('appt.db')

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
		cur.execute("INSERT INTO appointment (fk_advisor_id, fk_student_id, date_time_start, date_time_end) VALUES (?, ?, ?, ?)", (advisorId, studentId, startDateString, endDateString))

if emailType == 'CANCELLED':
	with con:
		cur = con.cursor() 
		cur.execute("PRAGMA foreign_keys = 1")

		print "Removing Appointments"
		cur.execute("SELECT id, date_time_start, date_time_end FROM appointment WHERE date_time_start = " + "'" + startDateString +"'")
		rows = cur.fetchone()

		if rows:
			appointmentID = rows[0]
			print "Removing id " + str(appointmentID)
			cur.execute("DELETE FROM appointment WHERE id = " + "'" + str(appointmentID) + "'")

		else:
			print "No appointment in database!"