"""
Author: Brianna Eskin
Function: Alter user_info table in case we decide to add/delete more columns/change indexing, etc
Alter the execution call to fit your purpose
"""

import mysql.connector as connection

mysql_connection = connection.connect(host = "localhost", user="data_man_group3", passwd="abc123", database="twitter_users")

mycursor = mysql_connection.cursor()

mycursor.execute("ALTER TABLE user_info MODIFY last_tweet VARCHAR(255)")
