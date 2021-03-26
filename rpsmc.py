from finviz.screener import Screener
from psaw import PushshiftAPI
import datetime as dt

api = PushshiftAPI()


filters = ['sh_price_u1']  # Filters stocks to be under $2
stock_list = Screener(filters=filters, table='Performance', order='price')  # Get the performance table and sort it by price ascending


penny_stocks = []
for stock in stock_list:
    penny_stocks.append(stock['Ticker'])


start_epoch=int(dt.datetime(2020, 3, 25).timestamp())

posts = api.search_submissions(after=start_epoch,
                            subreddit='pennystocks',
                            filter=['url','author', 'title', 'subreddit'],)

mentions = {}

for post in posts:
    words = post.title.split()
    for word in words:
        if word in penny_stocks:
            if word in mentions:
                mentions[word] += 1
            else:
                mentions[word] = 1           

print(mentions)



