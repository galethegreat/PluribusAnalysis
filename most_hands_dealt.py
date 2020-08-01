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
        list_of_formated_hands.append(str(hand_raw))
        list_of_formated_hands.append(str(hand_raw[3]+hand_raw[4]+' '+hand_raw[0]+hand_raw[1]))

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


total_hands_found_for_player = dict()
for player_search in players:
    for hand in hands:
        cur.execute('''SELECT Hands.hand_dealt,Hands.ps_id, Players.player
        FROM Hands JOIN Players ON Hands.player_id = Players.id
        WHERE Hands.hand_dealt = ? AND Players.player = ? ''', (hand ,player_search ))

        try:
            row = cur.fetchall()
            print('Number of %s found:'%hand, len(row))
            total_hands_found_for_player[player_search] = total_hands_found_for_player.get(player_search, 0) + len(row)
        except:
            print('Could not find any hands matching this input')
total_hands_found_for_player_sorted = list()
total_hands_found_for_player_sorted = sorted([(hands,player) for player, hands in  total_hands_found_for_player.items()], reverse = True )

print('\n')
most_hands,top_player = total_hands_found_for_player_sorted[0]

file_handle = open('most_hands_dealt.js','w')
file_handle.write('anychart.onDocumentReady(function() {\n')
file_handle.write('var data = {\n')
file_handle.write(' header: ["Player", "Number of Hands Dealt"],\n')
file_handle.write(' rows: [\n')
last_player_count = 0
for hand_total,player_search in total_hands_found_for_player_sorted:
    last_player_count += 1
    print('%d (%s) were dealt to %s ' %(hand_total,hand_search,player_search))
    if len(total_hands_found_for_player_sorted) >last_player_count:
        file_handle.write('["%s", %d],\n'%(player_search,hand_total))
    else:
        file_handle.write('["%s", %d]\n'%(player_search,hand_total))

file_handle.write(']}\n')
file_handle.write('var chart = anychart.column();\n')
file_handle.write('chart.data(data);\n')
file_handle.write('chart.title("Amount of (%s) dealt to players");\n' %(hand_search))
file_handle.write("chart.container('container');\n")
file_handle.write('chart.draw();\n')
file_handle.write('});\n')
print('\n')
print('Player with most (%s):' %(hand_search),  top_player,most_hands)

file_handle.close()
cur.close()
print('\ndone')
