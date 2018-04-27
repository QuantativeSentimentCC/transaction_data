import twitter
import json
from pymongo import MongoClient;
import hashlib;
import time;
import html



def getTimestamp(create):
	ts = str(int(time.strftime('%s', time.strptime(create,'%a %b %d %H:%M:%S +0000 %Y'))));
	return ts;



def search_twitter():
	client  = MongoClient('localhost',27017);
	db = client['cs5412'];
	news_data = db['news_data'];


	api = twitter.Api(consumer_key = "HQIo5JvUjEVgqXOAzoK0vgjg8",
	                 consumer_secret="vCQTglUJzyTmmIVF4i0IlX5a8Vfi3FIoxsX38rSnVHO5iGBOhT",
	                  access_token_key="875584099808759808-ppXVjLfAHBATvGqlGqEqeZfGLNROYR3",
	                  access_token_secret="8PajfI8d0kR65avqhcncsfL8N6VmpuH4awi2LpXgKVQNE")
	# using MD5 value to get rid of same message
	while(1):
		count = 0;
		md5Set = set();
		while (count <= 1000):
			count += 1;
			try:
				result = api.GetSearch(raw_query= "result_type=recent&count=100&q=bitcoin&lang=en&include_entities=true");
				if result is None or len(result) == 0:
					continue;
				res_list = []
				for r in result:
					m = hashlib.md5();
					m.update(r.text.encode('utf-8'));
					MD5value = m.digest();
					if MD5value not in md5Set:
						tweet = {};
						tweet["source"] = "twitter";
						tweet["text"] = html.unescape(r.text);
						print(tweet["text"]);
						time_01 = getTimestamp(r.created_at);
						tweet["title"] = "Twitter Post";
						tweet["time"] = time_01;
						tweet["weight"] = r.favorite_count + r.retweet_count;
						md5Set.add(MD5value);
						if '\u2026' not in tweet["text"]:
							res_list.append(tweet);

				if len(res_list) != 0:
					result = news_data.insert_many(res_list);
					print(result);
				time.sleep(10);
			except:
				print("unexpected failure");



if __name__ == '__main__':
	search_twitter();
