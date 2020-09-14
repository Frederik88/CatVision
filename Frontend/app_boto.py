#!/usr/bin/env python
from flask import Flask, render_template, Response, flash
import os
import cv2
import boto3

# import camera driver
# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

app = Flask(__name__)

STREAM_NAME = "RaspStream"
kvs = boto3.client('kinesisvideo')
print(kvs)
# Grab the endpoint from GetDataEndpoint
endpoint = kvs.get_data_endpoint(
    APIName="GET_HLS_STREAMING_SESSION_URL",
    StreamName=STREAM_NAME
)['DataEndpoint']

print(endpoint)

# # Grab the HLS Stream URL from the endpoint
kvam = boto3.client("kinesis-video-archived-media", endpoint_url=endpoint)
url = kvam.get_hls_streaming_session_url(
    StreamName=STREAM_NAME,
    PlaybackMode="LIVE"
)['HLSStreamingSessionURL']

print(STREAM_NAME)

vcap = cv2.VideoCapture(url)
print(vcap)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/button1')
def algo1():
    print('Hello Button 1')

@app.route('/button2')
def algo2():
    print('Hello Button 2')

@app.route('/button3')
def algo3():
    print('Hello Button 3')

@app.route('/button4')
def algo4():
    print('Hello Button 4')



port = os.getenv('PORT', '5000')

def gen():
    """Video streaming generator function."""
    while True:
        # Capture frame-by-frame
        ret, frame = vcap.read()

        if frame is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            image = cv2.imencode('.jpg', gray)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


            if cv2.waitKey(22) & 0xFF == ord('q'):
                break
        else:
            print("Frame is None")
            break

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port), threaded=True)