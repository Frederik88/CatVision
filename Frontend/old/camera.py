import io
import socket
import struct
import cv2
import os
import numpy as np
from flask import Flask, render_template, Response
from tkinter import *
from PIL import ImageTk, Image


class Camera:
    server_socket = []
    connection = []

    def __init__(self):
        Camera.server_socket = socket.socket()
        Camera.server_socket.bind(('', 8000))
        Camera.server_socket.listen(0)
        Camera.connection = Camera.server_socket.accept()[0].makefile('rb')


    def frames(self):
        #try:
        #    while True:
                # Read the length of the image as a 32-bit unsigned int. If the
                # length is zero, quit the loop
        image_len = struct.unpack('<L', Camera.connection.read(struct.calcsize('<L')))[0]
        #        if not image_len:
        #            break
                # Construct a stream to hold the image data and read the image
                # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(Camera.connection.read(image_len))
                # Rewind the stream, open it as an image with PIL and do some
                # processing on it
        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        return cv2.imencode('.jpg', img)[1].tobytes()
        #finally:
        #   Camera.connection.close()
        #    Camera.server_socket.close()


