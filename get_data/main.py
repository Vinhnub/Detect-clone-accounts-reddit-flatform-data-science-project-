from reddit_crawler import RedditCrawler
from database_fetcher import DatabaseFetcher

oBot = RedditCrawler()
oData = DatabaseFetcher()
oBot.fetch_user(1000)