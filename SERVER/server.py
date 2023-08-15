import os
import socket
import threading
import time
import typing as tp
import json
import sys
import uuid
import sqlite3

ADDR = "localhost"
PORT = 45678
MAX_LISTENER = 500

HEADER_SIZE = 40
SHUTDOWN_SERVER = False

DATABASE_FILENAME = "BOOTH FREEDOM WALL DATABASE.db"
DATABASE_TABLE = "booth"
D_COLS = ('id', 'post', 'category', 'nickname', 'date_publish', 'user_mood')
CATEGORIES = ('love', 'school', 'thoughts')
MOODS = ('happy', 'angry', 'sad', 'loved', 'empty')

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
            News Feed : { category (int) : [ id , ... ] }
            
        Sending Data : 
            News Feed : {   category (int) : [ ( id, post, category, nickname, date_publish, user_mood ) , ... ] 
                            has_a_next_data (int : 9 ) : boolean }
            Json Problem : { error ( string : 'j' ) : None }
"""


def create_socket() -> tp.Union[socket.socket, None] :
    try :
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ADDR, PORT))
    except socket.error :
        return None
    return server


def received_data(client: socket.socket, packet: int) -> tp.Union[bytes, None] :
    try :
        while not SHUTDOWN_SERVER :
            try :
                data: bytes = client.recv(packet)
            except BlockingIOError :
                if SHUTDOWN_SERVER :
                    return None
            else :
                return data
    except socket.error :
        return None


def send_data(client: socket.socket, data: bytes, timing=30) -> bool :
    try :
        time.sleep(1 / timing)
        client.sendall(data)
    except socket.error :
        return False
    return True


def getDataFromDatabaseBy(data: dict, limit=5, size_limit=760) -> dict :
    conn = sqlite3.connect(DATABASE_FILENAME)
    cur = conn.cursor()
    key = next(iter(data))  # Get the key of data dictionary

    query = f"SELECT * FROM {DATABASE_TABLE} WHERE id NOT IN ({', '.join('?' for _ in data[key])}) AND {D_COLS[2]}='{CATEGORIES[int(key)]}' LIMIT {limit + 1}"
    cur.execute(query, data[key])

    results = cur.fetchall()
    conn.close()

    if not len(results) :
        return {key: [], 9: False}

    print(results)

    total_bytes = 0
    sending = []
    for i in range(len(results)):
        total_bytes += sys.getsizeof(results[i])
        if total_bytes < size_limit :
            category = CATEGORIES.index(results[i][2])
            user_mood = MOODS.index(results[i][5])
            sending.append(
                ( results[i][0] , results[i][1] , category , results[i][3], results[i][4], user_mood)
            )
        if i+1 > limit:
            break

    return {key : sending, 9 : True if len(results) > limit else False}


class CustomSocket :
    __connection: socket.socket = None

    def __init__(self, client: socket.socket) :
        self.setSocket(client)

    def setSocket(self, connection: socket.socket) :
        self.__connection = connection
        self.__connection.setblocking(False)

    def received(self) -> tp.Union[None, tp.Dict , int] :
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
            return 104 # Its mean has a json error

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


class CustomServer :
    object_server: socket.socket = None
    clients: dict[str, CustomSocket] = {}

    def createServer(self) :
        self.object_server = create_socket()
        if not self.object_server :
            raise Exception("[!] Cant Create A Server ")

    def runServer(self) :
        self.createServer()
        print("[/] Done Creating Socket")

        try :
            self.object_server.listen(MAX_LISTENER)
            while not SHUTDOWN_SERVER :
                client, _ = self.object_server.accept()
                threading.Thread(target=self.threadAcceptUser, args=(client,)).start()
        except os.error as e :
            print(f"[!] Error : {e}")

    def threadAcceptUser(self, client: socket.socket) :
        user_id = str(uuid.uuid4())[:8]
        client = CustomSocket(client)
        self.clients[user_id] = client
        while not SHUTDOWN_SERVER :
            activity: tp.Union[None, dict[str, tp.Any]] = self.clients[user_id].received()
            if not activity :  # if None close the socket
                self.clients[user_id].close()
                del self.clients[user_id]
                break

            # Do some activity here !!!!!!
            if isinstance(activity , dict):
                data = self.userActivity(activity)
            else:
                data = {'j': None}

            if not self.clients[user_id].send(data=data) :  # if cant send ,close the socket
                self.clients[user_id].close()
                del self.clients[user_id]
                break

    def userActivity(self, action: dict[str, tp.Any]) -> dict :
        key: str = next(iter(action))

        if key.isdigit() :
            if len(CATEGORIES) > int(key) > -1 :
                return getDataFromDatabaseBy(action)

        return {'E' : None}  # 'E' Stand for ERROR




if __name__ == "__main__":
    CustomServer().runServer()
