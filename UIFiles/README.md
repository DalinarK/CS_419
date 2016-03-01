### Curses UI code ###

Basic curses UI for the scheduling app. Requires ncurses (incl. with all
Linux systems).

Make appointments.py executable (on Linux): 'chmod +x appointments.py'

##Update 2016-02-29:##

Database is connected to UI, but deletions have not been worked out yet.
Create an appt.db test database in the same directory as the UI by running
the tableCreate_withdates.py script (it's in the main repo directory).
Unless you add appointments to the sample entries in that script, there
are appointments for Feb 28 and 29 and March 1. No code has been added to
handle days without appointments (you just get a blank listing). Trying to
delete an appointment will result in the app crashing. Just sayin'.


