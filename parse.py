import sys
import re

print("Starting python script")
# fileStream = open("pythoncreatedfile", 'w')

# fileStream.write('swag \n')
# for line in sys.stdin:
	# fileStream.write (line),

inputVar = sys.stdin.read()
# Purpose: Find advisor first name and last and store it in variables
# If there is a middle name it will also get parsed out. If the number of names
# is greater than 3 or less than 2 then the first and last name will be the first and last elements
# in the parsed name list.
expressionObject = re.compile('Advising Signup with (.*)\sconfirmed')

matchObject = expressionObject.search(inputVar)
advisorLastName = matchObject.group(1)

print advisorLastName

expressionObject = re.compile('Advising Signup with (.*),\s(.*)\sconfirmed')

#Purpose: Find name of appointment maker
#Parses out the first and last name
# If there is a middle name it will also get parsed out. If the number of names
# is greater than 3 or less than 2 then the first and last name will be the first and last elements
# in the parsed name list.

expressionObject = re.compile('Name: (.*)')
matchObject = expressionObject.search(inputVar)	
expressionObject = re.compile('\W+')
nameLine = matchObject.group(1)
nameList = expressionObject.split(nameLine)

if len(nameList) == 2:
	# print "found two names"
	appointeeFirstName = nameList[0]
	appointeeLastName = nameList[1]
elif len(nameList) == 3:
	# print "found three names"
	appointeeFirstName = nameList[0]
	appointeeLastName = nameList[1]
	appointeeMiddleName = nameList[2]
# If there are multiple names, only save the last name of the set
else:
	# print "found less than or more than one name"
	appointeeFirstName = nameList[0]
	appointeeLastName = nameList[-1]

# print "first name: " + appointeeFirstName
# print "last naem: " + appointeeLastName
# if len(nameList) == 3:
# 	print "last name: " + appointeeMiddleName



# full_msg = sys.stdin.readlines()

# msg = email.message_from_string(full_msg.join());

# to = msg['to']
# fromHeader = msg['from']
# subject = msg['subject']
# body = msg['body']

# fileStream.write(subject)