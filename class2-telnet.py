
#!/usr/bin/env python
import telnetlib
import time
from getpass import getpass
import socket
import sys

pynet_rtr1 = u'184.105.247.70'
COMMAND = ('show ip interface brief',)

TELNET_PORT = 23
TELNET_TIMEOUT = 6

class TN(object):
    def __init__(self, ip_addr, TELNET_PORT=23, TELNET_TIMEOUT=6):
        '''' constructor to initialise variables'''
        self.TELNET_PORT = TELNET_PORT
        self.TELNET_TIMEOUT = TELNET_TIMEOUT
        self.ip_addr = ip_addr

    def __enter__(self):
        try:
            self.conn = telnetlib.Telnet(self.ip_addr, self.TELNET_PORT, self.TELNET_TIMEOUT)
            return self
        except socket.timeout:
            sys.exit("Connection timed-out")

    def login(self, username, password):
        output = self.conn.expect([r'[uU]sername:', r'[lL]ogin:'], TELNET_TIMEOUT)
        print output
        output = output[2]
        self.conn.write(username + '\n')
        if password:
            output += self.conn.read_until('ssword:', TELNET_TIMEOUT)
            self.conn.write(password + '\n')
        output += self.conn.read_very_eager() #read eargely and display login process.
        return output

    def send_command(self, cmd):
        '''This function will send a command over telnet session and returns a string.'''
        cmd = cmd.strip()
        self.conn.write(cmd + '\n')
        time.sleep(1)
        return self.conn.read_very_eager()

    def __exit__(self, ip_addr, TELNET_PORT=23, TELNET_TIMEOUT=6):
        self.conn.close()

    def __del__(self):
        self.conn.close()

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

