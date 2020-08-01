# PluribusAnalysis
Python, SQL and JavaScript project to visualize hands dealt from Pluribus Hands

I have done a similar project to Dr.Chucks. In my project I look at data from poker hands played by Pluribus, Facebook's Poker AI Bot against top pros. The goal was to look at a data of all the hands played by this bot and other players, make a raw database with  raw_data.py, make a clean database with clean_data.py
 and then visualize from the clean data which player got dealt with how many of a specific user-inputted hand (ie How many times A A were dealt with each player) and then spit out a javascript file to visualize it in a bar graph.

Git repo: https://github.com/galethegreat/PluribusAnalysis (if you want to run, wrote instructions at the bottom, to see who got dealt most A A visualized just download the repo and open most_hands_dealt.html)

I have made a file called raw_data.py which creates a raw_hands.sqlite database which stores an id, PokerStars hand id and the raw hand text data. This is a restartable process, asking the user how many hands they would like to retrieve and storing every 50 hands to the DB. Since the actual data set is not too large, I wanted to practice and pretend like it was. I copied the folder of all the hand's text files (each file contains about 100 hands) and then pretended like those hands are coming from a server and would load them up, check to see if it was retrieved in the DB and then store them in the DB. In this example,  I really do NOT need a DB but I wanted to do it for practice.

clean_data.py cleans up the raw data and makes another database with 2 tables, Hands and Players. I could have done all of this in one table but I wanted to practice not replacing the Player's names over and over again and to try to practice the JOIN ON portion of SQL. The Hands table contains the id, ps_id (poker stars hand id, player_id (foreign key to link to players Table) and hand dealt with that player for that hand. Essentially it looks at the raw hand data and extracts what hand was dealt to each player and stores it in the DB. Players Table has id and players names, when JOIN ON Hands.player_id = Player.id you get the complete table.

For visualization, most_hands_dealt.py takes user input (for example: A A) and finds out how many times each player has been dealt with pocket Aces. It formats the hands for each permutation of suits (ie Ah Ac and then also Ac Ah, the c and h are shorthand for clubs and hearts, there are 4 suits hearts, clubs , diamonds and spades). Currently, I have not implemented all the possible hands to look up, you can look up any pocket pair by typing in: 2 2 or K K etc. You can also look for any specific hand like Queen of clubs and Jack of spades by typing in: Qc Js. I did NOT implement error checking or the ability to check for offsuit combos and suited combos (and total combos) just yet. Will add it soon. Once it finds from the DB and makes a histogram using the dictionary.get method and using the SQL code we learned in class (with JOIN ON and SELECT and then fetchall), it then writes to a most_hands_dealt.js file using this tutorial https://www.anychart.com/blog/2017/10/25/javascript-bar-chart-tutorial/ to visualize the data.

The most_hands_dealt.html file opens it. The uploaded file is the one to show which player got dealt Aces and how many times.

TO RUN:

(sqllite browser must be installed)

1) Clone or download repo: https://github.com/galethegreat/PluribusAnalysis  

2) Run raw_data.py, enter any number of hands you want to grab, there is only 10000 hands, type 10000 to get all the hands and press enter. (it will go very quickly, the hands are stored at poker hands folder locally and no internet connection is made to retrieve the data.)

3) Run clean_data.py

4) Run most_hands_dealt.py and input hand you want to see, ex: A A (only pocket pairs work 2 2, K K, T T, 9 9 etc and single combo hands: Qc Jc, Kh 5s etc at the moment)

5) Open most_hands_deal.html to visualize in the browser (works with chrome)
