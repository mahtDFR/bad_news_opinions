import tweepy

import keys

# authorize using api keys (contained in separate 'keys' file)
auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(auth)  # create variable containing authorized data for ease

# scrape data from 'anon_opin' twitter account
data = api.user_timeline(screen_name="anon_opin", tweet_mode='extended', count=3000)

# initiate a list to store tweets
tweets = []

# weed out tweets we're not interested in, and clean up grammar for ones we are.
for i in data:  # iterate through the source data
	tweet = i.full_text  # get the full text of the tweet, not the truncated version
	if not "https://t.co/" in tweet:  # filter out tweets containing urls
		if not "@" in tweet:  # filter tweets containing RTs
			if not "&gt;" in tweet:  # filter '>' because this symbol doesn't play nice right now...
				if not len(tweet) > 125:  # filter out any tweets greater than x chars
					if not tweet.endswith("."):  # if the tweet text doesn't end with "."
						if not tweet.endswith("!"):  # and if it doesn't end with "!"
							tweet = tweet + "."  # add "." to the end
							tweets.append(tweet)  # and then add the processed entry to the list
					else:
						tweets.append(tweet)  # otherwise, just add it to the list as it is

# (after writing this bit i realized the guardian website avoids periods
# at the end of bylines - but whatever i'm leaving it in because i think it looks better).

# # iterate through the resulting list
# for i in tweets:
# 	print(i + "\n") # print each entry with a line break
# print("*** " + str(len(tweets)) + " tweets scraped ***") # print the amount of entries in the list for reference
