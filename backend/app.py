from flask import Flask,request,jsonify
from dotenv import load_dotenv
import json
import os
import pymongo

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db=client.test

collection=db['flask_db']
todo_collection=db['todo_items']
app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'GET':
        return (
            "This endpoint expects a POST with JSON or form data: "
        ), 200
    data = dict(request.json)
    username = data.get('name')
    email = data.get('email')
    if not username or not email:
        return "Missing username or email", 400
    try:
        collection.insert_one(data)
    except Exception as e:
        return jsonify({"error":"failed to insert","detail":str(e)}),500
    
    return jsonify({"message":"user data uploaded successfully"}), 201

@app.route('/submittodoitem', methods=['POST'])
def submit_todo_item():
    data = dict(request.json)
    item_name = data.get('itemName')
    item_description = data.get('itemDescription')

    if not item_name or not item_description:
        return jsonify({"error": "itemName and itemDescription are required"}), 400

    # Insert into MongoDB
    try:
        todo_collection.insert_one(data)
    except Exception as e:
        return jsonify({"error": "failed to insert", "detail": str(e)}), 500

    return jsonify({"message": "To-Do item stored successfully"}), 201

@app.route('/api', methods=['GET'])
def api_list():
    json_path = os.path.join(os.path.dirname(__file__), 'data.json')

    if not os.path.exists(json_path):
        return jsonify({"error": "data.json not found"}), 404

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        return jsonify({"error": "data.json is not valid JSON"}), 500
    except Exception as e:
        return jsonify({"error": f"failed to read data.json: {str(e)}"}), 500

    return jsonify(data)

@app.route('/view')
def view():
    records = list(collection.find({}, {'_id': 0}))
    return records

@app.route('/viewtodoitems')
def viewtodoitems():
    records = list(todo_collection.find({}, {'_id': 0}))
    return records

if __name__ == '__main__':
    app.run(debug=True)