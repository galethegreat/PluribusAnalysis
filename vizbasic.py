import os
import re
import sqlite3
import time

def hand_formater(hand_raw):
    list_of_formated_hands = list()
    if len(hand_raw) == 3:
        if hand_raw[0] == hand_raw[2]:
            print('\n 6 Combos of Pocket Pair:',hand_raw)
            list_of_formated_hands.append(str(hand_raw[0]+'d '+hand_raw[2]+'h'))
            list_of_formated_hands.append(str(hand_raw[0]+'d '+hand_raw[2]+'s'))
            list_of_formated_hands.append(str(hand_raw[0]+'h '+hand_raw[2]+'s'))
            list_of_formated_hands.append(str(hand_raw[0]+'d '+hand_raw[2]+'c'))
            list_of_formated_hands.append(str(hand_raw[0]+'h '+hand_raw[2]+'c'))
            list_of_formated_hands.append(str(hand_raw[0]+'c '+hand_raw[2]+'s'))
            list_of_formated_hands.append(str(hand_raw[0]+'h '+hand_raw[2]+'d'))
            list_of_formated_hands.append(str(hand_raw[0]+'s '+hand_raw[2]+'d'))
            list_of_formated_hands.append(str(hand_raw[0]+'s '+hand_raw[2]+'h'))
            list_of_formated_hands.append(str(hand_raw[0]+'c '+hand_raw[2]+'d'))
            list_of_formated_hands.append(str(hand_raw[0]+'c '+hand_raw[2]+'h'))
            list_of_formated_hands.append(str(hand_raw[0]+'s '+hand_raw[2]+'c'))
        else:
            print('\n 16 Combos of:',hand_raw)
    elif len(hand_raw) == 4:
        if hand_raw[2] == 'o':
            print('\n 12 Combos of offsuit:',hand_raw)

        else:
            print('\n 4 Combos of suited:',hand_raw)

    else:
        print('\n There is 1 exact combo of:',hand_raw)


    return list_of_formated_hands



conn = sqlite3.connect('clean_hands.sqlite')
cur = conn.cursor()

players = ['Bill','Budd','Eddie','Gogo','Hattori','Joe','MrBlonde','MrBlue','MrBrown','MrOrange','MrPink','MrWhite','ORen','Pluribus']
players_and_ids = dict()
id = 1
for player in players:
    players_and_ids[player] = id
    id += 1
hands = None
hand_search = input('What hand do you want to retrive?[A T,Tc Qs,AooQ,TssC,2 2]: ')
if len(hand_search) < 1: quit()
hands = hand_formater(hand_search)
print(hands)

player_search = input('What player do you want to retrive?')
if len(player_search) < 1: quit()

while player_search not in players:
    player_search = input('Player not found, re-enter player you want to retrive')
    if len(player_search) < 1: quit()
total_hands_found = 0
for hand in hands:
    cur.execute('''SELECT Hands.hand_dealt,Hands.ps_id, Players.player
    FROM Hands JOIN Players ON Hands.player_id = Players.id
    WHERE Hands.hand_dealt = ? AND Players.player = ? ''', (hand ,player_search ))

    try:
        row = cur.fetchall()
        print(row)
        print('Number of %s found:'%hand, len(row))
        total_hands_found = total_hands_found + len(row)
    except:
        print('Could not find any hands matching this input')
print('%d (%s) were dealt to %s ' %(total_hands_found,hand_search,player_search))

cur.close()
print('\ndone')
