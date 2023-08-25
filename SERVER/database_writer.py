import sqlite3
from datetime import datetime
import json


def writeDataInDatabase(data: list[str, ...], table: str) :
    command = f"""
        INSERT INTO {table} (post, category, nickname, date_publish , user_mood)
        VALUES (?, ?, ?, ? , ?)
    """
    conn = sqlite3.connect(DATABASE_FILENAME)
    cur = conn.cursor()
    cur.execute(command, data)
    conn.commit()
    conn.close()


def resetDatabase(table: str) :
    command = f"DELETE FROM {table}"
    conn = sqlite3.connect(DATABASE_FILENAME)
    cur = conn.cursor()
    cur.execute(command)
    conn.commit()
    conn.close()


def createDatabase() :
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

    for d_table in DATABASE_TABLE :
        cur.execute(command.format(table=d_table))

    conn.commit()
    conn.close()


def writeTruJsonFile(file='post_container.json') :
    with open(file, 'r') as jf :
        for obj in json.load(jf) :
            writeDataInDatabase(
                data=[obj['post'], obj['category'], obj['nickname'], obj['date_publish'], obj['user_mood']],
                table=obj['table']
            )

    with open(file, 'w') as jf :
        json.dump([], jf)


DATABASE_FILENAME = "BOOTH FREEDOM WALL DATABASE.db"
DATABASE_TABLE = ("love_table", "school_table", "life_table", "random_table")
D_COLS = ('id', 'post', 'category', 'nickname', 'date_publish', 'user_mood')
CATEGORIES = ('love', 'school', 'life', 'random')
MOODS = ('happy', 'angry', 'sad', 'loved', 'empty')
"""
    Database Data ;
        - id (int) 
        - post (string)
        - category (string) -> Sending (int)
        - nickname (string) 
        - date_publish (string) : Dec 17, 2001
        - user_mood (string) -> Sending (int)
    
    JSON FILE ;
        [ {'table' : str, 'post' : str, 'category' : str, 'nickname' : str, 'date_publish: str, 'user_mood' : str} , ...]
    
"""

table = DATABASE_TABLE[1]
post = "In this example, the get_last_child method retrieves the MDGridLayout widget using its id attribute (assuming you've assigned an id to the MDGridLayout). It then uses list indexing to get the last item in the children list of the MDGridLayout. The condition grid_layout.children checks if there are any children in the grid layout before attempting to access the last child. If there are children, the last child is printed to the console."
category = CATEGORIES[0]
nickname = "gwapo345"
date_publish = datetime.now().strftime("%b %d, %Y")
user_mood = MOODS[4]
