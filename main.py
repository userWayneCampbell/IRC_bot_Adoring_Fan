import socket
import sys
import time
import random
import argparse

##
# IRC bot created for idlebot, simulates the Adoring Fan from Oblivion.
#
# Strike fear into your enemies
# Oblivion memes and dialog
#
# Author: Wayne Campbell
##

parser = argparse.ArgumentParser(description='Connect to irc with idlerpg')
parser.add_argument('server', type=str,
                    help='ip address for irc server')
parser.add_argument('password', type=str,
                    help='password for idlerpg')
parser.add_argument('-c','--channel', required=False, default='#irpg',
                    help='channel to connect to, default: #irpg')
parser.add_argument('-r','--register', required=False, action="store_true",
                    help='used to register a idlerpg character the first time')

# Parse arguments
parsed = parser.parse_args()

# Set Variables
server = parsed.server
channel = parsed.channel
botnick = "Adoring_Fan"

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "connecting to:"+server
irc.connect((server, 6667))
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :Hmmmm!\n")
irc.send("NICK "+ botnick +"\n")
time.sleep(5)
irc.send("JOIN "+ channel +"\n")
time.sleep(2)

# Register name
if parsed.register:
    irc.send("PRIVMSG idlerpg :REGISTER Adoring_Fan " + parsed.password + " Bosmer" + "\n")
    time.sleep(2)
irc.send("PRIVMSG idlerpg :LOGIN Adoring_Fan " + parsed.password + "\n")
time.sleep(10)

def print_random():
    s_rand = ["Yes, oh great and mighty Grand Champion? Is there something you need? Can I carry your weapon? Shine your boots? Backrub, perhaps?",
            "By Azura, by Azura, by Azura! It's the Grand Champion! I can't believe it's you! Standing here! Next to me!",
            "I once was an adventurer like you then I took an arrow in the knee",
            "I don't really think you can ever get rid of me, even if you wanted!",
            "Hey everyone, why don't you just logout and let CayneWambell get some alone idle time.",
            "You guys don't think you can really beat CayneWembell right?... right?",
            "I followed my Champion all the way from the Arena, I am the best companion alive!",
            "You could tell me to leave, maybe i'll just walk off a cliff or something, this is the only purpose I have found in life",
            "I am sworn to carry your burdens",
            "I don't care how many penalties I get, I just wanna tell the world how great CayneWambell is!",
            "I'm just so happy to be here, standing in the glory of CayneWambell!",
            "Does anyone here have any sweetrolls?",
            "I feel so alone, doesn't anyone else talk? We should be talking about how great CayneWambell is!"]
    irc.send("PRIVMSG " + channel + " :" + random.choice(s_rand) + "\n")

last_time = int(time.strftime("%H"))
try:
    while True:
        text=irc.recv(2040)
        print(text)

        if int(time.strftime("%H")) != last_time:
            last_time = int(time.strftime("%H"))
            print("new time:" + str(last_time))
            if last_time % 4 == 0:
                print_random()

        if text.find('PING') != -1:
            irc.send('PONG ' + text.split() [1] + '\r\n')
        if 'CayneWambell' in text:
            print("found")
            if 'lost' in text and text.count("CayneWambell") == 2:
                irc.send("PRIVMSG " + channel + " :CayneWambell is the greatest player alive, I fear the next time you face him in battle for you will surely lose" + "\n")
            if 'lost' in text and text.count("CayneWambell") == 1:
                irc.send("PRIVMSG " + channel + " :You should have never tried to beat CayneWambell, for I know he is the best" + "\n")
            if 'won' in text and text.count("CayneWambell") == 2:
                irc.send("PRIVMSG " + channel + " :CayneWambell is the greatest player alive, All bow down before his greatness" + "\n")
            if 'won' in text and text.count("CayneWambell") == 1:
                irc.send("PRIVMSG " + channel + " :How dare you strike down the great CayneWambell, he will be sure to remember this" + "\n")

except KeyboardInterrupt:
    print('rip')
