# TODO: separate this code into front-end and back-end.
# TODO:create pytest for this code(maybe something that checks the values of the requests
# TODO: crate 2 dockerfiles(one for each file) with requirements.txt and try is as a pod

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

# Connect to your MongoDB instance 
username="root"
password="3yGWpZ7jeS"
client = MongoClient(f'mongodb://{username}:{password}@34.78.116.136:27017/')
db = client['omri_pro']
collection = db['omri_url']
#backend - connection to db 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        url = request.form['url']

        # Insert the new key-value pair into MongoDB
        collection.insert_one({'text': text, 'url': url})
    urls = list(collection.find())  # Retrieve all key-value pairs from MongoDB
    return render_template('index.html', urls=urls)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=9001, debug=True)
