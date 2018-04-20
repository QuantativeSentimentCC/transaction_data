import requests;
import time;
import json;
from pymongo import MongoClient;


def getPrice():
	client  = MongoClient('localhost',27017);
	db = client['cs5412'];
	price_data = db['price_data'];

	while (1):

		cur1 = "BTC";
		cur2 = "USD";
		url = "https://cex.io/api/last_price/" + cur1 + "/" + cur2;
		response = requests.get(url);
		if response is not None and response.status_code == 200:
			content = response.json();
			data = {}
			data['id'] = '1';
			data['price'] = content['lprice'];
			data['timestamp'] = int(time.time());
			data['exchange'] = 'cex';
			price_data.insert_one(data);
			print(data);
		time.sleep(30);









if __name__ == '__main__':
	getPrice();