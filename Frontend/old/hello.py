import os
import socket
import io
import struct
import cv2
import os
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template('hello.html')

port = os.getenv('PORT', '5000')

server_socket = socket.socket()
server_socket.bind(('', int(port)))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
try:
    while True:
        # Read the length of the image as a 32-bit unsigned int. If the
        # length is zero, quit the loop
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
        if not image_len:
            break
        # Construct a stream to hold the image data and read the image
        # data from the connection
        image_stream = io.BytesIO()
        image_stream.write(connection.read(image_len))
        # Rewind the stream, open it as an image with PIL and do some
        # processing on it
        image_stream.seek(0)
        file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.flip(img,0)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        print("FOUND {0} faces!".format((len(faces))))

        # Draw a rectangle around the faces
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

        cv2.imshow("Image", img)
        cv2.waitKey(1)
        #image = Image.open(image_stream)
        #print('Image is %dx%d' % image.size)
        #image.verify()
        #print('Image is verified')
finally:
    connection.close()
    server_socket.close()

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))


