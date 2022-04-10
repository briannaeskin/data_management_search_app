"""
Author: Brianna Eskin
Function: Test that database and table is available when logged in after creation
"""

import mysql.connector as connection

mysql_connection = connection.connect(host = "localhost", user="data_man_group3", passwd="abc123", use_pure = True)

print("Databases")
mycursor = mysql_connection.cursor()
mycursor.execute("SHOW DATABASES")
for x in mycursor:
    print(x)

mycursor.execute("USE twitter_users")

print("Tables in database")
mycursor.execute("SHOW TABLES")
for x in mycursor:
    print(x)

print("Columns in table")
mycursor.execute("SHOW COLUMNS FROM user_info")
for x in mycursor:
    print(x)

mycursor.execute("SELECT COUNT(*) FROM user_info")
for x in mycursor:
    print(x)
