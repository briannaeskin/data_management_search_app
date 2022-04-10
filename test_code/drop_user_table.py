"""
Author: Brianna Eskin
Function: Delete entries from user table. Used for testing store_twitter_data only.
DO NOT run otherwise (will remove when done with store code).
"""

import mysql.connector as connection

mysql_connection = connection.connect(host="localhost", user="data_man_group3", passwd="abc123", database="twitter_users")

#Delete info from user_info table
mycursor = mysql_connection.cursor()
mycursor.execute("DELETE FROM user_info")
mysql_connection.commit()
print(mycursor.rowcount, " record(s) deleted")