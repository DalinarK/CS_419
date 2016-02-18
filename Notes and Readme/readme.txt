.procmailrc is the procmail file that will look for an appointment email and forward it to the parse.py.

tableCreate.py is the initial script that will create the tables and also insert in dummy data

the test email file I'm using to feed into parse.py is called email.

To invoke parse py for testing I used this command:

cat email | python parse.py