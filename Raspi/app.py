from flask import Flask, request, Response
import jsonpickle
import json
from io import BytesIO
import numpy as np
import cv2
from CameraControl import CameraControl

app = Flask(__name__)

CameraControl = CameraControl()

@app.route('/api/capture', methods=['GET'])
def capture():
    cap = CameraControl.start_capture()

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}
    
    #img = cv2.imread(cap)
    _, img_encoded = cv2.imencode('.jpg', cap)
    
    response = app.response_class(
        response = bytearray(img_encoded),
        status = 200,
        mimetype='image/jpeg'
        )
    return response
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(8080), threaded=True)