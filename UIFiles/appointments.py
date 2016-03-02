#!/usr/bin/env python

#
# CS 419 Winter 2016, Group 10
# Simplified Advising Scheduling
#
# Dustin Dinh, Michael Marven, Erik Ratcliffe
#
# appointments.py - Main appointments application
#
# Requires: 
#    functions.py (provided)
#    ncurses libraries (incl. w/ Linux)
#    Python curses (incl. w/ Python)
#

# Scrolling list hints taken from UniCurses test_keymenu demo as well as
# YouTube video tutorials on UniCurses.


from functions import *
from curses import *


def main(stdscr):

    # Holds data about the appointment list. This dictionary is mutable so
    # it should not be necessary to make this global to "share" it.
    list_info = {
        'highlight': 0,         # highlighted line in list view
        'view_height': 0,       # number of lines in list view
        'max_y': 0,             # max height of list window
        'max_x': 0,             # max width of list window
        'highlight_offset': 0,  # offset from beg. of list to highlight
        'highlight_limit': 0,   # highest line number that's highlightable
        'start': 0,             # start of "window" of appts to show
        'end': 0,               # end of "window" of appts to show
        'n_items': 0            # number of items in appt list
        }


    ##############################################
    # Set up some base curses settings
    ##############################################

    use_default_colors()   # like the function says
    curs_set(False)        # no blinking cursor
    stdscr.keypad(True)    # keyboard support
    choice       = 0       # ENTER choice
    c            = 0       # character input
    max_y, max_x = stdscr.getmaxyx() # Y,X limits of term window

    # Color pairs (color #, foreground, background). -1 = default.
    init_pair(1, COLOR_WHITE, COLOR_CYAN)
    init_pair(2, COLOR_CYAN, -1)
    init_pair(3, COLOR_GREEN, -1)

    # Get the list of appointments
    menu_items = get_appts()


    ##############################################
    # Set up the various windows
    ##############################################

    # Create the "header" window
    header_str = " SIMPLIFIED ADVISING SCHEDULING "
    header_win = newwin(1, max_x - 6, 1, 3)
    header_win.addstr(0, (header_win.getmaxyx()[1]/2 - len(header_str)/2), header_str, color_pair(2))

    # Create the Appointment List "outline" window
    list_outline_win = gen_list_outline_window(max_y, max_x)

    # Create the Appointment List "container" window. This will
    # be (re)displayed when it's refreshed in the print function.
    list_win = newwin(max_y - 9, max_x - 6, 5, 3)
    list_win.keypad(True)  

    # Create the Calendar "outline" window
    cal_title = " Choose A New Date "
    help_str = " [t = today | q = quit] "
    popup_outline_win = gen_popup_outline_window(max_y, max_x, cal_title, help_str)

    # Create the Calendar "container" window. 
    cal_win = newwin(8, 20, popup_outline_win.getbegyx()[0]+2, popup_outline_win.getbegyx()[1]+4)
    cal_win.keypad(True)  

    # Create the Confirmation "container" window. 
    cnf_win = newwin(7, 20, popup_outline_win.getbegyx()[0]+2, popup_outline_win.getbegyx()[1]+4)
    cnf_win.keypad(True)  

    # Create the "footer" window
    footer_str = "[ (c) 2016 | Dustin Dinh | Michael Marven | Erik Ratcliffe ]"
    footer_win = newwin(1, max_x - 6, max_y - 2, 3)
    footer_win.addstr(0, (footer_win.getmaxyx()[1]/2 - len(footer_str)/2), footer_str, color_pair(2))

    # Send the header, list outline, and footer windows to the user
    header_win.refresh()
    list_outline_win.refresh()
    footer_win.refresh()


    ##############################################
    # Set up the geometry/sizing of the appt. list
    ##############################################

    reset_list(list_info, menu_items, list_win)


    ##################################################
    # Generate and send the first list of appointments
    ##################################################

    print_list(list_win, menu_items, list_info)


    ##############################################
    # Read user navigation
    ##############################################

    # List scrolling is accomplished by moving the list indices up or down
    # based on whether the user is going beyond the top of the list or the
    # bottom of the list. In either case, the end the user is extending
    # gets one new list item and one list item is removed from the
    # opposite end, then the list is refreshed. This gives the illusion of
    # scrolling, when really all it's doing is changing which N-items are
    # going to display in the list (there is no full-list scrolling behind
    # the viewport, in other words).

    # IMPORTANT: Don't re-query the database when scrolling! Only do it
    # when an appointment is deleted or when a new calendar day is selected.
    
    running = True
    while(running):

        # Flags whether or not we need to get a fresh appointment list
        rescan = False

        # Read keyboard input in the list window, not stdscr!
        c = list_win.getch()

        # NAVIGATION: UP
        # If cursor UP arrow or k (ASCII code 107)...
        if c == KEY_UP or c == 107:
            # Note: highlight != appointment array index! It only
            # refers to the line in the UI that is highlighted.
            if list_info['highlight'] == 1:
                # top-most appointment is highlighted...
                if list_info['start'] > 0:
                    # highlighted appointment isn't the first...
                    list_info['start'] -= 1
                    list_info['end'] -= 1
                    list_info['highlight_offset'] -= 1
                # else: 
                #     do nothing
            else:
                list_info['highlight'] -= 1


        # NAVIGATION: DOWN
        # If cursor DOWN arrow or j (ASCII code 106)...
        elif c == KEY_DOWN or c == 106:
            if list_info['highlight'] == list_info['highlight_limit']:
                # bottom-most appointment is highlighted...
                if list_info['end'] < list_info['n_items']:
                    # highlighted appointment isn't the last...
                    list_info['start'] += 1
                    list_info['end'] += 1
                    list_info['highlight_offset'] += 1
                # else: 
                #     do nothing
            else:
                list_info['highlight'] += 1


        # OPERATION: CALENDAR
        # If user hits c or C (for calendar, ASCII code 67 or 99)
        elif c == 67 or c == 99:
            # Clear out the list window
            list_win.erase()
            list_win.refresh()

            # Display the calendar 
            cal_title = " Choose A New Date "
            help_str = " [t = today | q = quit] "
            popup_outline_win = gen_popup_outline_window(max_y, max_x, cal_title, help_str)
            popup_outline_win.refresh()
            success = nav_cal(cal_win)

            # If we got a new date, signal that a fresh appointment list
            # is needed.
            if success:
                rescan = True

            # Update the list outline window with the new date.
            list_outline_win = gen_list_outline_window(max_y, max_x)
            list_outline_win.refresh()


        # OPERATION: DELETE APPOINTMENT
        # If user hits d or D (ASCII code 68 or 100)...
        elif c == 68 or c == 100:
            if list_info['n_items'] >= 1:
                # Choice points to the menu_items index, NOT the
                # appointment ID in the database!
                choice = list_info['highlight'] + list_info['highlight_offset'] - 1

                # Process (delete) the appointment.
                success = process_appt(max_y, max_x, cnf_win, menu_items, choice)

                # If an appointment was deleted, start the listing over again.
                # Reset values, recalculate list start/end, etc. 
                if success:
                    rescan = True


        # OPERATION: QUIT
        # If user hits ESC (ASCII code 27) or Q or q, quit.
        elif c == 81 or c == 113 or c == 27:
            running = False

        # Re-get the list of appointments
        if rescan: 

            # Get a fresh set of appointments from the database
            menu_items = get_appts()

            # Reset the list window to defaults
            reset_list(list_info, menu_items, list_win)

        # Print a fresh appointment listing
        print_list(list_win, menu_items, list_info)


    # End curses...wrapper (below) cleans things up.
    return 0


# Initializes curses and cleanly exits without destroying the terminal
wrapper(main)

