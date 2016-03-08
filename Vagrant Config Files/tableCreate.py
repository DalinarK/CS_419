#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
print lite.sqlite_version   # should be 3.6.23.1

# advisors = (
#     ('Kevin', 'McGrath', 'D', 'dmcgrath@eecs.oregonstate.edu'),
# )

# students = (
# 	(1, 'Homer', 'J', 'Simpson', 'homerj@yahoo.com'),
# )

# appointments = (
# 	(1, 1, 1, 'jan', 'july'),
# )


con = lite.connect('../../../vagrant/appt.db')

with con:
    
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS advisor")
    cur.execute("DROP TABLE IF EXISTS student")
    cur.execute("DROP TABLE IF EXISTS appointment")
   # used to turn on foreign key constraints for the session
    cur.execute("PRAGMA foreign_keys = 1")    
    
    cur.execute("CREATE TABLE advisor (advisor_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, middle_name TEXT, email_address TEXT unique)")
    # cur.executemany("INSERT INTO advisor (first_name, last_name, middle_name, email_address) VALUES(?, ?, ?, ?)", advisors)

    cur.execute("CREATE TABLE student (student_id INTEGER PRIMARY KEY, first_name TEXT, middle_name TEXT, last_name TEXT, email_address TEXT unique)")
    # cur.executemany("INSERT INTO student VALUES(?, ?, ? , ?, ?)", students)

    cur.execute("CREATE TABLE appointment (id INTEGER PRIMARY KEY, fk_advisor_id TEXT, fk_student_id TEXT, date_time_start TEXT unique, date_time_end TEXT unique, FOREIGN KEY (fk_advisor_id) REFERENCES advisor(advisor_id), FOREIGN KEY (fk_student_id) REFERENCES student(student_id))")
    # cur.executemany("INSERT INTO appointment VALUES(?, ?, ?, ?, ?)", appointments)

with con:    
    
    cur = con.cursor()    
    cur.execute("SELECT * FROM advisor")

    rows = cur.fetchall()

    for row in rows:
        print row

    cur.execute("SELECT * FROM student")

    rows = cur.fetchall()

    for row in rows:
        print row

    cur.execute("SELECT * FROM appointment")

    rows = cur.fetchall()

    for row in rows:
        print row



