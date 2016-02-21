#
# CS 419 Winter 2016, Group 10
# Simplified Advising Scheduling
#
# Dustin Dinh, Michael Marven, Erik Ratcliffe
#
# appointments.py - Main appointments application
#
# Requires functions.py and unicurses.py
#

# Scrolling list hints taken from UniCurses test_keymenu demo as well as
# YouTube video tutorials on UniCurses.


from functions import *
from unicurses import *

# An array of choices for testing purposes...
# Keep this global ONLY FOR TESTING PURPOSES!
# TODO: Get rid of this!
menu_items = [
        "7:00 am - Bill Gates",
        "7:20 am - Lady Gaga",
        "7:40 am - Alfred Hitchcock",
        "8:00 am - Bernie Sanders",
        "8:20 am - Mary Queen of Scots",
        "8:40 am - Stephen King",
        "9:00 am - Barack Obama",
        "9:20 am - Lady Gaga",
        "9:40 am - Jackie Chan",
        "10:00 am - Kate Middleton",
        "10:20 am - Chris Christie",
        "10:40 am - Idris Elba",
        "11:00 am - Mary Queen of Scots",
        "11:20 am - Hillary Clinton",
        "11:40 am - Bill Gates",
        "12:00 pm - Bernie Sanders",
        "12:20 pm - Lady Gaga",
        "12:40 pm - Alfred Hitchcock",
        "1:00 pm - Bernie Sanders",
        "1:20 pm - Mary Queen of Scots",
        "1:40 pm - Stephen King",
        "2:00 pm - Barack Obama",
        "2:20 pm - Lady Gaga",
        "2:40 pm - Jackie Chan",
        "3:00 pm - Kate Middleton",
        "3:20 pm - Chris Christie",
        "3:40 pm - Idris Elba",
        "4:00 pm - Mary Queen of Scots",
        "4:20 pm - Hillary Clinton",
        "4:40 pm - Chris Rock" ]


def main():

    ##############################################
    # Set up stdscr and base curses settings
    ##############################################

    # Initialize the screen. This syntax must be adhered to.
    stdscr = initscr()

    # Curses ettings
    noecho()               # disable key echo
    cbreak()               # user input is immediately available
    start_color()          # start color system (not entirely necessary)
    use_default_colors()   # like the function says
    curs_set(False)        # no blinking cursor
    keypad(stdscr, True)   # keyboard support
    highlight    = 1       # default highlighted line in list
    choice       = 0       # ENTER choice
    c            = 0       # character input
    max_y, max_x = stdscr.getmaxyx() # Y,X limits of term window

    # Color pairs (color #, foreground, background). -1 = default.
    init_pair(1, COLOR_WHITE, COLOR_CYAN)
    init_pair(2, COLOR_CYAN, -1)
    init_pair(3, COLOR_GREEN, -1)

    # Get the list of appointments
    # TODO: This function will get appointments from the database
    #menu_items = get_appts()


    ##############################################
    # Set up the various windows
    ##############################################

    # Create the "header" window
    header_str = " SIMPLIFIED ADVISING SCHEDULING "
    header_win = newwin(1, max_x - 6, 1, 3)
    mvwaddstr(header_win, 0, (header_win.getmaxyx()[1]/2 - len(header_str)/2), header_str, COLOR_PAIR(2))

    # Create the Appointment List "outline" window
    list_outline_win = gen_list_outline_window(max_y, max_x)

    # Create the Appointment List "container" window. This will
    # be (re)displayed when it's refreshed in the print function.
    list_win = newwin(max_y - 9, max_x - 6, 5, 3)
    keypad(list_win, True)  

    # Create the Calendar "outline" window
    cal_title = " Choose A New Date "
    help_str = " [t = today | q = quit] "
    popup_outline_win = gen_popup_outline_window(max_y, max_x, cal_title, help_str)

    # Create the Calendar "container" window. 
    cal_win = newwin(7, 20, popup_outline_win.getbegyx()[0]+2, popup_outline_win.getbegyx()[1]+4)
    keypad(cal_win, True)  

    # Create the Confirmation "container" window. 
    cnf_win = newwin(7, 20, popup_outline_win.getbegyx()[0]+2, popup_outline_win.getbegyx()[1]+4)
    keypad(cnf_win, True)  

    # Create the "footer" window
    footer_str = "[ (c) 2016 | Dustin Dinh | Michael Marven | Erik Ratcliffe ]"
    footer_win = newwin(1, max_x - 6, max_y - 2, 3)
    mvwaddstr(footer_win, 0, (footer_win.getmaxyx()[1]/2 - len(footer_str)/2), footer_str, COLOR_PAIR(2))

    # Send the header, list outline, and footer windows to the user
    wrefresh(header_win)
    wrefresh(list_outline_win)
    wrefresh(footer_win)


    ##############################################
    # Set up the geometry/sizing of the appt. list
    ##############################################

    # How many items are in the appointments array
    n_items = len(menu_items)

    # How many lines we have to display appointments
    list_view_height = list_win.getmaxyx()[0]  - 1

    # Difference between highlight and underlying appointment index
    list_highlight_offset = 0

    # Last viewable line allowed to be highlighted
    list_highlight_limit = 0

    # Determine range of appointments to display initially
    list_start = 0
    if list_view_height > n_items:
        list_end = n_items
        list_highlight_limit = n_items
    else:
        list_end = list_view_height
        list_highlight_limit = list_view_height

    # Generate and send the first list of appointments
    print_list(list_win, menu_items, highlight, list_start, list_end)


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
    
    running = True
    while(running):
        # Read keyboard input in the list window, not stdscr!
        c = wgetch(list_win)

        # NAVIGATION: UP
        # If cursor UP arrow or k (ASCII code 107)...
        if c == KEY_UP or c == 107:
            # Note: highlight != appointment array index! It only
            # refers to the line in the UI that is highlighted.
            if highlight == 1:
                # top-most appointment is highlighted...
                if list_start > 0:
                    # highlighted appointment isn't the first...
                    list_start -= 1
                    list_end -= 1
                    list_highlight_offset -= 1
                # else: 
                #     do nothing
            else:
                highlight -= 1


        # NAVIGATION: DOWN
        # If cursor DOWN arrow or j (ASCII code 106)...
        elif c == KEY_DOWN or c == 106:
            if highlight == list_highlight_limit:
                # bottom-most appointment is highlighted...
                if list_end < n_items:
                    # highlighted appointment isn't the last...
                    list_start += 1
                    list_end += 1
                    list_highlight_offset += 1
                # else: 
                #     do nothing
            else:
                highlight += 1


        # OPERATION: CALENDAR
        # If user hits c or C (for calendar, ASCII code 67 or 99)
        elif c == 67 or c == 99:
            # Clear out the list window
            werase(list_win)
            wrefresh(list_win)

            # Display the calendar 
            cal_title = " Choose A New Date "
            help_str = " [t = today | q = quit] "
            popup_outline_win = gen_popup_outline_window(max_y, max_x, cal_title, help_str)
            wrefresh(popup_outline_win)
            nav_cal(cal_win)

            # Update the list outline window with the new date.
            list_outline_win = gen_list_outline_window(max_y, max_x)
            wrefresh(list_outline_win)

        # OPERATION: DELETE APPOINTMENT
        # If user hits d or D (ASCII code 68 or 100)...
        elif c == 68 or c == 100:
            if n_items >= 1:
                choice = highlight + list_highlight_offset - 1

                # Display the choice in the footer window (for debugging)
                success = process_appt(max_y, max_x, cnf_win, menu_items, choice)

                # If an appointment was deleted, start the listing over again.
                # Reset values, recalculate list start/end, etc. 
                # TODO: Put these settings in a dictionary and use a
                # function to change them!
                if success:
                    highlight = 1

                    # How many items are in the appointments array
                    n_items = len(menu_items)

                    # How many lines we have to display appointments
                    list_view_height = list_win.getmaxyx()[0]  - 1

                    # Reset diff. between highlight and underlying appointment index
                    list_highlight_offset = 0

                    # Reset last viewable line allowed to be highlighted
                    list_highlight_limit = 0

                    # Determine range of appointments to display initially
                    list_start = 0
                    if list_view_height > n_items:
                        list_end = n_items
                        list_highlight_limit = n_items
                    else:
                        list_end = list_view_height
                        list_highlight_limit = list_view_height


        # OPERATION: QUIT
        # If user hits ESC (ASCII code 27) or Q or q, quit.
        elif c == 81 or c == 113 or c == 27:
            running = False

        # Get the list of appointments
        # TODO: This function will get appointments from the database
        #menu_items = get_appts()

        # Print a fresh appointment listing
        print_list(list_win, menu_items, highlight, list_start, list_end)


    # End curses
    refresh()
    endwin()
    return 0

if(__name__ == "__main__"):
    main()

