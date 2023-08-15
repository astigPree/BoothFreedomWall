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
        server.connect((ADDR, PORT))
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


class CustomSocket :
    __connection: socket.socket = None

    def __init__(self, client: socket.socket) :
        self.setSocket(client)

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


if __name__ == "__main__":
    client = CustomSocket(create_socket())

    while True:
        value = input("Transaction : ")
        client.send(eval(value))
        get = client.received()
        for key in get:
            if key == "9":
                print(f"Has A Next Value : {get['9']}")
            else:
                print("IDS : ", end='')
                for data in get[key]:
                    print(f"{data[0]} " , end="")
                print()
