from flask import Flask, render_template, jsonify, make_response, request
from flask_restful import Resource, Api     
from google.cloud import storage
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, wave
from google.cloud import firestore


app = Flask(__name__)
api = Api(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/uploadFile", methods=['POST'])
def uploadToBucket():
    fileName = request.args.get('fileName')
    userName = request.args.get('userName')
    print("in here")
    totalFilePath = "C:\\Users\\iRoNhIdE\\Desktop\\" + fileName
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\\Arizona State University\\SEM-4\\CC\\Project2\\key.json"
    
    storage_client = storage.Client("CCHostedApp")
    bucket = storage_client.get_bucket("cc-project2-audio-file-bucket")
    blob = bucket.blob("Recording.wav")
    blob.upload_from_filename(totalFilePath)

    profileId = createProfile()

    # Add a new document
    db = firestore.Client()
    doc_ref = db.collection('enrolledUsers').document(str(profileId))
    doc_ref.set({'name': str(userName)})

    #in document name insert the profile id
    print(db.collection('enrolledUsers').document(str(profileId)).get().to_dict())
    enrollUser(profileId)

    res = ["Request successfully handled!"]
    resp = make_response(jsonify(res))

    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = '*'

    return resp

def createProfile():
    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': 'fe0249ae98df4780a901ec3594467e3c',
    }
    params = urllib.parse.urlencode({})

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/spid/v1.0/identificationProfiles?%s" % params, "{\"locale\":\"en-US\"}", headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        data = json.loads(data)
        profile_id = data['identificationProfileId']
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return profile_id

def enrollUser(profile_id):
    headers = {
        # Request headers
        'Content-Type': 'multipart/form-data',
        'Ocp-Apim-Subscription-Key': 'fe0249ae98df4780a901ec3594467e3c',
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'shortAudio': True,
    })
    try:
        storage_client = storage.Client("CCHostedApp")
        bucket = storage_client.get_bucket("cc-project2-audio-file-bucket")
        blob = bucket.blob("Recording.wav")
        blob.download_to_filename("Recording.wav")
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        w = open("sample.wav", "rb").read()
        # code to download the audio from bucket
        conn.request("POST", "/spid/v1.0/identificationProfiles/"+profile_id+"/enroll?%s" % params, w, headers)
        # response = conn.getresponse()
        conn.close()
        print("User Enrolled Successfully...!")
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


if __name__ == "__main__":
    app.run(debug=True)
