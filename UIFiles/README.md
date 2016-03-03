### Curses UI code ###

Basic curses UI for the scheduling app. Requires ncurses (incl. with all
Linux systems).

Make appointments.py executable (on Linux): 'chmod +x appointments.py'

##Update 2016-03-03:##

Database is connected to UI and appointment deletions work. No email code
has been added yet so deleting an appointment just removes it from the
database.  The ../tableCreate_withdates.py script has been updated to
create more appointments to make testing a bit easier, at least from Feb
28th - Mar 2nd. Be sure to run that script in the same directory as the UI
scripts to build a sorta populated appt.db file.

Also, if there are no appointments, the appointment listing now displays
"No appointments..." and delete functionality SHOULD BE unavailable.

