import os
import re
import sqlite3
import time

conn = sqlite3.connect('clean_hands.sqlite')
cur = conn.cursor()

players = ['Bill','Budd','Eddie','Gogo','Hattori','Joe','MrBlonde','MrBlue','MrBrown','MrOrange','MrPink','MrWhite','ORen','Pluribus']
players_and_ids = dict()
id = 1
for player in players:
    players_and_ids[player] = id
    id += 1

cur.execute('''DROP TABLE IF EXISTS Hands ''')
cur.execute('''DROP TABLE IF EXISTS Players ''')

cur.execute('''CREATE TABLE IF NOT EXISTS Hands
         (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, hand_dealt TEXT, player_id)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Players
         (id INTEGER UNIQUE, player TEXT)''')

for player in players_and_ids:
    print(( players_and_ids[player], player))
    cur.execute('''INSERT OR IGNORE INTO Players (id, player)
        VALUES ( ?, ?)''', ( players_and_ids[player], player))
conn.commit()

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
        player_line = line.split()
        player = player_line[2]

        #in case a player is not in the original list of players (ie new player)
        if player not in players:
            print(line)
            line = line.split()
            if line[2] not in list_of_users:
                list_of_users.append(line[2])

        else:
            cur.execute('''INSERT OR IGNORE INTO Hands (id, ps_id, hand_dealt,player_id)
                VALUES ( ?, ?, ?,?)''', ( id, ps_id, hand, players_and_ids[player]))



if len(list_of_users) > 0:print('New Players that need to be added to the list, check code:',list_of_users)
conn.commit()
cur.close()

cur_1.close()
