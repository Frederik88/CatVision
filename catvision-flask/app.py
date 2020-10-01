#!/usr/bin/env python
from flask import Flask, render_template, Response, jsonify, request
import requests
import os
import sys
import json
import types
import time
import cv2
import chardet
import io
from DatabaseTransaction import DatabaseTransaction
from Yolo import Yolo;
from PIL import Image
import numpy as np

app = Flask(__name__)
DatabaseTransaction = DatabaseTransaction();
Yolo = Yolo();


@app.route('/api/v1/transfer')
def transfer_capture():
    r =requests.get('http://localhost:8081/api/capture')
    r.status_code
    r.headers['Content-Type']
    
    image = app.response_class(
        response = bytearray(r.content),
        status = 200,
        mimetype='image/jpeg'
        )
    
    img_name = time.strftime("%Y%m%d-%H%M%S") + '.jpeg'
    path = 'F:\\20200914_CatVision_TechDay\\CatVision\Images\\' + img_name
    img = np.array(Image.open(io.BytesIO(r.content)))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    text = ""
    detection = False
    
    img, label, conf = Yolo.forward_pass(img, 0.5, 0.3)
    
    if(conf == 0 or label != 'cat'):
        text = "None"
        detection = False
    else:
        text = "{}: {:.4f}".format('Cat', conf)
        detection = True
    
    cv2.imwrite(path, img)
    DatabaseTransaction.save_img_to_db(path, text, time.strftime("%Y%m%d-%H%M%S"), detection)
    
    return image



port = os.getenv('PORT', '5000')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port), threaded=True)
