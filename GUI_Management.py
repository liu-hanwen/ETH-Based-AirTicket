import tkinter as tk
import tkinter.messagebox
import sqlite3
import Blockchain
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
                 (no text, comp text, time text, from_ text, to_ text, price integer, volume integer, addr text)''')
    conn.commit()
conn.close()

'''GUI PART'''

window = tk.Tk()
window.title('Manage System')
window.geometry('1200x500')

labels = ['No.', 'Company', 'Time', 'From', 'To', 'Price', 'Volume']
entries = {}

frm = tk.Frame(window)
frm.pack()
frm_r = tk.Frame(frm)
frm_r.pack(side = 'right')
frm_l = tk.Frame(frm)
frm_l.pack(side = 'left')


'''LEFT, NEW FLIGHT SUBMIT'''
for lb in labels:
    entries[lb] = tk.Entry(frm_l)

for key in entries:
    tmp = tk.Label(frm_l, text = key)
    tmp.pack()
    entries[key].pack()

flightsListBox = tk.Listbox(frm_r, height = 200, width = 100)
# flightsListBox.insert('end','No.\tCompany\tTime\tFrom\tTo\tVolume\tContract\t\tPrice')

def refresh():
    flightsListBox.delete(0,'end')
    conn = sqlite3.connect(DATABASE_PATH_DIR + DATABASE_NAME)
    for item in conn.execute('''SELECT * from flights'''):
        tmp_str = '%s\t%s\t%s\t%s\t%s\t%E\t\t%s\t\t%s' % (item[0], item[1], str(datetime.strptime(item[2], '%Y%m%d%H%M')), item[3], item[4], item[5], item[6],item[7])
        flightsListBox.insert('end', tmp_str)
    conn.close()


def submit():
    # print(','.join(([entries[key].get() for key in entries])))
    args = {}
    for key in entries:
        args[key] = entries[key].get()
    tkinter.messagebox.showinfo(title='New Flight', message=str(args))
    conn = sqlite3.connect(DATABASE_PATH_DIR + DATABASE_NAME)
    ret = Blockchain.newFlight_submit(conn, args=args)
    conn.close()
    tkinter.messagebox.showinfo(title='New Flight', message=str(ret))
    refresh()

bt = tk.Button(frm_l, text = 'Submit', command=submit, width=12, height = 5)
bt.pack()

'''RIGHT, FLIGHTS TABLE'''
refresh()
flightsListBox.pack()

tk.mainloop()
