"""
Author: Brianna Eskin
Function: Holds the search app, including the GUI
"""

from pymongo import MongoClient
import mysql.connector as connection

class Search:

    def __init__(self):
        """
        Initialize the search object by connecting to mySQL, MongoDB, and Redis
        """

        #MySQL Connection
        self.mysql_connection = connection.connect(host="localhost", user="data_man_group3", passwd="abc123",
                                              database="twitter_users")
        self.mysql_connection.autocommit = True
        self.cursor = mysql_connection.cursor(prepared=True)

        #MongoDB Connection
        self.client = MongoClient("mongodb+srv://data_man_group3:dkncO5uFyOd6IB5Y@cluster0.na33p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.twitter_data = client["twitter_data"]
        self.tweet_info_collection = twitter_data["tweet_info"]

        #Placeholder for Redis store