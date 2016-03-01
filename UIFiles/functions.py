#
# CS 419 Winter 2016, Group 10
# Simplified Advising Scheduling
#
# Dustin Dinh, Michael Marven, Erik Ratcliffe
#
# functions.py - Functions used in appointments.py
#

# Scrolling list hints taken from UniCurses test_keymenu demo as well as
# YouTube video tutorials on UniCurses.


import calendar
import datetime
import time
import sqlite3 as lite
from curses import *


# Selected calendar day
cal_selected = {
        'month': datetime.datetime.now().month,
        'day'  : datetime.datetime.now().day,
        'year' : datetime.datetime.now().year }


#################################################
# (Re)set settings for the appt list to defaults
#################################################

def reset_list(list_info, menu_items, list_win):

    # Line to highlight in the list view
    list_info['highlight'] = 1

    # How many items are in the appointments array
    list_info['n_items'] = len(menu_items)

    # Get/store dimensions of list_win
    list_info['max_y'] = list_win.getmaxyx()[0]
    list_info['max_x'] = list_win.getmaxyx()[1]

    # How many lines we have to display appointments
    list_info['view_height'] = list_info['max_y'] - 1

    # Difference between highlight and underlying appointment index
    list_info['highlight_offset'] = 0

    # Last viewable line allowed to be highlighted
    list_info['highlight_limit'] = 0

    # Determine range of appointments to display initially
    list_info['start'] = 0
    if list_info['view_height'] > list_info['n_items']:
        list_info['end'] = list_info['n_items']
        list_info['highlight_limit'] = list_info['n_items']
    else:
        list_info['end'] = list_info['view_height']
        list_info['highlight_limit'] = list_info['view_height']


#################################################
# Get the list of appointments from the database
#################################################

def get_appts():

    # Set up a new dictionary for appointment data
    appts = {}

    # IMPORTANT: SQLite3 only recognizes ISO8601 date strings.

    # Force 2-digit conversion of spelled-out month and day values,
    # required for ISO date string.
    padmonth = format(time.strptime(str(cal_selected['month']), '%m').tm_mon, '02d')
    padday   = format(time.strptime(str(cal_selected['day']), '%d').tm_mday, '02d')

    # Build an ISO8601 date string (NOTE: Is this really an ISO string?)
    isodate = str(cal_selected['year']) + "-" + str(padmonth) + "-" + str(padday)

    # SQLite3 query for appointments that match isodate.
    # Result set includes:
    #   [0] first_name  (student first name)
    #   [1} middle_name (student middle name)
    #   [2} last_name   (student last name)
    #   [3} appt_id     (appointment ID in the DB)
    #   [4} appt_t      (ISO date of start time)
    sql = "SELECT s.first_name, s.middle_name, s.last_name, a.id AS appt_id, a.date_time_start AS appt_t"
    sql += " FROM appointment AS a JOIN student AS s WHERE s.student_id = a.fk_student_id" 
    sql += " AND appt_t >= date('" + isodate + "') AND appt_t < date('" + isodate + "', '+1 day') ORDER BY appt_t"

    # Open the database. Of course, the database should exist first. Check
    # this.
    con = lite.connect('appt.db')

    with con:
        cur = con.cursor()
        cur.execute(sql)

        # Get the result set
        rows = cur.fetchall()

        # Add rows to appts list. Format the data into dictionary entries:
        #   id = appt_id
        #   name = first_name + middle_name + last_name
        #   time = date.strftime(isodate, "
        appt_n = 0
        for row in rows:

            # Create a datetime object from the appointment time string
            t = time.strptime(row[4], '%Y-%m-%d %H:%M:%S')
            appt_dt = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)

            # Appointment start time: appt_dt.strftime("%-I:%M%p")

            # Build the student name
            s_name = row[0]
            if row[1] != "":
                s_name += (" " + row[1])
            if row[2] != "":
                s_name += (" " + row[2])

            # Add the row to the dictionary
            appts[appt_n] = row[3], appt_dt.strftime("%-I:%M%p"), s_name
            appt_n += 1

    # An array of appointments for testing purposes...
    #appts = [
    #        "7:00 am - Bill Gates",
    #        "7:20 am - Lady Gaga",
    #        "7:40 am - Alfred Hitchcock",
    #        "8:00 am - Bernie Sanders",
    #        "8:20 am - Mary Queen of Scots",
    #        "8:40 am - Stephen King",
    #        "9:00 am - Barack Obama",
    #        "9:20 am - Lady Gaga",
    #        "9:40 am - Jackie Chan",
    #        "10:00 am - Kate Middleton",
    #        "10:20 am - Chris Christie",
    #        "10:40 am - Idris Elba",
    #        "11:00 am - Mary Queen of Scots",
    #        "11:20 am - Hillary Clinton",
    #        "11:40 am - Bill Gates",
    #        "12:00 pm - Bernie Sanders",
    #        "12:20 pm - Lady Gaga",
    #        "12:40 pm - Alfred Hitchcock",
    #        "1:00 pm - Bernie Sanders",
    #        "1:20 pm - Mary Queen of Scots",
    #        "1:40 pm - Stephen King",
    #        "2:00 pm - Barack Obama",
    #        "2:20 pm - Lady Gaga",
    #        "2:40 pm - Jackie Chan",
    #        "3:00 pm - Kate Middleton",
    #        "3:20 pm - Chris Christie",
    #        "3:40 pm - Idris Elba",
    #        "4:00 pm - Mary Queen of Scots",
    #        "4:20 pm - Hillary Clinton",
    #        "4:40 pm - Chris Rock" ]

    return appts


################################################
# Create the appointment list outline window
################################################

def gen_list_outline_window(max_y, max_x):

    # Create the window and box it
    list_outline_win = newwin(max_y - 6, max_x - 2, 3, 1)
    list_outline_win.attron(color_pair(2))
    list_outline_win.box()
    list_outline_win.attroff(color_pair(2))

    # Get window dimensions
    win_y = list_outline_win.getmaxyx()[0]
    win_x = list_outline_win.getmaxyx()[1]

    # Heading and help text strings
    appthead = calendar.month_name[cal_selected['month']] + " " + str(cal_selected['day']) + ', ' + str(cal_selected['year'])
    list_title = " Appointment List: " + appthead + " "
    help_str = " [c = change date | d = delete appt | q = quit] "

    # Add window heading, centered
    list_outline_win.addstr(0, (win_x/2 - len(list_title)/2), list_title, color_pair(3)|A_BOLD)

    # Turn off BOLD
    list_outline_win.attroff(A_BOLD)

    # Add help text, centered
    list_outline_win.addstr(win_y-1, (win_x/2 - len(help_str)/2), help_str, color_pair(3))

    return list_outline_win


################################################
# Create the popup outline window
################################################

def gen_popup_outline_window(max_y, max_x, win_title, help_str):

    # Create the window and box it
    popup_outline_win = newwin(12, 28, (max_y/2 - 6), (max_x/2 - 14))
    popup_outline_win.attron(color_pair(2))
    popup_outline_win.box()
    popup_outline_win.attroff(color_pair(2))

    # Get window dimensions
    win_y = popup_outline_win.getmaxyx()[0]
    win_x = popup_outline_win.getmaxyx()[1]

    # Add window heading, centered
    popup_outline_win.addstr(0, (win_x/2 - len(win_title)/2), win_title, color_pair(3)|A_BOLD)

    # Turn off BOLD
    popup_outline_win.attroff(A_BOLD)

    # Add help text, centered
    popup_outline_win.addstr(win_y-1, (win_x/2 - len(help_str)/2), help_str, color_pair(3))

    return popup_outline_win


################################################
# Do something with the selected appointment
################################################

# TODO: This is where appointments will be deleted.

def process_appt(max_y, max_x, cnf_win, menu_items, choice):

    # Display the confirmation popup
    cnf_title = " Confirm Deletion "
    help_str = " [y = yes | q = quit] "
    popup_outline_win = gen_popup_outline_window(max_y, max_x, cnf_title, help_str)
    popup_outline_win.refresh()

    # Clunky, but it works. Curses has little/no text formatting.
    msg1 = "  Are you sure you\n"
    msg2 = "want to delete this:\n\n"
    msg = msg1 + msg2 + menu_items[choice]

    # Print Confirmation 
    print_cnf(cnf_win, msg)

    # Prompt for a deletion confirmation
    success = False
    deciding = True
    while(deciding):
        # Read keyboard input from the confirmation window
        c = cnf_win.getch()

        # OPERATION: CONFIRM
        # If user hits y or Y (ASCII code 89 or 121)...
        if c == 89 or c == 121:
            success, del_item = delete_appt(menu_items, choice)
            if success:
                deciding = False
            else:
                msg = "ERROR: Could not delete \"" + menu_items[choice] + "\""
                print_cnf(cnf_win, msg)

        # OPERATION: QUIT THE CALENDAR
        # If user hits q or Q (ASCII code 81 or 113) or ESC (ASCII code 27)...
        elif c == 81 or c == 113 or c == 27:
            deciding = False

    return success


################################################
# Print the confirmation window
################################################

def print_cnf(cnf_win, msg):

    # Clear out the confirmation window
    cnf_win.erase()

    # Print confirmation message & appointment
    cnf_win.addstr(0, 0, msg)

    # Send the new calendar to the screen
    cnf_win.refresh()


################################################
# Delete an appointment
################################################

def delete_appt(menu_items, choice):

    success = False
    del_item = ""

    del_item = menu_items.pop(choice)

    if del_item != "":
        success = True

    return success, del_item


################################################
# Print the calendar
################################################

def print_cal(cal_win, cal_highlight):

    # Clear out the calendar window
    cal_win.erase()

    # Holds the last day of the month
    last_day = 0

    # Month and year of calendar
    calhead = calendar.month_name[cal_highlight['month']] + " " + str(cal_highlight['year'])

    # Print month, day, year heading, centered
    cal_win.addstr(0, (cal_win.getmaxyx()[1]/2 - len(calhead)/2), calhead)

    # Generate a collection of week arrays for the month and year
    calendar.setfirstweekday(calendar.SUNDAY)
    cal = calendar.monthcalendar(cal_highlight['year'], cal_highlight['month'])

    # Build the new calendar
    for i in range(0, len(cal)):
       for x in range(0, len(cal[i])):
           if cal[i][x] != 0:
               # If we have reached the highlighted day...
               if cal[i][x] == cal_highlight['day']:
                   cal_win.attron(A_REVERSE)
                   cal_win.addstr(i+2, x * 3, str(cal[i][x]))
                   cal_win.attroff(A_REVERSE)
               else:
                   cal_win.addstr(i+2, x * 3, str(cal[i][x]))
               # Save the new last day
               last_day = cal[i][x]
           else:
               cal_win.addstr(i+2, x * 3, ' ')

    # Send the new calendar to the screen
    cal_win.refresh()

    # nav_cal needs to know the last day of the month
    return last_day


################################################
# Navigate the calendar
################################################

def nav_cal(cal_win):

    cal_highlight = {
            'month': cal_selected['month'],
            'day'  : cal_selected['day'],
            'year' : cal_selected['year'] } 

    # Print the new calendar and grab the last day value
    last_day = print_cal(cal_win, cal_highlight)

    ################################################
    # Navigate the calendar
    ################################################

    browsing = True
    while(browsing):

        # Flags whether or not we changed the date
        success = False

        # Read keyboard input from the calendar window, not the list!
        c = cal_win.getch()

        # NAVIGATION: UP
        # If cursor UP arrow or k (ASCII code 107)...
        if c == KEY_UP or c == 107:
            if cal_highlight['month'] >= 2:
                cal_highlight['month'] -= 1
            else:
                cal_highlight['month'] = 12
                cal_highlight['year'] -= 1

            last_day = print_cal(cal_win, cal_highlight)

        # NAVIGATION: DOWN
        # If cursor DOWN arrow or j (ASCII code 106)...
        elif c == KEY_DOWN or c == 106:
            if cal_highlight['month'] <= 11:
                cal_highlight['month'] += 1
            else:
                cal_highlight['month'] = 1
                cal_highlight['year'] += 1

            last_day = print_cal(cal_win, cal_highlight)

        # NAVIGATION: LEFT
        # If cursor LEFT arrow or h (ASCII code 104)...
        elif c == KEY_LEFT or c == 104:
            if cal_highlight['day'] > 1:
                cal_highlight['day'] -= 1

            print_cal(cal_win, cal_highlight)

        # NAVIGATION: RIGHT
        # If cursor RIGHT arrow or l (ASCII code 108)...
        elif c == KEY_RIGHT or c == 108:
            if cal_highlight['day'] < last_day:
                cal_highlight['day'] += 1

            print_cal(cal_win, cal_highlight)

        # OPERATION: GO TO TODAY'S DATE
        # If user hits t or T (ASCII code 84 or 116)...
        elif c == 84 or c == 116:
            # Highlight today's date
            cal_highlight['month'] = datetime.datetime.now().month
            cal_highlight['day']   = datetime.datetime.now().day
            cal_highlight['year']  = datetime.datetime.now().year

            print_cal(cal_win, cal_highlight)

        # OPERATION: SELECT DATE
        # If user hits ENTER (ASCII code 10)...
        elif c == 10:
            cal_selected['month'] = cal_highlight['month']
            cal_selected['day']   = cal_highlight['day']
            cal_selected['year']  = cal_highlight['year']

            browsing = False
            success  = True

        # OPERATION: QUIT THE CALENDAR
        # If user hits q or Q (ASCII code 81 or 113) or ESC (ASCII code 27)...
        elif c == 81 or c == 113 or c == 27:
            browsing = False

    return success


################################################
# Print the appointment list
################################################

def print_list(list_win, menu_items, list_info):

    # Clear out the list window
    #werase(list_win)
    list_win.erase()

    # How many appointments have been displayed so far
    line_count = 1

    # Keeps track of the row we're on
    list_win_y = 0

    for i in range(list_info['start'], list_info['end']):
        # Build a string to display in the list
        appt_str = menu_items[i][1] + " - " + menu_items[i][2]

        if(list_info['highlight'] == line_count):
            # When we get to the highlight line, reverse it
            list_win.attron(A_REVERSE)
            list_win.addstr(list_win_y, 0, appt_str)
            list_win.attroff(A_REVERSE)
        else:
            list_win.addstr(list_win_y, 0, appt_str)

        # Clear to end of line.
        list_win.clrtoeol()

        # Increment to the next row...
        list_win_y += 1
        line_count += 1

    # Send updated appointment listing to the screen
    list_win.refresh()


