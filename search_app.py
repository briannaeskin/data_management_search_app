"""
Author: Brianna Eskin
Function: Holds the search app, including the GUI
"""

from pymongo import MongoClient
from datetime import datetime
import mysql.connector as connection
import time

class Search:

    def __init__(self):
        """
        Initialize the search object by connecting to mySQL, MongoDB, and Redis
        """

        #MySQL Connection
        self.mysql_connection = connection.connect(host="localhost", user="data_man_group3", passwd="abc123",
                                              database="twitter_users")
        self.mysql_connection.autocommit = True
        self.cursor = self.mysql_connection.cursor(prepared=True)

        #MongoDB Connection
        self.client = MongoClient("mongodb+srv://data_man_group3:dkncO5uFyOd6IB5Y@cluster0.na33p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        self.twitter_data = self.client["twitter_data"]
        self.tweet_info_collection = self.twitter_data["tweet_info"]

        #Placeholder for Redis store

    def search_by_text(self, text, timerange_lower=None, timerange_upper=None):
        """
        Given a text, searches for relevant tweets with given text. Reports how many tweets contain the text, how many
        retweets contain the text, the most popular tweets
        """

        start_time = time.time()
        redis_enabled = False #Temp vairable since no cache is set up yet. Will remove this and all reference once set up

        if redis_enabled:
            cache_status = "Found in cache"
            pass

        else:
            cache_status = "Not Found in cache. Data pulled from Mongo and mySQL"

            timerange_lower = timerange_lower if timerange_lower else datetime.strptime('1/1/2000', '%m/%d/%Y')
            timerange_upper = timerange_upper if timerange_upper else datetime.strptime('12/31/9999', '%m/%d/%Y')

            query = {
                "$or": [
                    {'orig_text': {'$regex': text, '$options': 'i'}},
                    {'rt_text': {'$regex': text,'$options': 'i'}}
                ],
                'tweeted_date': {'$gte': timerange_lower, '$lt': timerange_upper}
            }

            tweets_query = self.tweet_info_collection.find(query).sort('total_engagement', -1)

            num_tweets = 0
            num_retweets = 0
            popular_tweets = ""

            for tweet in tweets_query:
                if not tweet['is_retweet']:
                    num_tweets += 1
                    if num_tweets <= 10:
                        popular_tweets += str(tweet) + '\n'
                else:
                    num_retweets += 1

            end_time = time.time()
            query_runtime = end_time - start_time

            query_runtime_ms = query_runtime * 1000
            runtime = "Results returned in: {} ms".format(query_runtime_ms)

            result = """
            Result for text: {}

            Number of Tweets: {}
            Number of Retweets: {}

            Most Popular Tweets: 
            {}

            """.format(text, num_tweets, num_retweets, popular_tweets)

            # Add to Redis cache

            return cache_status + '\n' + runtime + '\n' + result


    def search_by_hashtag(self, hashtag, timerange_lower=None, timerange_upper=None):
        """
        Given a hashtag, searches for relevant tweets with given hashtag. Reports how many tweets use that hashtag, how
        many retweets use that hashtag, the most popular tweets
        """

        start_time = time.time()
        redis_enabled = False #Temp variable since no cache is set up yet. Will remove this and all reference once set up

        if redis_enabled:
            cache_status = "Found in cache"
            pass

        else:
            cache_status = "Not Found in cache. Data pulled from Mongo and mySQL"

            timerange_lower = timerange_lower if timerange_lower else datetime.strptime('1/1/2000', '%m/%d/%Y')
            timerange_upper = timerange_upper if timerange_upper else datetime.strptime('12/31/9999', '%m/%d/%Y')

            query = {
                "$or": [
                    {'orig_hashtags': {'$elemMatch': {'$regex': hashtag, '$options': 'i'}}},
                    {'rt_hashtags': {'$elemMatch': {'$regex': hashtag,'$options': 'i'}}}
                ],
                'tweeted_date': {'$gte': timerange_lower, '$lt': timerange_upper}
            }

            tweets_query = self.tweet_info_collection.find(query).sort('total_engagement', -1)

            num_tweets = 0
            num_retweets = 0
            popular_tweets = ""

            for tweet in tweets_query:
                if not tweet['is_retweet']:
                    num_tweets += 1
                    if num_tweets <= 10:
                        popular_tweets += str(tweet) + '\n'
                else:
                    num_retweets += 1

            end_time = time.time()
            query_runtime = end_time - start_time

            query_runtime_ms = query_runtime * 1000
            runtime = "Results returned in: {} ms".format(query_runtime_ms)

            result = """
            Result for hashtag: {}
            
            Number of Tweets: {}
            Number of Retweets: {}
            
            Most Popular Tweets: 
            {}
            
            """.format(hashtag, num_tweets, num_retweets, popular_tweets)

            #Add to Redis cache

            return cache_status + '\n' + runtime + '\n' + result

    def search_by_user(self, user_name, timerange_lower=None, timerange_upper=None):
        """
        Given a user name, searches for relevant information about user, including name, screen_name, number of followers,
        number of friends, total number of tweets (including retweets), their most recent tweet (including retweets), and
        their 5 most popular tweets (or all tweets if user tweeted less than 5 times)
        """

        start_time = time.time()
        redis_enabled = False #Temp variable since no cache is set up yet. Will remove this and all reference once set up

        #Query user_id based on screen_name, required for Redis lookup, so needs to execute regardless
        self.cursor.execute("""SELECT * FROM user_info WHERE screen_name = '{}'""".format(user_name))
        user = self.cursor.fetchone()

        if not user:#No user found
            message = "No user found with provided user name {}".format(user_name)
            return message

        user_id = user[0]

        if redis_enabled:
            """
            This is the placeholder for the cache check. For now passing. But when ready for implementation will need to
            replace with check for redis key and fill in accordingly
            """
            cache_status = "Found in cache"
            pass
        else:
            cache_status = "Not Found in cache. Data pulled from Mongo and mySQL"
            user_name = user[1]
            screen_name = user[2]
            num_followers = user[3]
            num_friends = user[4]

            timerange_lower = timerange_lower if timerange_lower else datetime.strptime('1/1/2000', '%m/%d/%Y')
            timerange_upper = timerange_upper if timerange_upper else datetime.strptime('12/31/9999', '%m/%d/%Y')

            query = {'user_id': user_id, 'tweeted_date': {'$gte': timerange_lower, '$lt': timerange_upper}}

            tweets = self.tweet_info_collection.find(query).sort('total_engagement', -1)

            num_tweets = 0
            most_recent_tweet = None
            popular_tweets = ""

            for tweet in tweets:
                num_tweets += 1
                if num_tweets <= 5:
                    popular_tweets += str(tweet) + '\n'
                try:
                    if tweet['tweeted_date'] > most_recent_tweet['tweeted_date']:
                        most_recent_tweet = tweet
                except:
                    most_recent_tweet = tweet

            most_recent_tweet_str = str(most_recent_tweet)
            end_time = time.time()
            query_runtime = end_time - start_time

            query_runtime_ms = query_runtime*1000
            runtime = "Results returned in: {} ms".format(query_runtime_ms)

            result = """
            Result for user name: {}
        
            Name: {}
            Number of Followers: {}
            Number of Friends: {}
            Total Tweets (Including Retweets): {}
            Most Recent Tweet: 
            {}
        
            Top Tweets: 
            {}
            """.format(screen_name, user_name, num_followers, num_friends, num_tweets, most_recent_tweet_str, popular_tweets)

            #Add to Redis cache

            return cache_status + '\n' + runtime + '\n' + result

    def user_drilldown(self, tweet_id):
        query = {'tweet_id': tweet_id}
        tweet = self.tweet_info_collection.find_one(query)
        user_id = tweet['user_id']

        self.cursor.execute("""SELECT * FROM user_info WHERE user_id = '{}'""".format(user_id))
        user = self.cursor.fetchone()

        user_name = user[1]
        screen_name = user[2]
        num_followers = user[3]
        num_friends = user[4]

        query = {'user_id': user_id}
        tweets = self.tweet_info_collection.find(query).sort('total_engagement', -1)

        num_tweets = 0
        most_recent_tweet = None
        popular_tweets = ""

        for tweet in tweets:
            num_tweets += 1
            if num_tweets <= 5:
                popular_tweets += str(tweet) + '\n'
            try:
                if tweet['tweeted_date'] > most_recent_tweet['tweeted_date']:
                    most_recent_tweet = tweet
            except:
                most_recent_tweet = tweet

        most_recent_tweet_str = str(most_recent_tweet)

        result = """
        Result for user name: {}

        Name: {}
        Number of Followers: {}
        Number of Friends: {}
        Total Tweets (Including Retweets): {}
        Most Recent Tweet: 
        {}

        Top Tweets: 
        {}
        """.format(screen_name, user_name, num_followers, num_friends, num_tweets, most_recent_tweet_str,
                   popular_tweets)

        return result



if __name__ == "__main__":
    search = Search()
    #Test Queries
    #print(search.search_by_hashtag("coronavirus"))
    #print(search.search_by_hashtag("Drosten"))

    #print(search.search_by_text("Turkey", None,datetime.strptime('04/10/2020','%m/%d/%Y')))
    #print(search.search_by_text("Trump"))

    print(search.search_by_user("Turkey_Pics", None, datetime.strptime('04/4/2020','%m/%d/%Y')))
    #print(search.search_by_user("nuffsaidny"))

