import Website
import Blockchain
import sqlite3
from flask import Flask, request
import os
from datetime import datetime

'''Load the database'''
DATABASE_PATH_DIR = './'
DATABASE_NAME = 'flights.db'

existedDB = DATABASE_NAME in os.listdir(DATABASE_PATH_DIR)
conn = sqlite3.connect(DATABASE_PATH_DIR + DATABASE_NAME)
if not existedDB:
    # Create table
    conn.execute('''CREATE TABLE flights
                 (no text, comp text, time text, from text, to text, price integer, volume integer, addr text, abi text)''')
    conn.commit()
conn.close()

'''APP Initial'''
app = Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def flightTable():
    return Website.flightTable_page(conn_path = DATABASE_PATH_DIR + DATABASE_NAME)

@app.route('/#',methods=['GET', 'POST'])
def backOnePage():
    return "<script>window.history.back(-1)</script>"