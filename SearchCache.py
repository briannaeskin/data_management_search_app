# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 19:31:39 2022

@author: Michael Gleyzer
"""
import pandas as pd 
import json  
from datetime import datetime, timezone   
from collections import OrderedDict

class Cache: 
    
    def __init__(self, size: int):
        self.cache = OrderedDict()
        self.size = size
        
    def get(self, key: tuple) :
      if key not in self.cache:
            return -1  
      else:
            self.cache.move_to_end(key)  
            return self.cache[key]
 
    # first, we add / update the key by conventional methods.
    # And also move the key to the end to show that it was recently used.
    # But here we will also check whether the length of our
    # ordered dictionary has exceeded our capacity,
    # If so we remove the first key (least recently used)
    
    # Modify by making the key to be (string hastag , string lowtime-hightime) and value be 
    # the results you would like from the search query as written in the "search app"
    def put(self, key, value) :
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
    