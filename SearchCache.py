# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 19:31:39 2022

@author: Michael Gleyzer
"""

from datetime import datetime, timezone   
from collections import OrderedDict

class Cache: 
    
    def __init__(self, size: int):
        self.cache = OrderedDict()
        self.size = size
    
    # In the retrieve method, we retrieve the desired search query by
    # moving the corresponding {key : value} pair to the end of the dictionary, and returning the value,
    # which are the query results
    def retrieve(self, key: tuple) :
      if key not in self.cache:
            return None 
      else:
            self.cache.move_to_end(key)  
            return self.cache[key] 
 
    
    #The key will be a tuple in the form of (string query , string lowtime-hightime or date string) and the corresponding value 
    # will be the result of the search query.  
    
    #In the store method we store the {key:value} pair at the end of the cache, if there is enough space.
    # If there isn't enough space, then we remove the first item from the cache, 
    # which is the least recently used item or the oldest item in the cache
    
    
    def store(self,key,value) : 
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.size:
            self.cache.popitem(last = False) 
            
if __name__ == "__main__" : 
    cache = Cache(2)
    result = """
    Result for hashtag: {5}
    
    Number of Tweets: 4
    Number of Retweets: {3}
    
    Most Popular Tweets: {2}
    
    """
    
    result2 = """
    Result for hashtag: {6}
    
    Number of Tweets: 4
    Number of Retweets: {3}
    
    Most Popular Tweets: {2}
    
    """
    
    result3 = """
    Result for hashtag: {7}
    
    Number of Tweets: 4
    Number of Retweets: {3}
    
    Most Popular Tweets: {2}
    
    """
    cache.put(('Turkeys' , '5.0-10.0') ,  result)
    cache.put(('Turkeys' , '6.0-10.0') ,  result2)
    cache.put(('Turkeys' , '7.0-10.0') ,  result3)
    print(cache.get(('Turkeys' , '6.0-10.0'))) 
    