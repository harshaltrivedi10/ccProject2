from flask import Flask, render_template, jsonify, make_response, request
from flask_restful import Resource, Api     
from google.cloud import storage
import os
import http.client, urllib.request, urllib.parse, urllib.error, base64, json, wave
from google.cloud import firestore
import time
from google.cloud import speech_v1
import io
import pandas as pd
import boto3
from botocore.exceptions import ClientError
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
api = Api(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/uploadFile", methods=['POST'])
def uploadToBucket():
    fileName = request.args.get('fileName')
    userName = request.args.get('userName')
    totalFilePath = fileName
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    storage_client = storage.Client("cse546-final")
    bucket = storage_client.get_bucket("cc-audio-bucket")
    blob = bucket.blob(fileName)
    profileId = createProfile()

    # Add a new document
    db = firestore.Client()
    doc_ref = db.collection('enrolledUsers').document(str(profileId))
    doc_ref.set({'name': str(userName)})

    #in document name insert the profile id
    print(db.collection('enrolledUsers').document(str(profileId)).get().to_dict())
    enrollUser(profileId, fileName)

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

def enrollUser(profile_id, fileName):
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
        blob = bucket.blob(fileName)
        print(fileName)
        print(profile_id)
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        with open('/tmp/'+fileName, 'wb') as fileObject:
            blob.download_to_file(fileObject)
        w = open('/tmp/'+fileName, "rb").read()
        print(w)
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
        storage_client = storage.Client("cse546-final")
        bucket = storage_client.get_bucket("cc-audio-bucket")
        blob = bucket.blob(fileName)
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        print(fileName)
        with open('/tmp/'+fileName, 'wb') as fileObject:
            blob.download_to_file(fileObject)
        w = open('/tmp/'+fileName, "rb").read()
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
            print(data['processingResult']['identifiedProfileId'])
            speakerProfileId = data['processingResult']['identifiedProfileId']
            speechToText(speakerProfileId, fileName)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def speechToText(speakerProfileId, storage_uri):
    print(speakerProfileId)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    client = speech_v1.SpeechClient()
    sample_rate_hertz = 16000
    language_code = "en-US"
    config = {
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        }

    with io.open('/tmp/'+storage_uri, "rb") as f:
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
    docReferenceScore = fireStoreClient.collection('performanceScore').document(str(userName))
    importantWords = ["welcome", "thank you", "sorry", "apologise", "apologize", "good day", "nice day", "good morning", "good evening", "good noon", "awesome", "sweet", "hope", "see you", "bye", "hello", "hi", "please", "sure", "sort", "sorted", "enjoy", "safe"]
    wordsSpoken = dict()
    print(transcript)

    for word in importantWords:
        if word in transcript:
            wordsSpoken[word] = transcript.count(word)
    print(wordsSpoken)
    try:
        word_dct = docReferenceScore.get().to_dict()
        for word, freq in wordsSpoken.items():
            if word in word_dct.keys():
                new_freq = word_dct[word]["frequency"] + freq
                docReferenceScore.set({word: {"frequency": new_freq}}, merge=True)
            else:
                docReferenceScore.set({word: {"frequency": freq}}, merge=True)
    except:
        for word, freq in wordsSpoken.items():
            docReferenceScore.set({word: {"frequency": freq}}, merge=True)

@app.route('/generateAndDownloadReport', methods=['GET', 'POST'])
def downloadAndGenerateReport():
    emailAddress = request.args.get('emailAddress')
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
    db = firestore.Client()
    doc_ref = db.collection('performanceScore')
    docs = list(doc_ref.stream())
    final_d = {}
    for i in docs:
        d = i.to_dict()
        for item in d.items():
            d[item[0]] = item[1]['frequency']
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

    df.to_csv('/tmp/'+fileName)
    #storage_client = storage.Client("cse546-final")
    #bucket = storage_client.get_bucket("cc-reports-bucket")
    #bucket.blob('newReport.csv').upload_from_string(df.to_csv(), 'text/csv')
    #blob = bucket.blob('newReport.csv')
    time.sleep(3)
    sendEmail(emailAddress, '/tmp/'+fileName)
    res = ["Identification successfully handled!"]
    resp = make_response(jsonify(res))

    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = '*'

    return resp

def sendEmail(recepient, file_name):
    sender = 'ap@cdarevon.com'
    aws_region = 'us-east-1'
    subject = 'Customer Representative Report'
    BODY_TEXT = "Hello,\r\nThis mail contains the report generated of the customer representatives.."
    # The HTML body of the email.
    BODY_HTML = """\
    <html>
    <head></head>
    <body>
    <h4>Hello!</h4>
    <h4>Please find the attached file of the report generated of the customer representatives.</h4>
    <h4>Thank You</h4>
    </body>
    </html>
    """
    CHARSET = "utf-8"
    client = boto3.client('ses', region_name=aws_region, aws_access_key_id="AKIAVSEGXB4YT5M4W5AB",
                          aws_secret_access_key="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")
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = sender
    # msg['To'] = recipient
    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)
    att = MIMEApplication(open(file_name, 'rb').read())
    att.add_header('Content-Disposition', 'attachment', filename="report.csv")

    if os.path.exists(file_name):
        print("File exists")
    else:
        print("File does not exists")

    msg.attach(msg_body)
    msg.attach(att)
    try:
        response = client.send_raw_email(
            Source=msg['From'],
            Destinations=[recepient],
            RawMessage={
                'Data': msg.as_string(),
            }
        )
    except ClientError as e:

        return (e.response['Error']['Message'])
    else:
        return ("Email sent! Message ID"+response["MessageId"])

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
