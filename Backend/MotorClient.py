import socket


class MotorClient:

    def __init__(self, port):
        """
        Setup connection to raspberry
        """
        self.__server = socket.socket()
        self.__port = port
        
        self.__server.bind(('', self.__port))
        self.__server.listen(5)
        self.__c, self.__addr = self.__server.accept()
        print("[MOTOR CLIENT] Socket Up and running with a connection from ",self.__addr)


    def send_start(self):
        self.__c.send("Start".encode())

    def send_stop(self):
        self.__c.send("Stop".encode())

    def send_pwm(self, duty_cycle):
        self.__c.send(str(duty_cycle).encode())

    def close_connection(self):
        self.__c.close()