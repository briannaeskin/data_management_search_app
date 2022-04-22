"""
Author: Brianna Eskin
Function: Write data to MySQL and MongoDB datastores
"""

from datetime import datetime, timezone
import json
import mysql.connector as connection
from pymongo import MongoClient
import re

def setup_mysql():
    """
    Function: Setup mySQL connection, check if table already exists, and drop and recreate if it does. We do this for
    testing purposes so we don't need to wipe table continuously during testing
    """

    CREATE_TABLE_QUERY = """
    CREATE TABLE user_info (
    user_id VARCHAR(255),
    name VARCHAR(255),
    screen_name VARCHAR(255),
    followers_count INT,
    friends_count INT,
    num_tweets INT,
    last_tweet_id VARCHAR(255),
    PRIMARY KEY(user_id),
    INDEX(screen_name, followers_count, friends_count, num_tweets)
    );
    """

    mysql_connection = connection.connect(host="localhost", user="data_man_group3", passwd="abc123",
                                          database="twitter_users")
    mysql_connection.autocommit = True
    cursor = mysql_connection.cursor(prepared = True)
    cursor.execute("SHOW TABLES LIKE 'user_info'")
    result = cursor.fetchone()
    if result:
        print("Dropping user_info table since it already exists")
        cursor.execute("DROP TABLE user_info")
    print("Creating user_info table")
    cursor.execute(CREATE_TABLE_QUERY)
    return mysql_connection, cursor

def setup_mongo():
    """
    Function: Setup mongoDB connection, check if database/collection already exists, and drop and recreate if it does. We do this for
    testing purposes so we don't need to wipe table continuously during testing
    """
    client = MongoClient("mongodb+srv://data_man_group3:dkncO5uFyOd6IB5Y@cluster0.na33p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    twitter_data = client["twitter_data"]
    collections = twitter_data.list_collection_names()
    if "tweet_info" in collections:
        print("Dropping tweet_info collection in twitter_data datastore since it already exists")
        twitter_data.tweet_info.drop()
    tweet_info = twitter_data["tweet_info"]

    return twitter_data

def mongo_indexes(twitter_data):
    twitter_data.tweet_info.create_index("tweet_id")
    twitter_data.tweet_info.create_index("created_date")
    twitter_data.tweet_info.create_index("user_id")
    twitter_data.tweet_info.create_index("favorite_count")
    twitter_data.tweet_info.create_index("retweet_count")

def insert_mysql(data, connection, cursor, insert):
    """
    Update mySQL database. Can either insert (if new entry), or update (if user already exists)
    """
    INSERT_QUERY = """
    INSERT INTO user_info (
    user_id, name, screen_name, followers_count, friends_count, num_tweets, last_tweet_id
    )
    VALUES (
    '{}','{}','{}',{},{},{},'{}'
    );
    """.format(data[0], data[1], data[2], data[3], data[4], data[5], data[6])

    UPDATE_QUERY = """
    UPDATE user_info SET name = '{}', screen_name = '{}', followers_count = {}, friends_count = {}, num_tweets = {},
    last_tweet_id = '{}' WHERE user_id = '{}';
    """.format(data[1], data[2], data[3], data[4], data[5], data[6], data[0])

    if insert:
        #print("INSERT_QUERY: ", INSERT_QUERY)
        cursor.execute(INSERT_QUERY)
    else:
        print("UPDATE_QUERY: ", UPDATE_QUERY)
        cursor.execute(UPDATE_QUERY)
        connection.commit()


def insert_mongo(data, twitter_data):
    """
    Insert document to MongoDB. Already know this is new since we check if exists in main method
    """
    twitter_data.tweet_info.insert_one(data)

def convert_time_created(created_at):
    """
    Convert created_at string to datetime that can be used for search purposes
    """
    #print("Starting time convert")
    time_list = created_at.split()
    month = time_list[1]
    day = time_list[2]
    time = time_list[3].split(':')
    hour = time[0]
    min = time[1]
    sec = time[2]
    year = time_list[5]

    #Convert month into number for datetime call
    if month == "Jan":
        month = 1
    elif month == "Feb":
        month = 2
    elif month == "Mar":
        month = 3
    elif month == "Apr":
        month = 4
    elif month == "May":
        month = 5
    elif month == "Jun":
        month = 6
    elif month == "Jul":
        month = 7
    elif month == "Aug":
        month = 8
    elif month == "Sep":
        month = 9
    elif month == "Oct":
        month = 10
    elif month == "Nov":
        month = 11
    elif month == "Dec":
        month = 12

    #print("Ready to call datetime function")
    new_date = datetime(year = int(year), month = month, day = int(day), hour = int(hour), minute = int(min),
                        second = int(sec), tzinfo = timezone.utc)
    #print("Finished with time convert")
    return new_date


if __name__ == "__main__":
    mysql_connection, mysql_cursor = setup_mysql()
    twitter_data = setup_mongo()

    id_set = set()

    with open("corona-out-2.json", "r") as f1:
        for line in f1:
            try:
                data = json.loads(line)
                print("Starting for ID: ", data['id_str'])

                #Is tweet new
                if twitter_data.tweet_info.find_one({'id_str' : data['id_str']}):
                    print("Skipping tweet ", data['id_str'], " since already exists in DB")
                    continue

                user = data['user']

                #print("Starting user extract")
                #Extract User Info for DB
                user_id = user['id_str']
                id_set.add(user_id)
                name = user['name']
                #remove "'" from name since causes issues in mySQL insert
                name = re.sub("'", "", name)
                screen_name = user['screen_name']
                followers_count = user['followers_count']
                friends_count = user['friends_count']
                last_tweet = data['id_str']
                #print("Finished user extract")

                mysql_cursor.execute("SELECT * FROM user_info where user_id = %s", (user_id,))
                user_entry = mysql_cursor.fetchone()
                if not user_entry: #Entry not in table, need to add
                    #print("Insert new user ", screen_name)
                    insert_data = [user_id, name, screen_name, followers_count, friends_count, 1, last_tweet]
                    #print(insert_data)
                    insert_mysql(insert_data, mysql_connection, mysql_cursor, insert = True)
                    #print("User inserted")
                else: #User exists
                    print("Update user ", screen_name)
                    num_tweets = user_entry[5] + 1
                    print("Number of tweets:",num_tweets)
                    if data['id_str'] > user_entry[6]: #More recent tweet, so check that other info is up to date
                        print("More recent tweet")
                        print("User ID: ", user_id)
                        print("name: ", name)
                        print("screen_name: ", screen_name)
                        print("followers_count: ", followers_count)
                        print("friends_count: ", friends_count)
                        print("num_tweets: ", num_tweets)
                        print("last tweet: ", last_tweet)
                        update_data = [user_id, name, screen_name, followers_count, friends_count, num_tweets, last_tweet]
                        print(update_data)
                        insert_mysql(update_data, mysql_connection, mysql_cursor, insert = False)
                    else: #Less recent tweet, update num tweets only
                        print("Less recent tweet")
                        update_data = [user_id, user_entry[1], user_entry[2], user_entry[3], user_entry[4], num_tweets, user_entry[6]]
                        print(update_data)
                        insert_mysql(update_data, mysql_connection, mysql_cursor, insert = False)
                    #print("User updated")

                #print("Compiling tweet info")
                hashtags = []
                is_retweet = False
                text = data['text']
                for hashtag in data['entities']['hashtags']:
                    hashtags.append(hashtag['text'])
                retweet_hashtags = None
                retweet_text = None
                #print("Checking if retweet")
                if (data['text'].startswith('RT')):
                    #print(data['id_str'], "is retweet")
                    is_retweet = True
                    try:
                        retweet_hashtags = []
                        for hashtag in data['retweeted_status']['entities']['hashtags']:
                            retweet_hashtags.append(hashtag['text'])
                            retweet_text = data['retweeted_status']['text']
                    except:
                        #print("No retweeted_status")
                        retweet_hashtags = None
                        retweet_text = None
                #print("Making tweet document for storage")
                tweet = {
                    "tweet_id": data['id_str'],
                    "tweeted_date": convert_time_created(data['created_at']),
                    "user_id": user_id,
                    "favorite_count": data['favorite_count'],
                    "retweet_count": data['retweet_count'],
                    "is_retweet": is_retweet,
                    "orig_hashtags": hashtags,
                    "rt_hashtags": retweet_hashtags,
                    "orig_text": text,
                    "rt_text": retweet_text
                }
                #print("Tweet setup, ready to insert")
                insert_mongo(tweet, twitter_data)
                print("Finished for ID: ", data['id_str'])
            except Exception as e:
                #print(e)
                #print("Hit exception for ID: ", data['id_str'])
                #break
                continue