import requests;
import time;
import json;


def getPrice():
	while (1):

		cur1 = "BTC";
		cur2 = "USD";
		url = "https://cex.io/api/last_price/" + cur1 + "/" + cur2;
		response = requests.get(url);
		content = response.json();
		data = {}
		data['id'] = '1';
		data['price'] = content['lprice'];
		data['timestamp'] = int(time.time());
		data['exchange'] = 'cex';
		json_data = json.dumps(data);
		print(json_data);
		time.sleep(30);








if __name__ == '__main__':
	getPrice();