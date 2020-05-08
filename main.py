from flask import Flask, render_template, jsonify, make_response, request
from flask_restful import Resource, Api     
from google.cloud import storage
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, wave
from google.cloud import firestore
import time
#import librosa
from google.cloud import speech_v1
import io
import pandas as pd

app = Flask(__name__)
api = Api(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/uploadFile", methods=['POST'])
def uploadToBucket():
    fileName = request.args.get('fileName')
    userName = request.args.get('userName')
    #print("in here")
    totalFilePath = "C:\\Users\\iRoNhIdE\\Desktop\\" + fileName
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\\Arizona State University\\SEM-4\\CC\\Project2\\key.json"
    
    storage_client = storage.Client("cse546-final")
    bucket = storage_client.get_bucket("cc-audio-bucket")
    blob = bucket.blob(fileName)
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
        'shortAudio': 'true',
    })
    try:
        storage_client = storage.Client("cse546-final")
        bucket = storage_client.get_bucket("cc-audio-bucket")
        blob = bucket.blob("Recording.wav")
        blob.download_to_filename("Recording.wav")
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        w = open("Recording.wav", "rb").read()
        #print(librosa.get_duration(filename="Recording.wav"))
        print(profile_id)
        # code to download the audio from bucket
        conn.request("POST", "/spid/v1.0/identificationProfiles/"+profile_id+"/enroll?%s" % params, w, headers)
        response = conn.getresponse()
        print(response.headers)
        conn.close()
        print("User Enrolled Successfully...!")
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

@app.route('/identifyUser', methods=['GET', 'POST'])
def identifyAndGenerateReport():
    fileName = request.args.get('fileName')
    #totalFilePath =  + fileName
    status_id = getStatusId(fileName)
    time.sleep(15)
    getSpeaker(status_id, fileName)

    res = ["Identification successfully handled!"]
    resp = make_response(jsonify(res))

    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = '*'

    return resp

def getProfileIds():
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'fe0249ae98df4780a901ec3594467e3c',
    }

    params = urllib.parse.urlencode({
    })

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("GET", "/spid/v1.0/identificationProfiles?%s" % params, "", headers)
        response = conn.getresponse()
        data = response.read().decode('utf-8')
        data = json.loads(data)
        ids = []
        for i in data:
            ids.append(i['identificationProfileId'])
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return ids

def getStatusId(fileName):
    profile_ids = getProfileIds()
    print(profile_ids)
    #insert code to get all the enrolled profile ids
    ids = ",".join(id for id in profile_ids)

    headers = {
        # Request headers
        'Content-Type': 'application/form-data',
        'Content-Type': 'audio/wave',
        'Ocp-Apim-Subscription-Key': 'fe0249ae98df4780a901ec3594467e3c'
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'shortAudio': 'true'
    })

    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        print(fileName)
        #print(librosa.get_duration(filename=fileName))
        w = open(fileName, "rb").read()
        # insert code to download audio from bucket
        conn.request("POST", "/spid/v1.0/identify?identificationProfileIds=%s&%s" % (ids,params),w, headers)
        response = conn.getresponse()

        stat_id = response.headers["Operation-Location"].split("/")[-1]
        print(stat_id)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return stat_id

def getSpeaker(statusId, fileName):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': 'fe0249ae98df4780a901ec3594467e3c',
    }
    params = urllib.parse.urlencode({
    })
    try:
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("GET", "/spid/v1.0/operations/%s?%s" % (statusId,params), "", headers)
        response = conn.getresponse()
        data = response.read().decode("utf-8")
        data = json.loads(data)
        print(data)
        if data['processingResult'] == None:
            print("No user Found")
        else:
           #print("Jari reje")
            print(data['processingResult']['identifiedProfileId'])
            speakerProfileId = data['processingResult']['identifiedProfileId']

            if (speakerProfileId and fileName):
                speechToText(speakerProfileId, fileName)
            else:
                print("Error")
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def speechToText(speakerProfileId, storage_uri):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\\Arizona State University\\SEM-4\\CC\\Project2\\key.json"
    client = speech_v1.SpeechClient()
    sample_rate_hertz = 16000
    language_code = "en-US"
    config = {
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        }

    with io.open(storage_uri, "rb") as f:
        content = f.read()
    audio = {"content": content}

    operation = client.long_running_recognize(config, audio)
    response = operation.result()
    transcript = ""
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        transcript += alternative.transcript
    fireStoreClient = firestore.Client()
    docReference = fireStoreClient.collection("enrolledUsers").document(speakerProfileId).get().to_dict()
    userName = docReference["name"]
    docReferenceScore = fireStoreClient.collection('performanceScore').document(userName)
    importantWords = ["welcome", "thank you", "sorry", "apologise", "apologize", "good day", "nice day", "good morning", "good evening", "good noon", "awesome", "sweet", "hope", "see you", "bye", "hello", "hi", "please", "sure", "sort", "sorted", "enjoy", "safe"]
    wordsSpoken = dict()
    for word in importantWords:
        if word in transcript:
            wordsSpoken[word] = transcript.count(word)

    try:
        word_dct = doc_ref.get().to_dict()
        for word, freq in wordsSpoken.items():
            if word in word_dct.keys():
                new_freq = word_dct[word]["frequency"] + freq
                docReferenceScore.set({word: {"frequency": new_freq}}, merge=True)
            else:
                docReferenceScore.set({word: {"frequency": freq}}, merge=True)
    except:
        for word, freq in wordsSpoken.items():
            docReferenceScore.set({word: {"frequency": freq}}, merge=True)

@app.route('/generateAndDownloadReport', methods=['GET'])
def downloadAndGenerateReport():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "D:\\Arizona State University\\SEM-4\\CC\\Project2\\key.json"
    db = firestore.Client()
    doc_ref = db.collection('performanceScore')
    doc_ref = db.collection('performanceScore')
    docs = list(doc_ref.stream())
    final_d = {}
    for i in docs:
        d = i.to_dict()
        for item in d.items():
            d[item[0]] = item[1]['frequency']
        # d['name'] = i.id
        final_d[i.id] = d

    df = pd.DataFrame.from_dict(final_d, orient='index')
    df.fillna(0, inplace=True)
    df['Total Score'] = df.sum(axis=1)
    avg = df['Total Score'].sum() / len(df.index)
    scores = []
    for s in df['Total Score']:
        val = ((s/avg)*100)-100
        if val < 0:
            scores.append(str(abs(round(val, 2)))+"% Below Mean")
        else:
            scores.append(str(abs(round(val, 2))) + "% Above Mean")
    for i, (index, row) in enumerate(df.iterrows()):
        final_d[index]['Total Score'] = row['Total Score']
        final_d[index]['Performance'] = scores[i]

    df = pd.DataFrame.from_dict(final_d, orient='index')
    df.fillna(0, inplace=True)
    print(df)
    fileName = "report.csv"
    df.to_csv(fileName)

    storage_client = storage.Client("cse546-final")
    bucket = storage_client.get_bucket("cc-reports-bucket")
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    time.sleep(3)
    blob.download_to_filename('downloaded'+fileName)

    res = ["Identification successfully handled!"]
    resp = make_response(jsonify(res))

    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = '*'

    return resp

if __name__ == "__main__":
    app.run(debug=True)
