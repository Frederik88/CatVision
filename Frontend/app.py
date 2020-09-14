#!/usr/bin/env python
from flask import Flask, render_template, Response, jsonify, request
import os
import sys
import json
import types

sys.path.append('../')

from Backend.Stream import Stream
from Backend.MotorClient import MotorClient
from Backend.LogData import LogData

app = Flask(__name__)

MotorClient = MotorClient(54321)
Stream = Stream()
Stream.load_net_parameters()

fps_log = types.SimpleNamespace
ms_log = types.SimpleNamespace
detected_log = types.SimpleNamespace

check_yolo = False
check_tiny_yolo = False
check_rcnn = False
check_ssd = False

check_writing = False


@app.route('/')
def index():
    """
    Routing to index.html page
    :return: index.html
    """
    return render_template('index.html')


# YOLO
@app.route('/button1')
def trigger_yolo_processing():
    """
    Trigger Yolo processing with specific routing url.
    Activates or deactivates the check parameter for the
    stream class depending on the current status of the
    parameter. Linked to Yolo Button displayed in the
    index.html.

    :return: OK message
    """
    global check_yolo
    global check_tiny_yolo
    global check_ssd
    global check_rcnn

    check_yolo = not check_yolo

    check_tiny_yolo = False
    check_ssd = False
    check_rcnn = False

    return 'OK'


# Tiny YOLO
@app.route('/button2')
def trigger_tiny_yolo_processing():
    """
    Trigger Tiny Yolo processing with specific routing url.
    Activates or deactivates the check parameter for the
    stream class depending on the current status of the
    parameter. Linked to Tiny Yolo Button displayed in
    the index.html.

    :return: OK message
    """
    global check_yolo
    global check_tiny_yolo
    global check_ssd
    global check_rcnn

    check_tiny_yolo = not check_tiny_yolo

    check_yolo = False
    check_ssd = False
    check_rcnn = False

    return 'OK'


# Faster R-CNN
@app.route('/button3')
def trigger_rcnn_processing():
    """
    Trigger Faster R-CNN processing with specific routing url.
    Activates or deactivates the check parameter for the
    stream class depending on the current status of the
    parameter. Linked to Faster R-CNN Button displayed in
    the index.html.

    :return: OK message
    """
    global check_yolo
    global check_tiny_yolo
    global check_ssd
    global check_rcnn

    check_rcnn = not check_rcnn

    check_yolo = False
    check_ssd = False
    check_tiny_yolo = False

    return 'OK'


# SSD
@app.route('/button4')
def trigger_ssd_processing():
    """
    Trigger SSD processing with specific routing url.
    Activates or deactivates the check parameter for the
    stream class depending on the current status of the
    parameter. Linked to SSD Button displayed in the
    index.html.

    :return: OK message
    """
    global check_yolo
    global check_tiny_yolo
    global check_ssd
    global check_rcnn

    check_ssd = not check_ssd

    check_yolo = False
    check_rcnn = False
    check_tiny_yolo = False

    return 'OK'


# Load parameters from nets
#@app.route('/button5')
#def load_net_parameter():
#    """
#    Trigger loading of net parameters with specific
#    routing url. Linked to Load Net Parameter Button
#    displayed in the index.html.

#    :return: OK message
#    """
#    Stream.load_net_parameters()

#    return 'OK'


# Start date fetching
@app.route('/button6')
def data_fetching():
    """
    Trigger data fetching with specific routing url.
    Creates logging files for performance parameters.
    Activation or deactivation depends on the current
    status of the check parameter. Linked to Start
    Fetching Data Button displayed in the index.html.

    :return: OK message
    """
    global check_writing
    global fps_log
    global ms_log
    global detected_log
    #check_writing = not check_writing

    #if check_writing:
    #    fps_log = LogData("FPS")
    #    ms_log = LogData("MS")
    #    detected_log = LogData("Detection")
    #else:
    #    fps_log.close_file()
    #    ms_log.close_file()
    #    detected_log.close_file()

    return 'OK'

# Start Motor
@app.route('/button7')
def start_motor():
    """
    Start Motor
    """
    MotorClient.send_start()

    return 'OK'

# Stop Motor
@app.route('/button8')
def stop_motor():
    """
    Stop Motor
    """
    MotorClient.send_stop()

    return 'OK'

# Get slider value and send it to motor
@app.route('/slider', methods=['GET', 'POST'])
def send_pwm():
    """
    Send value to pwm module
    """
    post = request.args.get('post', 0, type=int)
    MotorClient.send_pwm(post)

    return 'OK'


# Send fps data to javascript frontend
@app.route('/fps')
def send_fps_json():
    """
    Trigger fetching of fps data to frontend with specific
    routing url. If the check parameter is true, the fps data
    is send via json message and displayed in a diagram dis-
    played in the frontend page. Writes fps data to created
    log file.

    :return: OK message
    """
    global check_writing
    global fps_log
    message = {'FPS': Stream.frames_per_second}

    #if check_writing:
    #    fps_log.write_date(Stream.frames_per_second)

    return jsonify(message)


# Send ms data to javascript frontend
@app.route('/sec')
def send_sec_json():
    """
    Trigger fetching of ms data to frontend with specific
    routing url. If the check parameter is true, the fps data
    is send via json message and displayed in a diagram dis-
    played in the frontend page. Writes ms data to created
    log file.

    :return: OK message
    """
    global check_writing
    global ms_log
    message = {'SEC': Stream.ms_second}

    #if check_writing:
    #    ms_log.write_date(Stream.ms_second)

    return jsonify(message)


# Send counted data to javascript frontend
@app.route('/detected')
def send_obj_counts_json():
    """
    Trigger fetching of detection data to frontend with specific
    routing url. If the check parameter is true, the detection
    data is send via json message and displayed in a diagram dis-
    played in the frontend page. Writes detection data to created
    log file.

    :return: OK message
    """
    message = {
        'ONE': Stream.obj1,
        'TWO': Stream.obj2,
        'THREE': Stream.obj3
    }

    #if check_writing:
    #    detected_log.write_date(Stream.class_name +" "+ str(Stream.class_conf) +" "+ str(Stream.obj1)
    #                            + " " + str(Stream.obj2) +" "+ str(Stream.obj3))

    return jsonify(message)

@app.route('/perf')
def send_perf_json():
    try:
        message = {
            'FPS': Stream.frames_per_second,
            'SEC': Stream.ms_second,
            'HAZ': Stream.obj1,
            'WAL': Stream.obj2,
            'PEA': Stream.obj3
        }
    except:
         message = {
            'FPS': 0,
            'SEC': 0.0,
            'HAZ': 0,
            'WAL': 0,
            'PEA': 0
        }
    return jsonify(message)

@app.route('/button5')
def reset():
    try:
        Stream.obj1 = 0
        Stream.obj2 = 0
        Stream.obj3 = 0
    except:
        print("Stream class not loaded")

    return "OK"




def stream_generator():
    """
    Generator function for creating a continuous image stream
    which is displayed in the frontend page. Initialises the frame
    grabbing from the ip camera and send the grabbed frames to the
    Stream class for processing. Depending on the activated check
    parameter, a specific algorithm is used for object detection inside
    the Stream class. The processing starts when the frame from the ip
    camera yields a valid image. The stream is stopped when the stop function
    of the FrameShow class is activated or closed via disconnect of the ip
    camera.

    :yield: processed image frame
    """
    frame_show = Stream.fetch_frame_data()
    while frame_show.stopped != True:

        image = frame_show.frame

        if image != []:
            image = Stream.start_processing(image=image,
                                            check_yolo=check_yolo,
                                            check_tiny_yolo=check_tiny_yolo,
                                            check_rcnn=check_rcnn,
                                            check_ssd=check_ssd)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """
    Video streaming route to display the video stream inside
    the frontend page.
    """
    return Response(stream_generator(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

port = os.getenv('PORT', '8080')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(port), threaded=True)
