### Curses UI code ###

Basic curses UI for the scheduling app. Requires ncurses (incl. with all
Linux systems).

Make appointments.py executable (on Linux): 'chmod +x appointments.py'

##Update 2016-03-06:##

Deletions allegedly work. Code that sends deletion emails has been added
to delete_appt and the UI reacts the way I'd expect it to react. This
needs to be tested when the whole system is assembled in ONE PLACE, not
piecemeal in multiple subdirectories like it is now.

To play with this, a few things need to happen:

1. The ../PythonFiles/appt_email.py script needs to be in this directory.

2. Proper email credentials need to be added to delete_appt in
functions.py (these need to eventually be read from a shared configuration
file).

3. Just to get a database going, in this directory run
../tableCreate_withdates.py. Creates appts for the first few days of
March.
