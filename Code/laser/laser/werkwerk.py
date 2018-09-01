'''
TwitchStrip.py: Client End

Server Communication Code by Noah F. Fuselier
Hardware Implementation by Anant Kanungo
'''

import socket
import select
import subprocess
import time
import RPi.GPIO as GPIO
include time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(17,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

GPIO.setup(2,GPIO.OUT)
GPIO.setup(14,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)

GPIO.setup(9,GPIO.OUT)
GPIO.setup(10,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)

GPIO.setup(1,GPIO.OUT)

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

host = 'localhost'
port = 5000
buff = 1024

addr = ((host, port))
s.connect(addr)


print(s.recv(buff).decode())
s.send('Connection Established'.encode())

x = [17,18,22,23]
xn = [2,14,4,3]
y = [9,10,11,25]

xcoord = 0
ycoord = 0

pxcoord = 0
pycoord = 0
d = 0


msg = ''
while True:
    ready = select.select([s], [], [], 0.1)
    if ready[0]:
        msg = s.recv(buff).decode()
        #subprocess.run('c.exe', '-d' + msg) #place holder for Anant's file
    if not msg:
        pass
    else:
        print(msg + '\n')
        '''
        if msg = 'u':
            ycoord = ycoord + 1
            d = 1
            GPIO.output(ycoord%4,GPIO.HIGH)
            GPIO.output((ycoord-d)%4,GPIO.LOW)
        elif msg = 'd':
            ycoord = ycoord - 1
            d = -1
            GPIO.output(ycoord%4,GPIO.HIGH)
            GPIO.output((ycoord-d)%4,GPIO.LOW)
        elif msg = 'l':
            xcoord = xcoord - 1
            d = -1
            GPIO.output(xcoord%4,GPIO.HIGH)
            GPIO.output((xcoord-d)%4,GPIO.LOW)
        elif msg = 'r':
            xcoord = xcoord + 1
            d = 1
            GPIO.output(xcoord%4,GPIO.HIGH)
            GPIO.output((xcoord-d)%4,GPIO.LOW)
            '''
    msg = ''

