#################################### 
# IoT 2-Factor-Auth Door Lock (Facial + Voice Recognition)
# Kevin Leung @KSLHacks (Git: KSLHacks)
# James Earle @ItsJamesIRL (Git: JamesEarle)
# 9/12/2016

########### Python 2.7 #############
import httplib
import urllib
import base64
import json

headersDetect = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': '<Cognitive Service Face Key Here>',
}

paramsDetect = urllib.urlencode({
    # Request parameters
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
})

headersVerify = {
    # Request headers
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '<Cognitive Service Face Key Here>',
}

paramsVerify = urllib.urlencode({
})

def faceVerify():
    ########### Cognitive Services Face - Detect #############
    # Read the binary from the jpg file
    f = open("./output.jpg", "rb")
    try: 
        bodyDetect = f.read()
    finally:
        f.close()

    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/detect?%s" % paramsDetect, bodyDetect, headersDetect)
        response = conn.getresponse()
        data = response.read()
        # print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    faceDetectJson = json.loads(data)
    
    if(faceDetectJson == []): return False

    ########### Cognitive Services Face - Verify #############
    bodyVerify = "{\
    \"faceId1\":\"<Control faceId here - run the detect API to obtain faceId>\",\
    \"faceId2\":\"" + faceDetectJson[0]["faceId"] + "\"}"

    # print(bodyVerify)
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("POST", "/face/v1.0/verify?%s" % paramsVerify, bodyVerify, headersVerify)
        response = conn.getresponse()
        data = response.read()
        print(data)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    faceVerifyJson = json.loads(data)
    # print(faceVerifyJson)
    isIdentical = faceVerifyJson["isIdentical"]
    # print(isIdentical)
    return isIdentical
    