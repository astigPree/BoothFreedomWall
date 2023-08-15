import sqlite3
from datetime import datetime


def writeDataInDatabase( data : list[str, ...]):
    command = """
        INSERT INTO booth (post, category, nickname, date_publish , user_mood)
        VALUES (?, ?, ?, ? , ?)
    """
    conn = sqlite3.connect(DATABASE_FILENAME)
    cur = conn.cursor()
    cur.execute(command , data)
    conn.commit()
    conn.close()


def resetDatabase():
    command = f"DELETE FROM {DATABASE_TABLE}"
    conn = sqlite3.connect(DATABASE_FILENAME)
    cur = conn.cursor()
    cur.execute(command)
    conn.commit()
    conn.close()


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
        - date_publish (string) : Dec 17, 2001
        - user_mood (string) -> Sending (int)
"""

post = "Import the sqlite3 module."
category = CATEGORIES[0]
nickname = "gwapo345"
date_publish = datetime.now().strftime("%b %d, %Y")
user_mood = MOODS[4]

writeDataInDatabase( [post , category , nickname , date_publish , user_mood])
# resetDatabase()