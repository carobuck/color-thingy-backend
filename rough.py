## trying to use googles KMS service...but not really sure what I'm getting into. Come back if other stuff fails
## NOTE: this worked for saving keys safely, and deployed version works too!! :) https://medium.com/black-tech-diva/hide-your-api-keys-7635e181a06c
from google.cloud import kms

# Create the client.
client = kms.KeyManagementServiceClient()

# Build the parent location name.
location_name = f'projects/{project_id}/locations/{location_id}'

# Call the API.
key_rings = client.list_key_rings(request={'parent': location_name})

# Example of iterating over key rings.
for key_ring in key_rings:
    print(key_ring.name)


## Test get all data from firestore for particular user
import config
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
cred = credentials.Certificate(config.firestore_secret)
firebase_admin.initialize_app(cred)
db = firestore.client()

username = 'caro'
docs = db.collection(username).stream()
results = {}
for doc in docs:
    temp = {doc.id:doc.to_dict()}
    results.update(temp)
results # then return jsonify-ed version of this
