from finviz.screener import Screener
from psaw import PushshiftAPI
import datetime as dt
import re

api = PushshiftAPI()


filters = ['sh_price_u5']  # Filters stocks to be under $5
stock_list = Screener(filters=filters, table='Performance', order='price')  # Get the performance table and sort it by price ascending


# Saves all filtered stocks under $5 into a list to verify if the ticker is legitimate 
penny_stocks = [] 
for stock in stock_list:
    penny_stocks.append(stock['Ticker'])

# Sets start time to look for post after a certain date
start_epoch=int(dt.datetime(2021, 3, 1).timestamp()) 


# psaw sub reddit filter
posts = api.search_submissions(after=start_epoch, 
                            subreddit='pennystocks',
                            filter=['url','author', 'title', 'subreddit'],)


""" 
Iterates through all the posts, splits non alphabetic characters and appends
any tickers that matches anything from the penny_stocks list above then adds up the value by 1 every time it has been mentioned
"""

mentions = {} 
for post in posts:
    words = re.split('[^a-zA-Z]', post.title)
    for word in words:
        if word in penny_stocks:
            if word in mentions:
                mentions[word] += 1
            else:
                mentions[word] = 1

# Sorts the mentions dictionary by the value from highest number to lowest
mentions_sorted = sorted(mentions.items(), key=lambda x: x[1], reverse=True) #

#print the tickers and mentions
for key, value in mentions_sorted:
    print(key, value)


