from threading import Thread
import socket
import struct
import time
import numpy as np
import io
import pickle
import cv2


class FrameShow:

    def __init__(self):
        """
        Creates a object for handling and receiving image data from
        an ip camera. The constructor initializes a socket connection
        which listens on a specific port. When the ip camera connects to
        that port, the image date can be grabbed and processed.
        """
        print('[FRAMESHOW INIT] Initialize connection')
        self.__server_socket = socket.socket()
        self.__server_socket.bind(('', 12345))
        self.__server_socket.listen(0)
        self.frame = []
        self.__connection, self.__address = self.__server_socket.accept() #self.__server_socket.accept()[0].makefile('rb')
        self.stopped = False
        print('[FRAMESHOW INIT] Connected')

    def start(self):
        """
        Starts a thread for grabbing image data from the connected ip
        camera.

        :return: FrameShow object
        """
        Thread(target=self.show, args=()).start()
        print('[FRAMESHOW START] Start')
        return self

    def show(self):
        """
        Constructs a stream to hold the image data and read the image
        data from the connection. The image data is received as byte-
        stream and has to be converted to an array containing the pixel
        information. The converted image is stored in the frame parameter
        of the FrameShow object.
        """
        print('[FRAMESHOW SHOW] Start image grabbing')

        cap = cv2.VideoCapture(0)

        data = b'' ### CHANGED
        payload_size = struct.calcsize("L") ### CHANGED


        while not self.stopped:
            # Retrieve message size
            while len(data) < payload_size:
                data += self.__connection.recv(4096)

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("L", packed_msg_size)[0] ### CHANGED

            # Retrieve all data based on message size
            while len(data) < msg_size:
                data += self.__connection.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Extract frame
            self.frame = pickle.loads(frame_data)


            #image_len = struct.unpack('<L', self.__connection.read(struct.calcsize('<L')))[0]
            #if not image_len:
                #break
            # Construct a stream to hold the image data and read the image
            # data from the connection
            #image_stream = io.BytesIO()
            #image_stream.write(self.__connection.read(image_len))
            # Rewind the stream and convert it via cv2
            #image_stream.seek(0)
            #file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
            #self.frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        """
        Deactivates the connection to the ip camera.
        """
        print('[FRAMESHOW STOP] Stop image grabbing')
        self.__connection.close()
        self.__server_socket.close()
        cv2.destroyAllWindows()
        self.stopped = True
