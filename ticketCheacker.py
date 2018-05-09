import tkinter as tk
from tkinter import messagebox
import sqlite3
import Blockchain
import hashlib

DATABASE_PATH_DIR = './'
DATABASE_NAME = 'flights.db'

window = tk.Tk()
window.geometry('200x400')

labels = ['Name', 'Email', 'Birthday', 'Passport', 'FlightNO.', 'Time']
entries = {}
for lb in labels:
    tmp = tk.Label(window, text = lb)
    tmp.pack()
    entries[lb] = tk.Entry(window)
    entries[lb].pack()

def check():
    conn = sqlite3.connect(DATABASE_PATH_DIR + DATABASE_NAME)

    results = conn.execute('''SELECT addr FROM flights WHERE no='%s' AND time='%s' ''' % (entries['FlightNO.'].get(), entries['Time'].get()))

    results = list(results)

    if len(results) ==0 :
        messagebox.showinfo(title='Checked!', message='No flight found, please check!')
    else:
        hashvalue = ''.join([entries[key].get() for key in entries])
        hashvalue = hashlib.md5(hashvalue.encode('utf-8')).hexdigest()
        print(hashvalue)
        checked = 'Yes' if Blockchain.checkTicket(hashvalue, results[0][0]) else 'No'
        messagebox.showinfo(title='Checked!', message=  checked)

    conn.close()

bt = tk.Button(window, text = 'check', command = check, height = 10, width = 10)
bt.pack()

tk.mainloop()
