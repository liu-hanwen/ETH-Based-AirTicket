import sqlite3
from datetime import datetime
from jinja2 import Template
import Blockchain

TEMPLATES_PATH = './templates/'

def flightTable_page(conn_path):
    conn = sqlite3.connect(conn_path)
    results = conn.execute('''SELECT no, comp, from_, to_, time, price, addr from flights''')

    ans = []
    for result in results:
        print(result)
        no, comp, from_, to, time, price, addr = result
        volume = int(Blockchain.getVolume(addr))
        ans.append([no, comp, from_, to, time, price, volume, addr])
    # print(ans)
    if len(ans)==0:
        ans = [['NaN' for i in range(8)]]
        ans[0][-3] = 0
    with open(TEMPLATES_PATH + 'flightsTable.html', 'r') as f:
        with open(Blockchain.ABI_PATH, 'r') as ff:
            ret = Template(f.read()).render(flights_list = ans, abi = str(ff.read()))
    conn.close()
    return ret



