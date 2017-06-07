import twitter
import csv
import os
consumer_key="yh10KkaZmuWZ1GdXVP1SvqiyK"
consumer_secret="WB6qemh6UW4uPgdOKpOaN27ZyQfTXc9L9VFwH74lDuydCExi1R"
access_token_key="2387291089-KrXUNlvBaKfdYGz8PpcS4EKuIbLtHfs4w0uuH81"
access_token_secret="fhaZSX3QFbGdth993aXPW1iQkgSOz5GJH6kJpcqERFDgC"
utenti_file = "utenti.txt"
tweet_file = "tweet.csv"
max_tweet = 200
api = twitter.Api(consumer_key=consumer_key,\
		 consumer_secret=consumer_secret,\
		 access_token_key=access_token_key,\
		 access_token_secret=access_token_secret) 

if not os.path.exists(tweet_file):
	with open(tweet_file, "w") as tww:
		tww.write("user,id,timestamp,text\n")
with open(utenti_file) as uf, open(tweet_file, "r") as twr, open(tweet_file, "a") as twa:
	csv_reader = csv.DictReader(twr)
	csv_writer = csv.DictWriter(twa, csv_reader.fieldnames)
	user_past_tweets = [x for x in csv_reader]
	users_stalked = [x.strip() for x in uf.readlines()]
	last_id = {x:0 for x in users_stalked}
	for upt in user_past_tweets:
		if int(upt["id"]) > last_id[upt["user"]]:
			last_id[upt["user"]] = int(upt["id"])
	
	for row in users_stalked:
		tweet_fetched = []
		raw_data = api.GetUserTimeline(screen_name=row, count=max_tweet,\
				since_id=last_id[row])
		for r in raw_data:
			tmp = {}		
			tmp["id"] = r.id
			tmp["timestamp"] = r.created_at_in_seconds
			tmp["text"] = r.text
			tmp["user"] = str(row)
			csv_writer.writerow(tmp)



		
	
