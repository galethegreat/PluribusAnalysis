import os
import re
import sqlite3
import time

conn = sqlite3.connect('clean_hands.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS MrWhite ''')
cur.execute('''DROP TABLE IF EXISTS Gogo ''')
cur.execute('''DROP TABLE IF EXISTS Budd ''')
cur.execute('''DROP TABLE IF EXISTS Eddie ''')
cur.execute('''DROP TABLE IF EXISTS Bill ''')
cur.execute('''DROP TABLE IF EXISTS Pluribus ''')

cur.execute('''CREATE TABLE IF NOT EXISTS MrWhite
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Gogo
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Budd
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Eddie
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Bill
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Pluribus
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')

conn_1 = sqlite3.connect('raw_hands.sqlite')
cur_1 = conn_1.cursor()
cur_1.execute('SELECT max(id) FROM Hands' )
try:
    row = cur_1.fetchone()
    if row is None :
        last_id = 0
    else:
        last_id = row[0]
except:
    last_id = 0

ids = range(last_id)
print(ids)
ps_id = None

for id in ids:
    cur_1.execute('SELECT id, ps_id, rawhand FROM Hands WHERE id = ?', (id+1,) )
    row = cur_1.fetchone()
    ps_id = row[1]
    sRaw_hand_data = row[2]
    #sRaw_hand_data_nobrackets_re = re.findall('\[(.*)\]',sRaw_hand_data)
    #sRaw_hand_data_nobrackets = sRaw_hand_data_nobrackets_re[0]
    sRaw_hand_data = sRaw_hand_data.strip('[]')
    list_raw_hand_data = sRaw_hand_data.split(',')
    for line in list_raw_hand_data:
        line = line.strip()
        line = line.strip('\"')
        line = line.strip('\'')
        line = line.strip()
        line = line.rstrip('\\n')
        if not line.startswith('Dealt to '): continue

        if line.startswith('Dealt to Pluribus'):
            cur.execute('''INSERT OR IGNORE INTO Pluribus (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, line))
        elif line.startswith('Dealt to MrWhite'):
            cur.execute('''INSERT OR IGNORE INTO MrWhite (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, line))
        elif line.startswith('Dealt to Gogo'):
            cur.execute('''INSERT OR IGNORE INTO Gogo (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, line))



conn.commit()
cur.close()

cur_1.close()
