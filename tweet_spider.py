import twitter
import json
from pymongo import MongoClient;
import hashlib;
import time;
import html
import re;
import socket;


#UDP_IP = "34.218.214.180";
UDP_IP = "34.208.32.187";
#UDP_IP = "127.0.0.1";
UDP_PORT = 5005;
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM);


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
						raw_text = html.unescape(r.text);
						new_text = raw_text;
						for i in range(len(raw_text) - 5):
							if raw_text[i:i+5] == "https":
								j = i;
								while j < len(raw_text) and raw_text[j] != " ":
									j += 1;
								new_text = raw_text[0:i] + raw_text[j:];
								break;
						nnew_text = new_text;
						for i in range(len(new_text) - 5):
							if new_text[i:i+5] == "https":
								j = i;
								while j < len(new_text) and new_text[j] != " ":
									j += 1;
								nnew_text = new_text[0:i] + new_text[j:];
								break;
						tweet["text"] = nnew_text;
						print(tweet["text"]);
						time_01 = getTimestamp(r.created_at);
						tweet["title"] = "Twitter Post";
						tweet["time"] = time_01;
						tweet["weight"] = r.favorite_count + r.retweet_count;
						md5Set.add(MD5value);
						if '\u2026' not in tweet["text"]:
							res_list.append(tweet);

				if len(res_list) != 0:
					sock.sendto(json.dumps(res_list).encode('utf-8'),(UDP_IP,UDP_PORT));
					result = news_data.insert_many(res_list);
					print(result);
				time.sleep(10);
			except:
				print("unexpected failure");



if __name__ == '__main__':
	search_twitter();
