import os
import re
import sqlite3
import time

conn = sqlite3.connect('raw_hands.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Hands
    (id INTEGER UNIQUE, ps_id INTEGER UNIQUE, rawhand TEXT)''')

poker_hand_text_files = list()
poker_hand_text_files = os.listdir('pokerhands/')

enough_hands_reached = None
sql_id = 1
first_line_flag = 0
raw_hand_info = list()
psid_and_rawhand = dict()
ps_id = None
hands_retrieved = 0
start = None
cur.execute('SELECT max(id) FROM Hands' )
try:
    row = cur.fetchone()
    if row is None :
        start = 0
    else:
        start = row[0]
except:
    start = 0

if start is None : start = 0
ps_start_id = None
many = 0
found_ps_id = None

if ( many < 1 ) :
    conn.commit()
    sval = input('How many hands?:')
    if ( len(sval) < 1 ) :
        print('\nDone\n')
        quit()
    many = int(sval)

cur.execute('SELECT ps_id FROM Hands')
try:
    ps_sql_ids= cur.fetchall()
    print(ps_sql_ids)
except:
    ps_sql_ids = None

start = start + 1
cur.execute('SELECT id FROM Hands WHERE id=?', (start,) )
try:
    row = cur.fetchone()
    if row is not None :
        print('Quitting')
        quit()
        #continue
except:
    row = None


for text_file in poker_hand_text_files:

    print('\nOpening:',text_file)

    try:
        file_handle = open('pokerhands/'+text_file)
    except:
        print('Could not open:',text_file)

    print('\nGetting Hand Data for:',text_file)
    for line in file_handle:
        if line.startswith('PokerStars Hand #'):
            ps_id_re = re.findall('PokerStars Hand #(.*?):' , line)
            ps_id = int(ps_id_re[0])

            cur.execute('SELECT ps_id FROM Hands WHERE ps_id=?', (ps_id,) )
            try:
                row = cur.fetchone()
                if row is not None :
                    print('Found in database #', ps_id)
                    found_ps_id = True
                else:

                    found_ps_id = False
                    #continue
            except:
                found_ps_id = False


        if line == '\n' and not found_ps_id:
            first_line_flag += 1
            if first_line_flag > 1:
                first_line_flag = 0

                psid_and_rawhand[ps_id] = raw_hand_info
                cur.execute('''INSERT OR IGNORE INTO Hands (id, ps_id, rawhand)
                VALUES ( ?, ?, ?)''', ( start, ps_id, str(psid_and_rawhand[ps_id])))
                raw_hand_info = []
                many = many - 1
                start += 1
                hands_retrieved += 1
                if hands_retrieved % 50 == 0:
                    print('Saving 50 hands to database')
                    #time.sleep(2)
                    conn.commit()
                print('Hands left to collect:',many)
                if ( many < 1 ) :
                    conn.commit()
                    print('Reached Enough Hands')
                    enough_hands_reached = True
                    break
        else:
            if found_ps_id == True:
                continue

            raw_hand_info.append(line)

    file_handle.close()
    if enough_hands_reached is True:
        break



print('\nFinal commit to database')
conn.commit()

conn.commit()
cur.close()

print('\nDone\n')
