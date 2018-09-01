import sys
import socket
import subprocess
import time
import random
import select
import threading

class inconn:

    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.log_user = []
        self.log_msg = []

    def init_conn(self, server, port, user, oauth, channel): #Send packet to connect to server on port
        try: 
            self.s.connect_ex((server,port))
        except:
            print("Something went wrong...")
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            sys.exit()
        print("Connection Established")

        #Send username, password, and nickname information to server
        self.s.send(('USER ' + user + "\n").encode())
        self.s.send(('PASS ' + oauth + "\n").encode())
        self.s.send(('NICK ' + user + "\n").encode())

        #Joins a twitch irc channel
        self.s.send(('JOIN #' + channel + "\n").encode())
        data = self.s.recv(1024).decode()
        if ('Login authentication failed\r\n' in data) == True:
            print('Authentication Failed')
            self.s.shutdown(socket.SHUT_RDWR)
            self.s.close()
            sys.exit()
        else:
            print('Authentication Sucessful')
        message_temp = ("PRIVMSG #" + user +  " :" + 'Test' + "\n").encode()
        self.s.send(message_temp)
        print('Test Message is Sent!')

    def new_data(self):
        return select.select([self.s], [], [], 0)
    
    def getmsg(self): #Receives the data with a buffer rate of 4096 bytes , function returns a string (decoded from bytes of raw data) and its length
            data = self.s.recv(1024).decode()
            return data

    def verify_format_msg(self,buffer): # Verfies data type (console or message) and parses it to extract username and message, function returns string -> "user:message"
        
        def consolemsg(line): #Identifies if the received data is a console message
            if "PRIVMSG" in line:
                return True
            elif "tmi.twitch.tv" in line:
                return True
            else:
                return False
        
        for line in str.split(buffer,"\r\n"): #Finds messages to ignore, ping messages to "pong" back, or user messages to process
            if line == "":
                continue
            elif len(buffer) < 3:
                continue
            elif "PING" in buffer and consolemsg(buffer):
                self.s.send(("PONG tmi.twitch.tv\r\n").encode())
                user = 'ping'
                msg = 'pong'
            else:
                try:
                    col = str.split(buffer, ":", 2)
                    user = str.split(col[1], "!", 1)[0]
                    msg = str.split(col[2], "\r\n", 1)[0]
                except IndexError:
                    msg = ""
                    user = ""
        return user, msg

# class tallys:
#     def __init__(self, cmds):
#         self.cmds = cmds
#         self.cmd_list = []
#         for x in self.cmds:
#             for y in x:
#                 self.cmd_list.append(y)
#         self.tally = []

#     def vote(self, msg):
#         def filter1(msg):
#             if msg in self.cmd_list:
#                 return True
#             else:
#                 return False
        
#         msg_f = list(filter(filter1, msg))
#         print(msg_f)
        
#         catagories = []
#         for txt in msg_f:
#             for group in self.cmds:
#                 if txt in group:
#                     catagories.append(self.cmds.index(group))
#         #print(catagories)
#         if catagories == []:
#             voted = "null"
#             return voted
        
#         counter = []
#         for group in self.cmds:
#             count = 0
#             for num in catagories:
#                 if num == self.cmds.index(group):
#                     count = count + 1
#             counter.append(count)

#         print(counter)  
        
#         for x in counter:
#             x = x +  random.uniform(0, 1)
        
        
#         # voted_index = counter.index(max(catagories))
#         # voted = ("%s" % self.cmds[voted_index])
#         # return voted
        
#         # print(run_tab)
#         # self.tally[x] = self.tally[x] + random.uniform(0, 1)

class outconn:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    def init_conn(self, client, port):
        self.s.bind((client, port))
        self.s.listen(1)
        client, addr = self.s.accept()
        data ='Connected to Remote Server'.encode()
        client.send(data)
        return client

#Execution

def most_voted_input(msg):
    
    def filter1(msg):
        cmds = ['up', 'u', 'down', 'd', 'left', 'l', 'right', 'r']
        if msg in cmds:
            return True
        else:
            return False

    msg_f = list(filter(filter1, msg))

    cmd_u = msg_f.count('u') +  msg_f.count('up')
    cmd_d = msg_f.count('d') +  msg_f.count('down')
    cmd_l = msg_f.count('l') +  msg_f.count('left')
    cmd_r = msg_f.count('r') +  msg_f.count('right')

    array = [[cmd_u, 'up'],[cmd_d, 'down'],[cmd_l, 'left'], [cmd_r, 'right']]

    if [cmd_u, cmd_d, cmd_r, cmd_l] == [0,0,0,0]:
        return 'null'
    else:
        for x in array:
            x[0] = x[0] + random.uniform(0, 1)
        print(array)
        return max(array)[1]

def move_counter(vote, last_cmd, move_count, stream):
    if vote == 'up':
        move_count[1] = move_count[1] + 1 
    if vote == 'down':
        move_count[1] = move_count[1] - 1
    if vote == 'right':
        move_count[0] = move_count[0] + 1 
    if vote == 'left':
        move_count[0] = move_count[0] - 1

    if (move_count[0] == 19) or (move_count[0] ==  -1 ) or (move_count[1] == 19) or (move_count[1] == -1):
        if (vote != 'null'):
            message = ("PRIVMSG #" + user +  " :" + 'You shan\'t pass! Can\'t go ' + vote + '. Try again!'  + "\n").encode()
            stream.s.send(message)
        if vote == 'up':
            move_count[1] = move_count[1] - 1 
        if vote == 'down':
            move_count[1] = move_count[1] + 1
        if vote == 'right':
            move_count[0] = move_count[0] - 1 
        if vote == 'left':
            move_count[0] = move_count[0] + 1
        return 'null', vote
    else:
        return vote, vote

user = 'jwalker160930'
oauth = 'oauth:27fpxk004l9k5rquv4ignkyqhupqlj'
channel = 'jwalker160930'
in_server = 'irc.twitch.tv'
in_port = 6667

out_client = 'localhost'
out_port = 5000

timer = 5

twitch = inconn()
pi = outconn()

twitch.s.settimeout(timer)

pi_stream = pi.init_conn(out_client, out_port)
twitch.init_conn(in_server, in_port, user,oauth,channel)

move_count = [9,9]
last_cmd = ''
while True:
    init_time = time.time()
    while time.time()-init_time < timer:
        if twitch.new_data:
            try:
                data = twitch.getmsg()
                user, msg = twitch.verify_format_msg(data)
                twitch.log_user.append(user)
                twitch.log_msg.append(msg)
            except socket.timeout:
                break
    print(twitch.log_msg)
    vote = (most_voted_input(twitch.log_msg))
    voted, last_cmd = move_counter(vote, last_cmd, move_count, twitch)
    print(move_count)
    if voted == 'null':
        pass
    else:
        pi_stream.send(voted.encode())
    del twitch.log_msg[:]
    del twitch.log_user[:]