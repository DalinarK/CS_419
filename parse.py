import sys
import email

print("Starting python script")
fileStream = open("pythoncreatedfile", 'w')

fileStream.write('test \n')

full_msg = sys.stdin.readlines()

msg = email.message_from_string(full_msg.join());

to = msg['to']
fromHeader = msg['from']
subject = msg['subject']
body = msg['body']

fileStream.write(subject)