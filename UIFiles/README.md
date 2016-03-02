### Curses UI code ###

Basic curses UI for the scheduling app. Requires ncurses (incl. with all
Linux systems).

Make appointments.py executable (on Linux): 'chmod +x appointments.py'

##Update 2016-03-02:##

Database is connected to UI and appointment deletions work. No email code
has been added yet so deleting an appointment just removes it from the
database.  The ../tableCreate_withdates.py script has been updated to
create more appointments to make testing a bit easier, at least on March
2nd. Be sure to run that script in the same directory as the UI scripts to
build a sorta populated appt.db file.

There is still no code to handle days without appointments (you just get a
blank listing). 



