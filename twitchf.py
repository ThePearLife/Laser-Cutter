'''
TwitchStrip.py: Server End

Pi Communication Code by Noah S. Fuselier
Twitch IRC Communication Code by Shashwath S. Murthy
'''
import sys
import socket
import subprocess
import time
import random
import select
import itertools

def connecttoserver(s, server, port, user, oauth, channel): #Connects to server, returns intial data as string

    #Send packet to connect to server on port
    try: 
        s.connect_ex((server,port))
    except:
        print("Something went wrong...")
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        sys.exit()
    print("Connection Established")

    #Send username, password, and nickname information to server
    s.send(('USER ' + user + "\n").encode())
    s.send(('PASS ' + oauth + "\n").encode())
    s.send(('NICK ' + user + "\n").encode())

    #Joins a twitch irc channel
    s.send(('JOIN #' + channel + "\n").encode())
    data = s.recv(1024).decode()
    if ('Login authentication failed\r\n' in data) == True:
        print('Authentication Failed')
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        sys.exit()
    else:
        print('Authentication Sucessful')
    message_temp = ("PRIVMSG #" + user +  " :" + 'Test' + "\n").encode()
    s.send(message_temp)
    print('Test Message is Sent!')

def getmsg(s): #Receives the data with a buffer rate of 1024 bytes , function returns a string (decoded from bytes of raw data) and its length
    try:
        data = s.recv(1024).decode()
        length = len(str.split(data, ":", 2))
    except:
        data = ""
        length = len(str.split(data, ":", 2))
    return data, length

def verify_format_msg(buffer, length): # Verfies data type (console or message) and parses it to extract username and message, function returns string -> "user:message"
    
    def consolemsg(line): #Identifies if the received data is a console message
        if "PRIVMSG" in line:
            return True
        elif "tmi.twitch.tv" in line:
            return True
        else:
            return False
    
    for line in str.split(buffer,"\r\n"): #Finds messages to ignore, ping messages to "pong" back, or user messages to process
        #if line == "":
        #   continue
        #elif length < 3:
        #    continue
        if "PING" in buffer and consolemsg(buffer):
            s.send(("PONG tmi.twitch.tv\r\n").encode())
            user = 'ping'
            msg = 'pong'
            return user, msg
        else:
            try:
                col = str.split(buffer, ":", 2)
                user = str.split(col[1], "!", 1)[0]
                msg = str.split(col[2], "\r\n", 1)[0]
                user = user.lower()
                msg = msg.lower()
            except IndexError:
                user = ''
                msg = ''4
            print(type(user), type(msg))
        return user, msg

def log_append(s, log_user, log_msg):
    buffer, length = getmsg(s)
    print(buffer)
    user, msg = verify_format_msg(buffer, length)
    log_user.append(user)
    log_msg.append(msg)
    return buffer, length


def most_voted_input(msg):
    
    def filter1(msg):
        cmds = ['up', 'u', 'down', 'd', 'left', 'l', 'right', 'r']
        if msg in cmds:
            return True
        else:
            return False

    msg_f = list(filter(filter1, msg))
    print(msg_f)

    cmd_u = msg_f.count('u') +  msg_f.count('up')
    cmd_d = msg_f.count('d') +  msg_f.count('down')
    cmd_l = msg_f.count('l') +  msg_f.count('left')
    cmd_r = msg_f.count('r') +  msg_f.count('right')

    array = [[cmd_u, 'u'],[cmd_d, 'd'],[cmd_l, 'l'], [cmd_r, 'r']]

    if [cmd_u, cmd_d, cmd_r, cmd_l] == [0,0,0,0]:
        return 'null'
    else:
        for x in array:
            x[0] = x[0] + random.uniform(0, 1)
            return max(array)[1]

# Execution

user = 'jwalker160930'
oauth = 'oauth:27fpxk004l9k5rquv4ignkyqhupqlj'
channel = 'jwalker160930'
server = 'irc.twitch.tv'
port = 6667
timer = 10

topi_host = '169.254.122.248'
topi_port = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((topi_host, topi_port))

s.listen(1)

client, addr = s.accept()
data ='Connected to Remote Server'.encode()
client.send(data)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connecttoserver(s,server,port, user, oauth, channel)

log_user = []
log_msg = []

while True:
    init_time = time.time()
    while time.time()-init_time < timer:
        ready = select.select([s], [], [], 0.1)
        if ready[0]:
            buffer, length = log_append(s, log_user, log_msg)
            print(buffer)
    print log_msg
    if [log_msg[:]] == [[]]:
        print(most_voted_input(log_msg))
    else:
        print([log_msg[:]])
        print(most_voted_input(log_msg))
        argument = most_voted_input(log_msg)
        if argument == 'null':
            pass
        else:
            client.send(argument.encode())
        del log_msg[:]
        del log_user[:]
