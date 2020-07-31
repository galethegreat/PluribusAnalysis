import os
import re
import sqlite3


poker_hand_text_files = list()
poker_hand_text_files = os.listdir('pokerhands/')
count = 0;
for text_file in poker_hand_text_files:
    print('Opening:',text_file)
    try:
        file_handle = open('pokerhands/'+text_file)
    except:
        print('Could not open:',text_file)
    for line in file_handle:
        if not line.startswith('Dealt to Pluribus'): continue
        print(line)
        count = count+ 1
print(count)
