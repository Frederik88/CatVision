import socket
import sys

from CameraControl import CameraControl
from ImageStream import ImageStream

ip = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket()
s.connect((ip, port))

print("[SERVER] Connected with ", str(ip), ":", str(port))

camera = CameraContol()

while True:
    camera_data = s.recv(1024).decode()
    
    if(camera_data == "Start"):
        camera.start_capture()
        s.send("Pi Motor started".encode())
      
s.close()
