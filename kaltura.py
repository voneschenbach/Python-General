# Joins Kaltura user analytics file and enrollment export to provide csv
# showing just instructor users of Kaltura within a term.

import csv, sqlite3, datetime

# Create memory-only database to perform join
conn = sqlite3.connect(':memory:')
curs = conn.cursor()

# Create tables to hold data from export files
curs.execute("""
    CREATE TABLE faculty (
        first text,
        last text,
        email text
        )
    """)

curs.execute("""
    CREATE TABLE kaltura_users (
        email text,
        total integer,
        video integer,
        audio integer,
        image integer
        )
    """)

# Read export data file and insert into relevant tables
reader = csv.reader(open('faculty.csv', 'r'), delimiter=',')
for row in reader:
    curs.execute("INSERT INTO faculty values (?,?,?)", row)

reader = csv.reader(open('kaltura_users.csv', 'r'), delimiter=',')
for row in reader:
    curs.execute("INSERT INTO kaltura_users values (?,?,?,?,?)", row)

# Join the tables to show faculty Kaltura users
curs.execute("""
    SELECT first, last, kaltura_users.email, total, video, audio, image
    FROM faculty
    INNER JOIN kaltura_users
    ON faculty.email=kaltura_users.email
    """)
table_rows = curs.fetchall()

# Write the results to a CSV file
filename = 'faculty_kaltura_users_' + datetime.datetime.now().strftime('%Y%m%d_%H%M') + '.csv'
csvWriter = csv.writer(open(filename, 'w'))
header = (
    'Last Name', 'First Name', 'Email', 'Total' ,'Video', 'Audio', 'Image'
    )
csvWriter.writerow(header)
csvWriter.writerows(table_rows)

conn.commit()
conn.close()
