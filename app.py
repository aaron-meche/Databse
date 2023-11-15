from flask import Flask, jsonify, request
from flask_cors import CORS

import random
import json

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


# Utility
def new_key():
    key1 = random.randint(0,999999)    # 6
    key2 = random.randint(0,999999999) # 9
    key3 = random.randint(0,999)       # 3
    key = str(key1) + "-" + str(key2) + "-" + str(key3)
    return key
def get_value_from_path(data, path):
    # Split the path into its components
    keys = path.split('/')
    
    # Traverse the dictionary using the keys
    for key in keys:
        # Check if the key is a digit to assume it's an index for a list
        if key.isdigit() and isinstance(data, list):
            key = int(key)  # Convert to integer for list indexing
        try:
            data = data[key]
        except (KeyError, IndexError, TypeError):
            # Handle the error if key is not found, the index is out of range,
            # or the current object is not subscriptable (not a list/dict)
            return None
    
    return data


# constants
@app.route('/const')
def const():
    with open('#const.json', 'r') as file:
        data = json.load(file)
    return jsonify(data)

# connect
@app.route('/connect/<password>')
def connect(password):
    # Get Base URL
    scheme = request.scheme
    server = request.host
    base_url = f"{scheme}://{server}"
    key = new_key()

    db_identity = {
        "URL": base_url,
        "Key": key
    }
    return jsonify(db_identity)

# login
@app.route('/login/<username>/<password>')
def login(username, password):
    with open('@data.json', 'r') as file:
        data = json.load(file)
        user_password = data["users"][username]["password"]
        
        if (password == user_password):
            auth_key = new_key()
            return jsonify({"auth": auth_key})
        else:
            return jsonify({})

# read
@app.route('/read/<path>')
def read(path):
    with open('@data.json', 'r') as file:
        data = json.load(file)
        print(path)
    return jsonify(data)



# Run the Flask app
if __name__ == '__main__':
    app.run(debug = False)