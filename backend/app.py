from flask import Flask,request
from dotenv import load_dotenv
import os
import pymongo

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db=client.test

collection=db['flask_db']
app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    data = dict(request.json)
    username = data.get('name')
    email = data.get('email')
    if not username or not email:
        return "Missing username or email", 400
    
    collection.insert_one(data)
    return f"Received username: {username}, email: {email}", 200

@app.route('/view')
def view():
    records = list(collection.find({}, {'_id': 0}))
    return records

if __name__ == '__main__':
    app.run(debug=True)