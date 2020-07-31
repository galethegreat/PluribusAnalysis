import os
import re
import sqlite3
import time

conn = sqlite3.connect('clean_hands.sqlite')
cur = conn.cursor()

cur.execute('''DROP TABLE IF EXISTS Bill ''')
cur.execute('''DROP TABLE IF EXISTS Budd ''')
cur.execute('''DROP TABLE IF EXISTS Eddie ''')
cur.execute('''DROP TABLE IF EXISTS Gogo ''')
cur.execute('''DROP TABLE IF EXISTS Hattori ''')
cur.execute('''DROP TABLE IF EXISTS Joe ''')
cur.execute('''DROP TABLE IF EXISTS MrBlonde ''')
cur.execute('''DROP TABLE IF EXISTS MrBlue ''')
cur.execute('''DROP TABLE IF EXISTS MrBrown ''')
cur.execute('''DROP TABLE IF EXISTS MrOrange ''')
cur.execute('''DROP TABLE IF EXISTS MrPink ''')
cur.execute('''DROP TABLE IF EXISTS MrWhite ''')
cur.execute('''DROP TABLE IF EXISTS ORen ''')
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
cur.execute('''CREATE TABLE IF NOT EXISTS MrBlue
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS MrBlonde
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS MrPink
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS MrBrown
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS MrOrange
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Joe
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Hattori
        (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS ORen
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
ps_id = None
list_of_users = list()
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
        hand_line = line
        hand_re = re.findall('.*\[(.*)\]',hand_line)
        hand = hand_re[0]
        if line.startswith('Dealt to Gogo'):
        #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO Gogo (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        elif line.startswith('Dealt to Budd'):
        #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO Budd (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        elif line.startswith('Dealt to Eddie'):
        #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO Eddie (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        elif line.startswith('Dealt to Bill'):
        #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO Bill (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        elif line.startswith('Dealt to Pluribus'):
        #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO Pluribus (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        elif line.startswith('Dealt to MrBlue'):
        #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO MrBlue (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        elif line.startswith('Dealt to MrBlonde'):
            #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO MrBlonde (id, ps_id, hand_dealt)
                    VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        elif line.startswith('Dealt to MrPink'):
            #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO MrPink (id, ps_id, hand_dealt)
                    VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        elif line.startswith('Dealt to MrBrown'):
            #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO MrBrown (id, ps_id, hand_dealt)
                    VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        elif  line.startswith('Dealt to MrOrange'):
        #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO MrOrange (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        elif line.startswith('Dealt to Joe'):
    #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO Joe (id, ps_id, hand_dealt)
            VALUES ( ?, ?, ?)''', ( id, ps_id, hand))

        elif line.startswith('Dealt to Hattori'):
        #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO Hattori (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        elif line.startswith('Dealt to MrWhite'):
        #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO MrWhite (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        elif line.startswith('Dealt to ORen'):
        #    print(id, ps_id, line)
            cur.execute('''INSERT OR IGNORE INTO ORen (id, ps_id, hand_dealt)
                VALUES ( ?, ?, ?)''', ( id, ps_id, hand))
        else:
            print(line)
            line = line.split()

            if line[2] not in list_of_users:
                list_of_users.append(line[2])

print(list_of_users)
conn.commit()
cur.close()

cur_1.close()
