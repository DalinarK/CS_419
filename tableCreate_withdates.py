#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3 as lite
import sys
print lite.sqlite_version 

advisors = (
    ('Kevin', 'McGrath', 'D', 'dmcgrath@eecs.oregonstate.edu'),
    ('Antonin', 'Scalia', '', 'scalia@scotus.gov'),
    ('Barack', 'Obama', 'H', 'pres@whitehouse.gov'),
    ('Walt', 'Disney', '', 'walt@disney.com'),
)

students = (
    ('Homer', 'J', 'Simpson', 'homerj@yahoo.com'),
    ('Rust', 'B', 'Gone', 'rbg@gmail.com'),
    ('Roscoe', 'P', 'Coltrane', 'rosco@hotmail.com'),
    ('John', 'Wayne', 'Gacy', 'jwg@fedprison.gov'),
    ('Lady', 'Gaga', '', 'lady@gaga.com'),
    ('Remy', '', 'Sherwood', 'remy@canyonjam.net'),
    ('Suki', '', 'Sherwood', 'suki@canyonjam.net'),
)

appointments = (
    (1, 2, '2016-02-28 13:20:00', '2016-02-28 13:40:00'),
    (2, 1, '2016-02-28 13:40:00', '2016-02-28 14:00:00'),
    (4, 3, '2016-02-29 13:00:00', '2016-02-29 13:20:00'),
    (1, 4, '2016-02-29 13:20:00', '2016-02-29 13:40:00'),
    (1, 5, '2016-02-29 13:40:00', '2016-02-29 14:00:00'),
    (3, 1, '2016-03-01 10:00:00', '2016-03-01 10:20:00'),
    (3, 2, '2016-03-01 10:20:00', '2016-03-01 10:40:00'),
    (3, 3, '2016-03-01 10:40:00', '2016-03-01 11:00:00'),
    (3, 5, '2016-03-01 11:00:00', '2016-03-01 11:20:00'),
    (3, 1, '2016-03-02 10:00:00', '2016-03-02 10:20:00'),
    (3, 2, '2016-03-02 10:20:00', '2016-03-02 10:40:00'),
    (3, 4, '2016-03-02 10:40:00', '2016-03-02 11:00:00'),
    (3, 5, '2016-03-02 11:00:00', '2016-03-02 11:20:00'),
)


con = lite.connect('appt.db')

with con:
    
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS advisor")
    cur.execute("DROP TABLE IF EXISTS student")
    cur.execute("DROP TABLE IF EXISTS appointment")
   # used to turn on foreign key constraints for the session
    cur.execute("PRAGMA foreign_keys = 1")    
    
    cur.execute("CREATE TABLE advisor (advisor_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, middle_name TEXT, email_address TEXT unique)")
    cur.executemany("INSERT INTO advisor (first_name, last_name, middle_name, email_address) VALUES(?, ?, ?, ?)", advisors)

    cur.execute("CREATE TABLE student (student_id INTEGER PRIMARY KEY, first_name TEXT, middle_name TEXT, last_name TEXT, email_address TEXT unique)")
    cur.executemany("INSERT INTO student (first_name, middle_name, last_name, email_address) VALUES(?, ? , ?, ?)", students)

    cur.execute("CREATE TABLE appointment (id INTEGER PRIMARY KEY, fk_advisor_id TEXT, fk_student_id TEXT, date_time_start TEXT unique, date_time_end TEXT unique, FOREIGN KEY (fk_advisor_id) REFERENCES advisor(advisor_id), FOREIGN KEY (fk_student_id) REFERENCES student(student_id))")
    cur.executemany("INSERT INTO appointment (fk_advisor_id, fk_student_id, date_time_start, date_time_end) VALUES(?, ?, ?, ?)", appointments)

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

