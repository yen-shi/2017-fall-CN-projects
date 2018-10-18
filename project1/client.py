import socket

class IRCClient:
    """A class for IRC client connection"""
    def __init__(self, verbose=True):
        self.ircSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.verbose = verbose
        
    def connect(self, host, port):
        self.ircSocket.connect((host, port))
        if (self.verbose):
            print ('<IRC> Build connection to "' + host + ':' + str(port) + '"')
        
    def send(self, msg):
        self.ircSocket.send(str.encode(msg))
        
    def ping_pong(self, text):
        msg = str.split(text)
        if len(msg) != 0 and msg[0] == 'PING':
            reply = 'PONG ' + msg[1] + '\n'
            irc.send(reply)
            return True
        else:
            return False
        
    def user(self, userName, hostName, serverName, realName):
        user = 'USER ' + userName + ' ' + hostName + ' ' + serverName + ' :' + realName + '\n'
        self.send(user)
        
    def nick(self, nickName):
        nick = 'NICK ' + nickName + '\n'
        self.send(nick)
        
    def join(self, channelName):
        joinChannel = 'JOIN ' + channelName + '\n'
        self.send(joinChannel)
        if (self.verbose):
            print ('<IRC> Join channel: "' + channelName + '"')
        
    def privMsg(self, channel, msg):
        privMsg = 'PRIVMSG ' + channel + ' :' + msg + '\n'
        self.send(privMsg)
        if (self.verbose):
            print ('<IRC> Sent message to "' + channel + '"')
            print ('<IRC> Message : "' + msg + '"')
        
    def receive(self):
        text = self.ircSocket.recv(1024)
        text = text.decode('utf-8')
        return text
