import sys
import re
import time

print("Starting python script")
# fileStream = open("pythoncreatedfile", 'w')

# fileStream.write('swag \n')
# for line in sys.stdin:
	# fileStream.write (line),

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
# Notes: When performing any operation, make sure that advisorMiddleName actually exists
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Creates the filter
expressionObject = re.compile('Advising Signup with (.*)\sconfirmed')
# Executes the filter on inputVar and stores it in object matchObject then stores the result into 
# nameLine variable
matchObject = expressionObject.search(inputVar)
nameLine = matchObject.group(1)
# Creates second filter used to split up the names and executes split()
expressionObject = re.compile('\W+')
nameList = expressionObject.split(nameLine)

if len(nameList) == 2:
	# print "found two names"
	advisorFirstName = nameList[0]
	advisorLastName = nameList[1]
elif len(nameList) == 3:
	# print "found three names"
	advisorFirstName = nameList[0]
	advisorLastName = nameList[1]
	advisorMiddleName = nameList[2]
# If there are multiple names, only save the last name of the set
else:
	# print "found less than or more than one name"
	advisorFirstName = nameList[0]
	advisorLastName = nameList[-1]

# print "first name: " + advisorFirstName
# print "last naem: " + advisorLastName
# if len(nameList) == 3:
# 	print "middle name: " + advisorMiddleName

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
expressionObject = re.compile('\W+')
nameLine = matchObject.group(1)
nameList = expressionObject.split(nameLine)

if len(nameList) == 2:
	appointeeFirstName = nameList[0]
	appointeeLastName = nameList[1]
elif len(nameList) == 3:
	appointeeFirstName = nameList[0]
	appointeeLastName = nameList[1]
	appointeeMiddleName = nameList[2]
# If there are multiple names, only save the last name of the set
else:
	appointeeFirstName = nameList[0]
	appointeeLastName = nameList[-1]

# print "first name: " + appointeeFirstName
# print "last naem: " + appointeeLastName
# if len(nameList) == 3:
# 	print "middle name: " + appointeeMiddleName

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: parse out the user's email
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
expressionObject = re.compile('Email:\s*(.*)\s*')
matchObject = expressionObject.search(inputVar)	
appointeeEmail = matchObject.group(1)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Purpose: parse out the date and store it in the date variable
# Variables created: date
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

expressionObject = re.compile('Date: (.*)')
matchObject = expressionObject.search(inputVar)	
expressionObject = re.compile('\W+')
nameLine = matchObject.group(1)
dateList = expressionObject.split(nameLine)

print dateList
month = dateList[1]
year = dateList[3]
day = dateList[2]
# only keep the numbers and remove the suffixes like 'st' 'nd' etc
expressionObject = re.compile('\d*')
matchObject = expressionObject.search(day)	
day = matchObject.group()

# construct date
dateString = day + " " + month + " " + year
print dateString
date = time.strptime(dateString, "%d %B %Y")
print date
# full_msg = sys.stdin.readlines()

# msg = email.message_from_string(full_msg.join());

# to = msg['to']
# fromHeader = msg['from']
# subject = msg['subject']
# body = msg['body']

# fileStream.write(subject)