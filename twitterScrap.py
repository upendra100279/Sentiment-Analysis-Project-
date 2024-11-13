import time
import asyncio  # New import for async functionality
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import logging
from twikit import Client, TooManyRequests

MINIMUM_TWEETS = 100
QUERY = 'Virat Kohli'

# * logging configuration
logging.basicConfig(filename='tweet_scrape.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# * Asynchronous function to get tweets
async def get_tweets(tweets):
    if tweets is None:
        logging.info('Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        logging.info(f'Getting next tweets after {wait_time} seconds...')
        await asyncio.sleep(wait_time)  # Use await asyncio.sleep for async sleep
        tweets = await tweets.next()

    return tweets

# * login credentials
config = ConfigParser()
config.read('pass.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

# * authenticate to X.com
client = Client(language='en-US')
client.load_cookies('cookies_cleaned.json')

tweet_count = 0
tweets = None
batch_size = 20  # Set batch size for writing tweets in chunks

# * Main asynchronous function to run the scraping process
async def main():
    global tweet_count, tweets  # Use global to update tweet_count and tweets variables
    # * create a csv file and open it once for writing
    with open('C:\\Users\\upend\\Downloads\\tempCSV.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])

        while tweet_count < MINIMUM_TWEETS:
            try:
                tweets = await get_tweets(tweets)
            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
                logging.warning(f'Rate limit reached. Waiting until {rate_limit_reset}')
                wait_time = (rate_limit_reset - datetime.now()).total_seconds()
                await asyncio.sleep(max(0, wait_time))  # Async sleep until rate limit reset
                continue

            if not tweets:
                logging.info('No more tweets found.')
                break

            tweet_batch = []
            for tweet in tweets:
                tweet_count += 1
                tweet_data = [
                    tweet_count,
                    tweet.user.name,
                    tweet.text,
                    tweet.created_at,
                    tweet.retweet_count,
                    tweet.favorite_count
                ]
                tweet_batch.append(tweet_data)

                if len(tweet_batch) >= batch_size:
                    writer.writerows(tweet_batch)
                    tweet_batch.clear()  # Clear batch after writing to file

            # Write any remaining tweets in the batch
            if tweet_batch:
                writer.writerows(tweet_batch)

            logging.info(f'Got {tweet_count} tweets')

    logging.info(f'Done! Total {tweet_count} tweets retrieved.')

# Run the main function
asyncio.run(main())
