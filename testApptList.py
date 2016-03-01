import sqlite3 as lite
import datetime 
import time


# Selected calendar day, as it will be seen in the curses UI code
cal_selected = {
        'month': "February",
        'day'  : "29",
        'year' : "2016" }


#################################################
# Get the list of appointments from the database
#################################################

def get_appts():

    # Set up a new dictionary for appointment data
    appts = {}

    # IMPORTANT: SQLite3 only recognizes ISO8601 date strings.

    # Force 2-digit conversion of spelled-out month and day values,
    # required for ISO date string.
    padmonth = format(time.strptime(cal_selected['month'], '%B').tm_mon, '02d')
    padday   = format(time.strptime(cal_selected['day'], '%d').tm_mday, '02d')

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

    print "Appointments for " + isodate

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

    # Print out what we got, just to prove we got something...
    print appts


get_appts()
