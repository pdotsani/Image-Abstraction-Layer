#!image-abstraction/bin/python
import os
import datetime
import requests
import json
from flask import Flask, jsonify
from flask_pymongo import PyMongo

try:
	import CONFIG_FILE
except:
	print "No local config file!"

app = Flask(__name__)
mongo = PyMongo(app)

try:
	app.config['MONGO_URI'] =	os.environ['MONGODB_URI']
	app.config['MONGO_USERNAME'] = os.environ['MONGODB_USER']
	app.config['MONGO_PASSWORD'] = os.environ['MONGODB_PASS']
except:
	app.config['MONGO_URI'] = 'mongodb://localhost:27017/app'

try:
	GOOGLE_AUTH_KEY = os.environ['GOOGLE_AUTH']
except:
	GOOGLE_AUTH_KEY = CONFIG_FILE.GOOGLE_AUTH

try:
	GOOGLE_SEARCH_ENGINE = os.environ['GOOGLE_SEARCH_ENGINE']
except:
	GOOGLE_SEARCH_ENGINE = CONFIG_FILE.GOOGLE_SEARCH_ENGINE

GOOGLE_CUSTOM_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

def makeDict(item):
	return {
		'title': item['title'],
		'html': item['htmlSnippet'],
		'link': item['link'],
		'thumb': item['image']['thumbnailLink']
	}

def makeTimeStamp(item):
	return {
		'time': item['time'],
		'query': item['query'] 
	}

@app.route('/imagesearch/<query>', methods=['GET'])
def image_search(query):
	timestamp = datetime.datetime.utcnow()
	mongo.db.history.insert_one({ "query": query, "time": timestamp })
	url = "{0}?key={1}&searchType=image&num=10&q={2}&cx={3}".format(GOOGLE_CUSTOM_SEARCH_URL, GOOGLE_AUTH_KEY, query, GOOGLE_SEARCH_ENGINE)
	the_dict = json.loads(requests.get(url).text)
	result = [ makeDict(item) for item in the_dict['items'] ]
	return jsonify(result)

@app.route('/history', methods=['GET'])
def history():
	query = mongo.db.history.find()
	results = [ makeTimeStamp(item) for item in query ]
	return jsonify(results)

if __name__ == '__main__':
  app.run()
