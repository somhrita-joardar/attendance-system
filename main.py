import scanner_module
import ctypes
import mysql.connector

import datetime
a = scanner_module.main()

# print(a)
a_list = a.split(";")
print(a)


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="h2"
)
r= a_list[0]
mycursor = mydb.cursor()
mycursor.execute(f'''UPDATE attendance
SET attendance = 'yes', date_time = NOW() WHERE rno = '{r}'
''')
mydb.commit()
mydb.close()