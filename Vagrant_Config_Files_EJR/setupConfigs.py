import re
import sys

emailAddress = "cs419appt@gmail.com"
emailPassword = "CS419ApptFinal"
userName = "cs419appt"
realName = "Dustin D"

# http://stackoverflow.com/questions/15312493/read-and-write-the-same-text-file
# replace username password in .fetchmairc with variables at top
replace_pattern = re.compile("user .*")
emailAddressString = "user \"" + emailAddress +"\""
emailPasswordString = "there with password \"" + emailPassword + "\""
with open(".fetchmailrc",'r+') as f:
    text = f.read()
    f.seek(0)
    f.truncate()
    f.write(replace_pattern.sub(emailAddressString,text))
    f.close()

replace_pattern = re.compile("there with password .*")
with open(".fetchmailrc",'r+') as f:
    text = f.read()
    f.seek(0)
    f.truncate()
    f.write(replace_pattern.sub(emailPassword,text))
    f.close()

# set settings for .muttrc
emailAddressString = "set from = " + emailAddress
replace_pattern = re.compile("set from = .*")
with open(".muttrc",'r+') as f:
    text = f.read()
    f.seek(0)
    f.truncate()
    f.write(replace_pattern.sub(emailAddressString,text))
    f.close()

realNameString = "set realname = " + realName
replace_pattern = re.compile("set realname = .*")
with open(".muttrc",'r+') as f:
    text = f.read()
    f.seek(0)
    f.truncate()
    f.write(replace_pattern.sub(realNameString,text))
    f.close()

# Set settings for .msmtprc
emailAddressString = "from \"" + emailAddress +"\""
replace_pattern = re.compile("from .*")
with open(".msmtprc",'r+') as f:
    text = f.read()
    f.seek(0)
    f.truncate()
    f.write(replace_pattern.sub(emailAddressString,text))
    f.close()

userNameString = "user \"" + userName +"\""
replace_pattern = re.compile("user .*")
with open(".msmtprc",'r+') as f:
    text = f.read()
    f.seek(0)
    f.truncate()
    f.write(replace_pattern.sub(userNameString,text))
    f.close()

emailPasswordString = "password \"" + emailPassword +"\""
replace_pattern = re.compile("password .*")
with open(".msmtprc",'r+') as f:
    text = f.read()
    f.seek(0)
    f.truncate()
    f.write(replace_pattern.sub(emailPasswordString,text))
    f.close()
# Set settings for credential.py
emailPasswordString = "emailpassword = \"" + emailPassword +"\""
replace_pattern = re.compile("emailpassword .*")
with open("credentials.py",'r+') as f:
    text = f.read()
    f.seek(0)
    f.truncate()
    f.write(replace_pattern.sub(emailPasswordString,text))
    f.close()

emailAddressString = "emailusername = \"" + emailAddress +"\""
replace_pattern = re.compile("emailusername .*")
with open("/vagrant/credentials.py",'r+') as f:
    text = f.read()
    f.seek(0)
    f.truncate()
    f.write(replace_pattern.sub(emailAddressString,text))
    f.close()