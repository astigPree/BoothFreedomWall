import socket
import time
import typing as tp
import json
import sys

ADDR = "localhost"
PORT = 45678

HEADER_SIZE = 40
STOP_FUNCTION_ACTIVITY = False


MOODS = ('moods/happy.png', 'moods/angry.png', 'moods/sad.png', 'moods/loved.png', 'moods/empty.png')

"""
    Database Data ;
        - id (int) 
        - post (string)
        - category (string) -> Sending (int)
        - nickname (string)
        - date_publish (string)
        - user_mood (string) -> Sending (int)

    Actions;
        Receiving Data :
            News Feed : { category (int) : last_id (int or None) }
            
        Sending Data : 
            News Feed : {   category (int) : [ ( id , post , nickname, date_publish , user_mood (int) ), ... ] 
                            has_a_next_data (int : 9 ) : boolean }
            Json Problem : { error ( string : 'j' ) : None }
"""

def get_hostpot_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This sends a UDP packet to a known server (Google's DNS server) to get the local address
        s.connect(('1.1.1.1', 80))
        hostpot_address = s.getsockname()[0]
    except socket.error:
        hostpot_address = None
    finally:
        s.close()
    
    print(f"Hostpot : {hostpot_address}")
    return hostpot_address


def create_socket() -> tp.Union[socket.socket, None] :
    try :
        HOTSPOT_ADDR = get_hostpot_address()
        if not HOTSPOT_ADDR:
        	raise socket.error("Can't Connect")
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((HOTSPOT_ADDR, PORT))
    except socket.error as what:
        return None
    return server


def received_data(client: socket.socket, packet: int) -> tp.Union[bytes, None] :
    try :
        while not STOP_FUNCTION_ACTIVITY :
            try :
                data: bytes = client.recv(packet)
            except BlockingIOError :
                if STOP_FUNCTION_ACTIVITY :
                    return None
            else :
                return data
    except socket.error :
        return None
    return None


def send_data(client: socket.socket, data: bytes, timing=30) -> bool :
    try :
        time.sleep(1 / timing)
        client.sendall(data)
    except socket.error :
        return False
    return True


class CustomSocket :
    __connection: tp.Union[socket.socket, None] = None

    def setSocket(self, connection: socket.socket) :
        self.__connection = connection
        self.__connection.setblocking(False)

    def received(self) -> tp.Union[None, tp.Dict, int] :
        header: bytes = received_data(self.__connection, HEADER_SIZE)
        if header is None or not header :
            return None
        bode_size = header.decode()
        body: bytes = received_data(self.__connection, int(bode_size))
        if body is None and not body :
            return None

        try :
            body: dict = json.loads(body.decode())
        except json.JSONDecodeError :
            return 104  # Its mean has a json error

        return body

    def send(self, data: tp.Any) -> bool :
        data = json.dumps(data).encode()
        body_size = sys.getsizeof(data)
        if not send_data(self.__connection, f"{body_size}".encode()) :
            return False
        if not send_data(self.__connection, data) :
            return False
        return True

    def close(self) :
        self.__connection.shutdown(socket.SHUT_RDWR)
        self.__connection.close()
        self.__connection = None


class AppNetworkHandler :
    conn = CustomSocket()
    closeApp = False  # Used to notify if the user want to stop activity
    hasSocket = False  # Used to check if it was connected to server
    hasConnectionError = False  # Trigger if it has connection error
    hasDataInterruption = False  # Trigger if it has data interruption

    receivedData: tp.Union[None, dict] = None  # Used for storing received data from server
    sendData: tp.Union[None, dict] = None  # Used for storing sending data to server

    def connectToServer(self) -> bool :
        connection = create_socket()
        if connection :
            self.conn.setSocket(connection)
            self.hasSocket = True
            self.hasConnectionError = False
            return True
        else :
            self.hasSocket = False
            return False

    def getReceivedData(self) -> dict :
        temp = self.receivedData
        self.receivedData = None
        return temp

    def sendDataToServer(self, data: dict) :  # Return False if the variable still has a data else True if None
        if self.sendData :
            return False
        self.sendData = data
        return True

    def sendDataToServerForce(self, data: dict) :
        self.sendData = data

    def shutdownActivities(self) :
        global STOP_FUNCTION_ACTIVITY
        STOP_FUNCTION_ACTIVITY = True
        self.closeApp = True
        self.conn.close()
        self.hasSocket = False

    def threadActivity(self) :
        while not self.closeApp :
            if self.hasSocket and self.sendData and not self.receivedData :
                if not self.conn.send(self.sendData) :
                    self.hasSocket = False
                    self.hasConnectionError = True
                    continue

                data = self.conn.received()
                if isinstance(data, int) :
                    self.hasDataInterruption = True
                elif isinstance(data, dict) :
                    self.hasDataInterruption = False
                    self.sendData = None
                    self.receivedData = data
                else :
                    self.hasSocket = False
                    self.hasConnectionError = True
                    continue

    def activity(self) :
        if self.hasSocket and self.sendData and not self.receivedData :
            if not self.conn.send(self.sendData) :
                self.hasSocket = False
                self.hasConnectionError = True

            data = self.conn.received()
            if isinstance(data, int) :
                self.hasDataInterruption = True
            elif isinstance(data, dict) :
                self.hasDataInterruption = False
                self.sendData = None
                self.receivedData = data
            else :
                self.hasSocket = False
                self.hasConnectionError = True

