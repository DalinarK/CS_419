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
print "filter pulled: " + nameLine
# Creates second filter used to split up the names and executes split()
expressionObject = re.compile('\W+')
nameList = expressionObject.split(nameLine)

print "length of nameList: " + str(len(nameList))

if len(nameList) == 2:
	# print "found two names"
	advisorFirstName = nameList[1]
	advisorLastName = nameList[0]
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
# Variables created: month (int), day (int), year(int)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

expressionObject = re.compile('Date: (.*)')
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

# Get the hours for startTime
# Check to see if the time is in PM and remove it + add 12 hours
expressionObject = re.compile('pm')
result = expressionObject.search(startTime)
if (result != None) & (result.group() == 'pm'):
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
if (result != None) and (result.group() == 'am'):
	# remove the pm from startTime
	print "found am replacing"
	startTime = expressionObject.sub("", startTime) 

# Get the minutes startTime
expressionObject = re.compile('(\d\d)')
print startTime
matchObject = expressionObject.search(startTime)
startMinute = matchObject.group()

# Get the hours for endTime
# Check to see if the time is in PM and remove it + add 12 hours
expressionObject = re.compile('pm')
result = expressionObject.search(endTime)
if (result != None) & (result.group() == 'pm'):
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
if (result != None) and (result.group() == 'am'):
	# remove the pm from endTime
	print "found am replacing"
	endTime = expressionObject.sub("", endTime) 

# Get the minutes endTime
expressionObject = re.compile('(\d\d)')
print endTime
matchObject = expressionObject.search(endTime)
endMinute = matchObject.group()

print "start Hour: " + startHour + " start Minute: " + startMinute
print "end Hour: " + endHour + " end Minute: " + endMinute

# construct start date
dateString = startHour  + " " + startMinute + " " + day + " " + month + " " + year
# print dateString
startDate = time.strptime(dateString, "%H %M %d %B %Y")
print dateString
