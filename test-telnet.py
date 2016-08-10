#!/usr/bin/env python

import telnetlib
import time
from getpass import getpass
import socket
import sys

pynet_rtr1 = u'184.105.247.70'
COMMAND = ('show version',)

TELNET_PORT = 23
TELNET_TIMEOUT = 6

def send_command(remote_conn,cmd):
   cmd = cmd.strip()
   if remote_conn==None:
      return ''
   remote_conn.write(cmd+'\n')
   time.sleep(1)
   return remote_conn.read_very_eager()

def login(remote_conn,username,password):
   if remote_conn==None:
      return ''
   output = remote_conn.read_until('sername:',TELNET_TIMEOUT)
   remote_conn.write(username + '\n')
   if password:
      output += remote_conn.read_until('ssword:',TELNET_TIMEOUT)
      remote_conn.write(password+'\n')
   return output

if __name__=="__main__":
   print "Telnet is not secure, but we will still going to use it"
   username = raw_input("Enter username : ")
   password = getpass()

   try:
      remote_conn = telnetlib.Telnet(pynet_rtr1,TELNET_PORT,TELNET_TIMEOUT)
   except socket.timeout:
      print "Connection timedout"
      remote_conn=None
   print login(remote_conn,username,password)
   time.sleep(1)

   output=remote_conn.read_very_eager()
   print output

   send_command(remote_conn,'term len 0')
   print send_command(remote_conn,COMMAND[0])
   time.sleep(6)

   print "Closing connection"
   remote_conn.close()

