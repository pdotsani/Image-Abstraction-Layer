#!image-abstraction/bin/python
from flask import Flask
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/imagesearch')
def image_search():
    return "Image search results here!"

@app.route('/history')
def history():
    return "Search history here!"

if __name__ == '__main__':
    app.run(debug=True)