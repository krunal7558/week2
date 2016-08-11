#!/usr/bin/env python

from telnetlib
import time
from getpass import getpass
import socket
import sys

pynet_rtr1 = u'184.105.247.70'
COMMAND = ('show ip interface brief',)

TELNET_PORT = 23
TELNET_TIMEOUT = 6

class TN(Telnet):

    def __init__(self,ip_addr, TELNET_PORT=23, TELNET_TIMEOUT=6):
        try:
            return telnetlib.Telnet(ip_addr, TELNET_PORT, TELNET_TIMEOUT)
        except socket.timeout:
            sys.exit("Connection timed-out")

    def login(self, username, password):
        output = self.expect([r'[uU]sername:', r'[lL]ogin:'], TELNET_TIMEOUT)[2] #some router uses Login:
        self.write(username + '\n')
        if password:
            output += self.read_until('ssword:', TELNET_TIMEOUT)
            self.write(password + '\n')
        output += self.read_very_eager() #read eargely and display login process.
        return output

    def send_command(self, cmd):
        '''This function will send a command over telnet session and returns a string.'''
        cmd = cmd.strip()
        self.write(cmd + '\n')
        time.sleep(1)
        return self.read_very_eager()

    def __del__(self):
        '''desctructor to close telnet session.'''
        self.close()

if __name__ == "__main__":
    print "Telnet is not secure, but we will still going to use it"
    username = raw_input("Enter username : ")
    password = getpass()

    with TN(pynet_rtr1) as remote_conn:
        print remote_conn.login(username, password)
        time.sleep(1)
        remote_conn.send_command('term len 0')   # disable paging
        print remote_conn.send_command(COMMAND[0])
        time.sleep(6)

