"""
Author: Brianna Eskin
Function: Creates database and user table using MySQL.
"""

import mysql.connector as connection

def create_database_and_table(mysql_connection):
    mycursor = mysql_connection.cursor()

    #Try and create database
    try:
        mycursor.execute("CREATE DATABASE twitter_users")
    except Exception as e:
        print(e)

    # Connect to twitter_users database
    mysql_connection = connection.connect(host="localhost", user="data_man_group3", passwd="abc123", database="twitter_users")
    mycursor = mysql_connection.cursor()

    #Try and create table
    try:
        mycursor.execute("CREATE TABLE user_info (id BIGINT PRIMARY KEY, name VARCHAR(255), screen_name VARCHAR(255), \
    followers_count INT, friends_count INT, num_tweets INT, num_times_retweet INT, last_tweet BIGINT)")
    except Exception as e:
        print(e)

if __name__ == "main":
    mysql_connection = connection.connect(host="localhost", user="data_man_group3", passwd="abc123", use_pure=True)
    create_database_and_table(mysql_connection)
