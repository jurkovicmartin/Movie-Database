from flask import g
import sqlite3


### CREATING DATABASE AND TABLE
# connection = sqlite3.connect("movies.db")
# connection.execute("""
# CREATE TABLE movies(
#              id     INTEGER     PRIMARY KEY     AUTOINCREMENT,
#              title  TEXT                    NOT NULL,
#              year   INT                     NOT NULL,
#              rating FLOAT                   NOT NULL
#              )
#              """)
# connection.close()

DATABASE = "movies.db"

def get_database():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


def close_database(exception=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()