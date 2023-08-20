import sqlite3
from datetime import datetime


def writeDataInDatabase( data : list[str, ...] , table:str):
    command = f"""
        INSERT INTO {table} (post, category, nickname, date_publish , user_mood)
        VALUES (?, ?, ?, ? , ?)
    """
    conn = sqlite3.connect(DATABASE_FILENAME)
    cur = conn.cursor()
    cur.execute(command , data)
    conn.commit()
    conn.close()


def resetDatabase(table: str):
    command = f"DELETE FROM {table}"
    conn = sqlite3.connect(DATABASE_FILENAME)
    cur = conn.cursor()
    cur.execute(command)
    conn.commit()
    conn.close()

def createDatabase():
    conn = sqlite3.connect(DATABASE_FILENAME)
    cur = conn.cursor()

    command = """
        CREATE TABLE IF NOT EXISTS {table} ( 
            id INTEGER PRIMARY KEY, 
            post TEXT, 
            category TEXT, 
            nickname TEXT, 
            date_publish TEXT,
            user_mood TEXT
        )
    """

    for d_table in DATABASE_TABLE:
        cur.execute(command.format(table = d_table))

    conn.commit()
    conn.close()


DATABASE_FILENAME = "BOOTH FREEDOM WALL DATABASE.db"
DATABASE_TABLE = ("love_table" , "school_table" , "life_table" , "random_table")
D_COLS = ('id', 'post', 'category', 'nickname', 'date_publish', 'user_mood')
CATEGORIES = ('love', 'school', 'life' , 'random')
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

table = DATABASE_TABLE[0]
post = "Import the sqlite3 module."
category = CATEGORIES[0]
nickname = "gwapo345"
date_publish = datetime.now().strftime("%b %d, %Y")
user_mood = MOODS[4]

writeDataInDatabase( data = [post , category, nickname, date_publish, user_mood] , table=table)
# createDatabase()
