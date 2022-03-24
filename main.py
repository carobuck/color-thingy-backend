from flask import Flask, jsonify, request
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
from datetime import date
import json

import config

app = Flask(__name__)
CORS(app)

# Initialize creds for reading data from firestore
#cred = credentials.Certificate('color-thingy-firebase.json')
cred = credentials.Certificate(config.firestore_secret)
firebase_admin.initialize_app(cred)
db = firestore.client()

## FUNCTIONS
## APP ROUTES
@app.route("/")
def homepage():
    return 'Home Page Route flask gcp app'

@app.route('/about')
def about():
    return 'About Page Route V1'


## Save color + color name + color description for particular user.
@app.route("/saveColor", methods=["POST"])
def saveColor():
    if request.method == "POST":
        data = request.get_json()

        # TODO: if collection exist, but no document, assume it's first entry (thus "self" input for document). else assume "other" person reporting for user
        # ALT: enter in name of who thought you were a particular color (for yourself, it'd be you)...
        # OOOOH : actually: collection = user name/id; document = whoever is giving color description (could be you or someone else)

        # Get all user input from front end
        username = data['user'] # who is color describing? # TODO: this might turn into unique userid??
        reporter = data['reporter'] # who is giving color description? (could be self or other person)
        color = data['color']
        color_name = data['color_name']
        color_reason = data['color_reason']

        # Push data to proper Firestore collection/document
        fs_data = {'color':color,'color_name':color_name,'color_reason':color_reason}
        db.collection(username).document(reporter).set(fs_data, merge=True)

        #doc_ref = db.collection(country).document(interventions).collection(starting_event).document(data_req)
        #doc = doc_ref.get()
        #data = doc.to_dict()

        return jsonify('hello') # TODO: can't have empty return stmt for Flask??

## Get all colors/entries for a user
@app.route("/getColors", methods=["POST"])
def getColors():
    if request.method == "POST":
        data = request.get_json()
        username = data['user']

        docs = db.collection(username).stream()
        results = {}
        for doc in docs:
            temp = {doc.id:doc.to_dict()}
            results.update(temp)
        
        return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
