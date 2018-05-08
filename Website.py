import sqlite3
import os
from flask import render_template
from datetime import datetime
from jinja2 import Template

TEMPLATES_PATH = './templates/'

def newFlight_page():
    content = None
    with open(TEMPLATES_PATH + 'newFlight.html', 'r') as f:
        content = f.read()
    return content

def flightTable_page(conn):

    ans = conn.execute('''SELECT * from flights WHERE time>''' + datetime.now().strftime('%Y%m%d%H%M'))

    ret = None
    with open(TEMPLATES_PATH + 'flightsTable.html', 'r') as f: # 未完成
        Template(f.read()).render(flights_list = ans)

    return ret

# def flightDetail(conn, args):
#
#     '''Check args'''
#     try:
#         no = args['no']
#         comp = args['comp']
#         time = args['time']
#         price = int(args['price'])
#         volume = int(args['volume'])
#         from_ = args['from']
#         to = args['to']
#
#     except KeyError as e:
#         return str(e)
#
#     ret = None
#     with open(TEMPLATES_PATH + 'flightDetail.html', 'r') as f: # 未完成
#         Template(f.read()).render(flights_list = ans)
#

# def buyTicket(conn, args):
#


