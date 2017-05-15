#!image-abstraction/bin/python
import requests
import json
from flask import Flask, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

GOOGLE_AUTH_KEY = "AIzaSyD4-UXkrmqT-nj4pqcbEMBPF13I8QFhRIU"
GOOGLE_CUSTOM_SEARCH_URL = 'https://www.googleapis.com/customsearch/v1'
GOOGLE_SEARCH_ENGINE = "016465477141158983016:zw10rls-o5c"

def makeDict(item):
	return {
		'title': item['title'],
		'html': item['htmlSnippet'],
		'link': item['link'],
		'thumb': item['image']['thumbnailLink']
	}

@app.route('/imagesearch/<query>')
def image_search(query):
	url = "{0}?key={1}&searchType=image&num=10&q={2}&cx={3}".format(GOOGLE_CUSTOM_SEARCH_URL, GOOGLE_AUTH_KEY, query, GOOGLE_SEARCH_ENGINE)
	the_dict = json.loads(requests.get(url).text)
	result = [makeDict(item) for item in the_dict['items']]
	return jsonify(result)

@app.route('/history')
def history():
  return "Search history here!"

if __name__ == '__main__':
  app.run(debug=True)
