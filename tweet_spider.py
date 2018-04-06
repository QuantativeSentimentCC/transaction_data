import twitter
import json

def search_twitter():
	api = twitter.Api(consumer_key = "HQIo5JvUjEVgqXOAzoK0vgjg8",
	                 consumer_secret="vCQTglUJzyTmmIVF4i0IlX5a8Vfi3FIoxsX38rSnVHO5iGBOhT",
	                  access_token_key="875584099808759808-ppXVjLfAHBATvGqlGqEqeZfGLNROYR3",
	                  access_token_secret="8PajfI8d0kR65avqhcncsfL8N6VmpuH4awi2LpXgKVQNE")

	result = api.GetSearch(raw_query= "result_type=recent&count=100&q=bitcoin&lang=en&include_entities=true");
	res_list = []
	for r in result:
		tweet = {};
		tweet["text"] = r.text;
		tweet["time"] = r.created_at;
		tweet["weight"] = r.favorite_count + r.retweet_count;
		res_list.append(tweet);
	for res in res_list:
		print(res);


if __name__ == '__main__':
	search_twitter();
