#!image-abstraction/bin/python
import os
import datetime
import requests
import json
from flask import Flask, jsonify
from flask_pymongo import PyMongo

import CONFIG_FILE

app = Flask(__name__)
mongo = PyMongo(app)

MONGO_URI = str(os.enviorn.get('MONGO_URI'))
app.config['MONGO_URI'] = 'mongodb://localhost:27017/app' if MONGO_URI is None else MONGO_URI

GOOGLE_AUTH_KEY = str(os.enviorn.get('GOOGLE_AUTH')) if CONFIG_FILE.GOOGLE_AUTH is None else CONFIG_FILE.GOOGLE_AUTH
GOOGLE_SEARCH_ENGINE = str(os.enviorn.get('GOOGLE_SEARCH_ENGINE')) if CONFIG_FILE.GOOGLE_SEARCH_ENGINE is None else CONFIG_FILE.GOOGLE_SEARCH_ENGINE
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

@app.route('/imagesearch/<query>')
def image_search(query):
	timestamp = datetime.datetime.utcnow()
	mongo.db.history.insert_one({ "query": query, "time": timestamp })
	url = "{0}?key={1}&searchType=image&num=10&q={2}&cx={3}".format(GOOGLE_CUSTOM_SEARCH_URL, GOOGLE_AUTH_KEY, query, GOOGLE_SEARCH_ENGINE)
	the_dict = json.loads(requests.get(url).text)
	result = [ makeDict(item) for item in the_dict['items'] ]
	return jsonify(result)

@app.route('/history')
def history():
	query = mongo.db.history.find()
	results = [ makeTimeStamp(item) for item in query ]
	return jsonify(results)

if __name__ == '__main__':
  app.run(debug=True)
