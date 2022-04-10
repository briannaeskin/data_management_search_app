"""
Author: Brianna Eskin
Function: Write data to MySQL and MongoDB datastores
"""

import json
import mysql.connector as connection

if __name__ == "__main__":
    mysql_connection = connection.connect(host="localhost", user="data_man_group3", passwd="abc123",
                                          database="twitter_users")
    mycursor = mysql_connection.cursor(prepared = True)

    user_check_query = """SELECT * FROM user_info where id = %s"""
    user_insert_query = """INSERT INTO user_info (id, name, screen_name, followers_count, friends_count, 
                        num_tweets, num_times_retweet, last_tweet) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    user_update_query = """UPDATE user_info SET name = %s, screen_name = %s, followers_count = %s, friends_count = %s,
                        num_tweets = %s, num_times_retweet = %s, last_tweet = %s WHERE id = %s, """
    user_update_query_2 = """"UPDATE user_info SET num_tweets = %s, num_times_retweet = %s WHERE id = %s"""

    id_set = set()

    with open("corona-out-2.json", "r") as f1:
        for line in f1:
            try:
                data = json.loads(line)
                # pseudocode:
                # if tweet has been seen before,
                #         continue (ignore this tweet, go to next iteration of loop)

                user = data['user']

                #Extract info for DB
                user_id = user['id_str']
                id_set.add(user_id)
                name = user['name']
                screen_name = user['screen_name']
                followers_count = user['followers_count']
                friends_count = user['friends_count']
                num_retweets = data['retweet_count']
                last_tweet = data['id_str']

                check_tuple = (user_id,)

                mycursor.execute(user_check_query, check_tuple)
                user_entry = mycursor.fetchone()
                if not user_entry: #Entry not in table, need to add
                    print("Adding new user ", user_id)
                    insert_tuple = (user_id, name, screen_name, followers_count, friends_count, 1,
                                    num_retweets, last_tweet)
                    mycursor.execute(user_insert_query, insert_tuple)
                    mysql_connection.commit()
                    print("Successfully added new user ", user_id)
                else: #User exists
                    print("Updating user ", user_id)
                    num_tweets = user_entry[5] + 1
                    num_retweets = user_entry[6] + num_retweets
                    if data['id_str'] > user_entry[7]: #More recent tweet, so check that other info is up to date
                        update_tuple = (name, screen_name, followers_count, friends_count, num_tweets, num_retweets,
                                        last_tweet, user_id)
                        mycursor.execute(user_update_query, update_tuple)
                        mysql_connection.commit()
                        print("Successfully updated user ", user_id)
                    else: #Less recent tweet, update num tweets and retweets only
                        update_tuple = (num_tweets, num_retweets, user_id)
                        mycursor.execute(user_update_query_2, update_tuple)
                        mysql_connection.commit()
                        print("Successfully updated user ", user_id)

                if (data['text'].startswith('RT')):
                    # psuedocode:
                    # update retweet information
                    # note that you may not have an entry for the original tweet
                    # if that is not in the dataset
                    pass  # does nothing right now

                else:
                    # psuedocode:
                    # add the new tweet to datastore
                    pass  # does nothing right now
            except:
                continue
    print("Number of user id: ", len(id_set))