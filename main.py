import Website
import Blockchain
import sqlite3
from flask import Flask, request
import os
from datetime import datetime

'''Load the database'''
DATABASE_PATH_DIR = './'
DATABASE_NAME = 'flghts.db'

existedDB = DATABASE_NAME in os.listdir(DATABASE_PATH_DIR)
conn = sqlite3.connect(DATABASE_PATH_DIR + DATABASE_NAME)
if not existedDB:
    # Create table
    conn.execute('''CREATE TABLE flights
                 (no text, comp text, time text, from text, to text, price integer, volume integer, addr text, abi text)''')
    conn.commit()

'''APP Initial'''
app = Flask(__name__)


@app.route('newFlight')
def newFlight():
    if len(request.args.keys)==0:
        return Website.newFlight_page()
    else:
        return Blockchain.newFlight_submit(conn, request.args)

@app.route('flightTable')
def flightTable():
    return Website.flightTable_page(conn)