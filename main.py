from flask import Flask, jsonify, request
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd
from datetime import date
import json

app = Flask(__name__)
CORS(app)

# Initialize creds for reading data from firestore
#cred = credentials.Certificate('firebase_secret.json')
#firebase_admin.initialize_app(cred)
#db = firestore.client()

## FUNCTIONS
## APP ROUTES
@app.route("/")
def homepage():
    return 'Home Page Route flask gcp app'

@app.route('/about')
def about():
    return 'About Page Route V1'


## ALT IF WE SAVE LONGER-DOC/COLLECTION CHAIN IN FIRESTORE ##
@app.route("/getData", methods=["POST"])
def getData():
    if request.method == "POST":
        data = request.get_json()

        # Get all user input from front end
        #country = data['country']
        #starting_event = data['startingEvent']
        #vax,sd,quar = data['interventions'] # interventions passed as list of #: [vax,socialDist,quar]
        #interventions = 'vax' + str(vax) + '_sd' + str(sd) + '_quar' + str(quar) # put in format to match in firestore

        #data_req = data['request'] # what piece of info is frontend asking for? (e.g. map, line chart data, etc.)

        # Pull collection/document for specified parameters:
        #doc_ref = db.collection(country).document(interventions).collection(starting_event).document(data_req)
        #doc = doc_ref.get()
        #data = doc.to_dict()

        #if data_req == 'viz_cal': # Need to add dynamic dates to daily infection values
    #        data['data'] = wrangle_cal(data['data'])
#
#        if data_req == 'viz_map': # Need to convert 'load' data to convert to json (from string format firestore needs to save)
#            data['data'] = json.loads(data['data'])

        return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True)
