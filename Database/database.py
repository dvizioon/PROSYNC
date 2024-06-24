import sqlite3
from flask import g
from flask import Flask
import sys
import os
sys.path.append(".")
from Modules._readIni import LerINI

ini = LerINI(".INI","paths")
# print(ini)


from Database.schema import create_tables

app = Flask(__name__)
DATABASE = os.path.join(ini['database'], ini['name_db'])  


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        create_tables(DATABASE, ini['name_table'])  
        db.commit()

# init_db()
