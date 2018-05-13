import requests;
import time;
import json;
from pymongo import MongoClient;
import socket;

#UDP_IP = "34.218.214.180";
UDP_IP = "34.208.32.187";
#UDP_IP = "127.0.0.1";
UDP_PORT = 5004;
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM);

def getPrice():
	client  = MongoClient('localhost',27017);
	db = client['cs5412'];
	price_data = db['price_data'];

	while (1):
		try:
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
				print("I am ready to send data");
				sock.sendto(json.dumps(data).encode('utf-8'),(UDP_IP,UDP_PORT));
				price_data.insert_one(data);
				print(data);
		except:
			print("a nobody care fail happen")
		time.sleep(30);









if __name__ == '__main__':
	getPrice();
