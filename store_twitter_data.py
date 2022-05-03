"""
Author: Brianna Eskin
Function: Write data to MySQL and MongoDB datastores. Note, need to change file name accordingly, and make sure file is
in same path as this file. Due to size, file couldn't be loaded to GitHub
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
    last_tweet_id VARCHAR(255),
    PRIMARY KEY(user_id),
    INDEX(screen_name, followers_count)
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
    twitter_data.tweet_info.create_index("total_engagement")

def insert_mysql(data, connection, cursor, insert):
    """
    Update mySQL database. Can either insert (if new entry), or update (if user already exists)
    """
    INSERT_QUERY = """
    INSERT INTO user_info (
    user_id, name, screen_name, followers_count, friends_count, last_tweet_id
    )
    VALUES (
    '{}','{}','{}',{},{},'{}'
    );
    """.format(data[0], data[1], data[2], data[3], data[4], data[5])

    UPDATE_QUERY = """
    UPDATE user_info SET name = '{}', screen_name = '{}', followers_count = {}, friends_count = {},
    last_tweet_id = '{}' WHERE user_id = '{}';
    """.format(data[1], data[2], data[3], data[4], data[5], data[0])

    if insert:
        cursor.execute(INSERT_QUERY)
        print("User ", data[2], "inserted")
    else:
        cursor.execute(UPDATE_QUERY)
        connection.commit()
        print("User", data[2], "updated")

def insert_mongo(data, twitter_data):
    """
    Insert document to MongoDB. Already know this is new since we check if exists in main method
    """
    twitter_data.tweet_info.insert_one(data)
    print("Tweet inserted")

def update_mongo(twitter_data, id_str, favorite_count, retweet_count, total_engagement):
    myquery = {"tweet_id": id_str}
    newvalues = {"$set": {
        "favorite_count": favorite_count,
        "retweet_count": retweet_count,
        "total_engagement": total_engagement
    }}
    twitter_data.tweet_info.update_one(myquery, newvalues)
    print("Tweet updated in Mongo")

def convert_time_created(created_at):
    """
    Convert created_at string to datetime that can be used for search purposes
    """
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

    new_date = datetime(year = int(year), month = month, day = int(day), hour = int(hour), minute = int(min),
                        second = int(sec), tzinfo = timezone.utc)
    return new_date

def is_tweet_new(id_str, twitter_data):
    doc = twitter_data.tweet_info.find_one({'tweet_id': id_str})
    if doc:
        return False
    else:
        return True

def gather_user_info(user, data, id_set):
    user_id = user['id_str']
    id_set.add(user_id)
    name = user['name']
    # remove "'" from name since causes issues in mySQL insert
    name = re.sub("'", "", name)
    screen_name = user['screen_name']
    followers_count = user['followers_count']
    friends_count = user['friends_count']
    last_tweet = data['id_str']
    return user_id, name, screen_name, followers_count, friends_count, last_tweet, id_set

def gather_tweet_info(data):
    hashtags = []
    is_retweet = False

    try:
        text = data['extended_tweet']['full_text']
    except:
        text = data['text']

    favorite_count = data['favorite_count'] if data['favorite_count'] else 0
    retweet_count = data['retweet_count'] if data['retweet_count'] else 0
    total_engagement = favorite_count + retweet_count

    try:
        for hashtag in data['extended_tweet']['entities']['hashtags']:
            hashtags.append(hashtag['text'])
    except:
        for hashtag in data['entities']['hashtags']:
            hashtags.append(hashtag['text'])

    retweet_hashtags = None
    retweet_text = None
    retweet_id = None
    return hashtags, is_retweet, text, favorite_count, retweet_count, total_engagement, retweet_hashtags, retweet_text, retweet_id

def gather_retweet_info(data):
    is_retweet = True
    retweet_hashtags = []

    try:
        for hashtag in data['extended_tweet']['entities']['hashtags']:
            retweet_hashtags.append(hashtag['text'])
    except:
        for hashtag in data['entities']['hashtags']:
            retweet_hashtags.append(hashtag['text'])

    try:
        retweet_text = data['extended_tweet']['full_text']
    except:
        retweet_text = data['text']

    retweet_id = data['id_str']
    return is_retweet, retweet_hashtags, retweet_text, retweet_id

if __name__ == "__main__":
    mysql_connection, mysql_cursor = setup_mysql()
    twitter_data = setup_mongo()

    id_set = set()
    tweet_id_set = set()

    with open("corona-out-3.JSON", "r") as f1:
        for line in f1:
            try:
                data = json.loads(line)
                print("Starting for ID: ", data['id_str'])
                tweet_id_set.add(data['id_str'])

                #Is tweet new
                if not is_tweet_new(data['id_str'], twitter_data):
                    print("Skipping tweet", data['id_str'], "since it already exists in DB")
                    continue

                #print("Starting user checks")

                user = data['user']

                user_id, name, screen_name, followers_count, friends_count, last_tweet, id_set = gather_user_info(user, data, id_set)

                mysql_cursor.execute("SELECT * FROM user_info where user_id = %s", (user_id,))
                user_entry = mysql_cursor.fetchone()
                if not user_entry: #Entry not in table, need to add
                    print("Insert new user", screen_name)
                    insert_data = [user_id, name, screen_name, followers_count, friends_count, last_tweet]
                    insert_mysql(insert_data, mysql_connection, mysql_cursor, insert = True)
                else: #User exists
                    #print("Last Tweet: ", user_entry[5])
                    if data['id_str'] > user_entry[5]: #More recent tweet, so check that other info is up to date
                        print("Update user", screen_name)
                        update_data = [user_id, name, screen_name, followers_count, friends_count, last_tweet]
                        insert_mysql(update_data, mysql_connection, mysql_cursor, insert = False)
                    else:
                        print("Tweet more recent, skipping update for user ", screen_name)

                #print("Start compiling tweet info")

                hashtags, is_retweet, text, favorite_count, retweet_count, total_engagement, retweet_hashtags, retweet_text, retweet_id = gather_tweet_info(data)

                if data['text'].startswith('RT'):
                    print("Tweet", data['id_str'], "is retweet")
                    try:
                        retweet_data = data['retweeted_status']
                        is_retweet, retweet_hashtags, retweet_text, retweet_id = gather_retweet_info(retweet_data)
                    except:
                        #print("No retweeted status")
                        is_retweet = True
                        retweet_hashtags = None
                        retweet_text = None
                        retweet_id = None


                tweet = {
                    "tweet_id": data['id_str'],
                    "tweeted_date": convert_time_created(data['created_at']),
                    "user_id": user_id,
                    "favorite_count": favorite_count,
                    "retweet_count": retweet_count,
                    "total_engagement": total_engagement,
                    "is_retweet": is_retweet,
                    "orig_hashtags": hashtags,
                    "rt_hashtags": retweet_hashtags,
                    "orig_text": text,
                    "rt_text": retweet_text,
                    "rt_id": retweet_id
                }


                insert_mongo(tweet, twitter_data)

                if data['text'].startswith('RT'):
                    print("Need to write retweeted tweet to database")
                    #print("Original tweet ID:", retweet_data['id_str'])
                    tweet_id_set.add(retweet_data['id_str'])

                    if is_tweet_new(retweet_data['id_str'], twitter_data):
                        print("Original tweet", retweet_data['id_str'], "is new")
                        is_orig_tweet_new = True
                    else:
                        print("Original tweet is already in DB")
                        is_orig_tweet_new = False

                    #print("Starting original tweet user checks")

                    orig_user = retweet_data['user']

                    orig_user_id, orig_name, orig_screen_name, orig_followers_count, orig_friends_count, orig_last_tweet, id_set = gather_user_info(orig_user, data, id_set)

                    mysql_cursor.execute("SELECT * FROM user_info where user_id = %s", (orig_user_id,))
                    orig_user_entry = mysql_cursor.fetchone()
                    if not orig_user_entry: #Entry not in table, need to add
                        print("Insert new original user", orig_screen_name)
                        insert_orig_data = [orig_user_id, orig_name, orig_screen_name, orig_followers_count, orig_friends_count, last_tweet]
                        insert_mysql(insert_orig_data, mysql_connection, mysql_cursor, insert = True)
                    else: #Original User Exists
                        #print("Last tweet:", orig_user_entry[5])
                        if last_tweet > orig_user_entry[5]: #More recent tweet, so check that other info is up to date
                            print("Update original user", screen_name)
                            orig_update_data = [orig_user_id, orig_name, orig_screen_name, orig_followers_count, orig_friends_count, last_tweet]
                            insert_mysql(orig_update_data, mysql_connection, mysql_cursor, insert = False)
                        else:
                            print("More recent tweet, skipping update")

                    orig_hashtags, orig_is_retweet, orig_text, orig_favorite_count, orig_retweet_count, orig_total_engagement, orig_retweet_hashtags, orig_retweet_text, orig_retweet_id = gather_tweet_info(retweet_data)

                    retweet = {
                        "tweet_id": retweet_data['id_str'],
                        "tweeted_date": convert_time_created(retweet_data['created_at']),
                        "user_id": orig_user_id,
                        "favorite_count": orig_favorite_count,
                        "retweet_count": orig_retweet_count,
                        "total_engagement": orig_total_engagement,
                        "is_retweet": orig_is_retweet,
                        "orig_hashtags": orig_hashtags,
                        "rt_hashtags": orig_retweet_hashtags,
                        "orig_text": orig_text,
                        "rt_text": orig_retweet_text,
                        "rt_id": orig_retweet_id
                    }

                    if is_orig_tweet_new:
                        print("Original tweet is new, so inserting")
                        insert_mongo(retweet, twitter_data)

                    else:
                        print("Tweet already exists, so updating")
                        update_mongo(twitter_data, retweet_data['id_str'], orig_favorite_count, orig_retweet_count, orig_total_engagement)

                print("Finished for ID: ", data['id_str'])

            except Exception as e:
                print(e)
                print("Hit exception for ID", data['id_str'])
                break
                #continue

    #Create Indexes
    mongo_indexes(twitter_data)

    #Checks
    print("ID Set Size:", len(id_set))
    print("Tweet ID Set Size:", len(tweet_id_set))

    #Close DB
    mysql_cursor.close()
    mysql_connection.close()

