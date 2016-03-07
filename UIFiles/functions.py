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
import os.path
from appt_email import CalAppt


# Selected calendar day
cal_selected = {
        'month': datetime.datetime.now().month,
        'day'  : datetime.datetime.now().day,
        'year' : datetime.datetime.now().year }


#################################################
# Connect to the database
#################################################

def db_connect():

    #db_path = os.path.expanduser('~')
    #db_path += '/.appts/appt.db'
    #db_path += '/.appts/appt.db'
    db_path = "appt.db"
    con = lite.connect(db_path)

    return con


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
    #
    #   [0] first_name  (student first name)
    #   [1] middle_name (student middle name)
    #   [2] last_name   (student last name)
    #   [3] s_email     (student email address)
    #   [4] appt_id     (appointment ID in the DB)
    #   [5] appt_st     (ISO datetime of appt start time)
    #   [6] appt_et     (ISO datetime of appt end time)
    #
    # Results are ordered by appt_st (start time).
    #
    sql = "SELECT s.first_name, s.middle_name, s.last_name, s.email_address AS s_email,"
    sql += " a.id AS appt_id, a.date_time_start AS appt_st, a.date_time_end AS appt_et"
    sql += " FROM appointment AS a JOIN student AS s WHERE s.student_id = a.fk_student_id" 
    sql += " AND appt_st >= date('" + isodate + "')"
    sql += " AND appt_st < date('" + isodate + "', '+1 day')"
    sql += " ORDER BY appt_st"

    # Open the database.
    con = db_connect()

    with con:
        cur = con.cursor()
        cur.execute(sql)

        # Get the result set
        rows = cur.fetchall()

        # Add rows to appts list
        appt_n = 0
        for row in rows:

            # Create a datetime object from the appointment start time
            # NOTE: For now, ISO dates are formatted like so: YYYY-MM-DD HH:MM:SS
            ts = time.strptime(row[5], '%Y-%m-%d %H:%M:%S')
            appt_sdt = datetime.datetime(ts.tm_year, ts.tm_mon, ts.tm_mday, ts.tm_hour, ts.tm_min, ts.tm_sec)

            # Create a datetime object from the appointment end time
            # NOTE: For now, ISO dates are formatted like so: YYYY-MM-DD HH:MM:SS
            te = time.strptime(row[6], '%Y-%m-%d %H:%M:%S')
            appt_edt = datetime.datetime(te.tm_year, te.tm_mon, te.tm_mday, te.tm_hour, te.tm_min, te.tm_sec)

            # Build the student name
            s_name = row[0]
            if row[1] != "":
                s_name += (" " + row[1])
            if row[2] != "":
                s_name += (" " + row[2])

            # Add the row to the appts dictionary. Each record should end up 
            # with the following items, in order:
            #
            #   [0] appointment ID in the DB
            #   [1] ISO datetime of appt start time
            #   [2] ISO datetime of appt end time
            #   [3] student full name
            #   [4] student email
            # 
            appts[appt_n] = row[4], appt_sdt, appt_edt, s_name, row[3]
            appt_n += 1

    # Close the database connection
    con.close()

    # Return appointment dictionary
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

def gen_popup_outline_window(max_y, max_x, height, width, win_title, help_str):

    # Create the window and box it
    origin_y = (max_y/2 - height/2)
    origin_x = (max_x/2 - width/2)
    popup_outline_win = newwin(height, width, origin_y, origin_x)
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

def process_appt(max_y, max_x, menu_items, choice):

    # Build the appointment string. We need to measure this to determine
    # the width of the confirmation popup.
    msg = menu_items[choice][1].strftime("%-I:%M%p") + " - " + menu_items[choice][3]

    # Display the confirmation popup
    cnf_title = " Confirm Deletion "
    help_str = " [y = yes | q = quit] "
    popup_outline_win = gen_popup_outline_window(max_y, max_x, 5, len(msg)+6, cnf_title, help_str)
    popup_outline_win.refresh()

    # Build the confirmation content window (contains the msg)
    cnf_win = newwin(2, len(msg), max_y/2, (max_x/2 - len(msg)/2))
    cnf_win.keypad(True)  

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
            success = delete_appt(max_y, max_x, menu_items, choice)
            if success:
                deciding = False
            else:
                # Clear out the confirmation window and outline
                cnf_win.erase()
                popup_outline_win.erase()

                # A general error message re: sending cancellation email 
                msg = "An error occurred when emailing the cancellation."

                # Display the error popup
                err_title = " Cancellation Error "
                help_str = " [q = quit] "
                popup_outline_win = gen_popup_outline_window(max_y, max_x, 5, len(msg)+6, err_title, help_str)
                popup_outline_win.refresh()

                # Build the error message content window (contains the msg)
                err_win = newwin(2, len(msg), max_y/2, (max_x/2 - len(msg)/2))
                err_win.keypad(True)  

                # Print error 
                print_cnf(err_win, msg)

                deciding = True
                while(deciding):
                    # Read keyboard input from the confirmation window
                    c = err_win.getch()

                    # OPERATION: QUIT THE ERROR POPUP
                    # If user hits q or Q (ASCII code 81 or 113) or ESC (ASCII code 27)...
                    if c == 81 or c == 113 or c == 27:
                        deciding = False

                #msg = "ERROR: Could not delete appt ID \"" + str(menu_items[choice][0]) + "\""
                #print_cnf(cnf_win, msg)

        # OPERATION: QUIT THE CONFIRMATION
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

# The menu_items[] list should contain the following:
#
#   [0] appointment ID in the DB
#   [1] ISO datetime of appt start time (YYYY-MM-DD HH:MM:SS)
#   [2] ISO datetime of appt end time (YYYY-MM-DD HH:MM:SS)
#   [3] student full name
#   [4] student email

def delete_appt(max_y, max_x, menu_items, choice):

    # Change to true if this function does everything it needs to do
    success = False

    # Open the database
    con = db_connect()

    # Parse start and end datetime structs from the date strings
    ts = time.strptime(str(menu_items[choice][1]), '%Y-%m-%d %H:%M:%S')
    te = time.strptime(str(menu_items[choice][2]), '%Y-%m-%d %H:%M:%S')

    # Make start and end datetime objects from datetime struct data
    appt_sdt = datetime.datetime(ts.tm_year, ts.tm_mon, ts.tm_mday, ts.tm_hour, ts.tm_min, ts.tm_sec)
    appt_edt = datetime.datetime(te.tm_year, te.tm_mon, te.tm_mday, te.tm_hour, te.tm_min, te.tm_sec)

    # Build ISO date strings (used by iCalendar) from datetime struct
    # data. Format: YYYYMMDDTHHMMSSZ
    iso_start = str(ts.tm_year) + str(ts.tm_mon) + str(ts.tm_mday) + "T" + \
                str(ts.tm_hour) + str(ts.tm_min) + str(ts.tm_sec) + "Z"
    iso_end   = str(te.tm_year) + str(te.tm_mon) + str(te.tm_mday) + "T" + \
                str(te.tm_hour) + str(te.tm_min) + str(te.tm_sec) + "Z"

    # Build appointment date and start/end time strings from datetime objects
    appt_date  = appt_sdt.strftime("%A, %B %-d, %Y")
    appt_stime = appt_sdt.strftime("%-I:%M%p")
    appt_etime = appt_edt.strftime("%-I:%M%p")

    # Declare variables
    # TODO: Grab CAPITALIZED VALUES from a shared config file!
    from_addr = "FROM_ADDR"
    to_addr = "TO_ADDR"
    server = 'smtp.gmail.com'
    server_port = 587
    email_pwd = "FROM_PASS" # TODO: Move this to config.py module
    
    email_subj = "Advising Signup Cancellation"
    email_body = ("Advising Signup CANCELLED\n"
                  "Name: "  + menu_items[choice][3] + "\n"
                  "Email: " + menu_items[choice][4] + "\n"
                  "Date: "  + appt_date + "\n"
                  "Time: "  + appt_stime + " - " + appt_etime
                 )
    appointment_id = str(menu_items[choice][0])
    start_dtim = iso_start
    end_dtim = iso_end
    student_email = menu_items[choice][4]
    
    # Create CalAppt object
    cncl_mail = CalAppt(from_addr, to_addr, server, server_port, email_pwd)
    
    # Send Calendar appt. If no exceptions were encountered during the
    # sending of the email, 'emailed' will be set to True.
    emailed = cncl_mail.sendCncl(email_subj, email_body, appointment_id, start_dtim, end_dtim, student_email)
    
    if emailed:
        # Delete the item from the database
        con.execute("DELETE FROM appointment WHERE id=?", (menu_items[choice][0],))
        con.commit()

        # Make sure one change was made to the database. 
        if con.total_changes == 1:
            success = True

    # Close the database connection
    con.close()

    return success


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
    list_win.erase()

    # How many appointments have been displayed so far
    line_count = 1

    # Keeps track of the row we're on
    list_win_y = 0

    # If we have appointments to show...
    if list_info['n_items'] > 0:
        for i in range(list_info['start'], list_info['end']):
            # Build a string to display in the list
            #
            # The menu_items[] list should contain the following:
            #
            #   [0] appointment ID in the DB
            #   [1] ISO datetime of appt start time
            #   [2] ISO datetime of appt end time
            #   [3] student full name
            #   [4] student email

            # Create AM/PM time string from ISO datetime of start
            appt_t = menu_items[i][1].strftime("%-I:%M%p")

            # Combine appt AM/PM time w/ student name 
            appt_str = appt_t + " - " + menu_items[i][3]

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
    else:
        # ...otherwise, say there are no appointments.
        list_win.addstr(list_win_y, 0, "No appointments...")

    # Send updated appointment listing to the screen
    list_win.refresh()


