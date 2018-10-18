import utils
import client
import config
import string
import time

# Configuration
ircServer   = config.SERVER
portNumber  = config.PORT
channelName = config.CHAN

# Robot name
userName   = 'ROBOT-b03901116'
hostName   = 'My-Mac'
serverName = 'ntu.edu.tw'
realName   = 'Yen-Shi Wang'
nickName   = userName
loginMsg   = 'Hello! I am robot.'

# Start IRC connection
irc = client.IRCClient()
irc.connect(ircServer, portNumber)
irc.user(userName, hostName, serverName, realName)
irc.nick(nickName)
irc.join(channelName)
irc.privMsg(channelName, loginMsg)

# Command string
privMsgStr = 'PRIVMSG ' + channelName + ' :'
repeatCmd = privMsgStr + '@repeat '
convertCmd = privMsgStr + '@convert '
ipCmd = privMsgStr + '@ip '
helpCmd = privMsgStr + '@help'

# Loop
while(True):
    text = irc.receive()
    # print(text)
    
    if not irc.ping_pong(text):
        text = text[:-2]
        if text.find(repeatCmd) != -1:
            print(nickName + ' got @repeat command!')
            reply = text[text.find(repeatCmd) + len(repeatCmd):]
            print('Message : ' + reply)
            irc.privMsg(channelName, reply)
            
        elif text.find(convertCmd) != -1:
            print(nickName + ' got @convert command!')
            convStr = text[text.find(convertCmd) + len(convertCmd):]
            print('Number : ' + convStr)
            if len(convStr) > 2 and text.find(convertCmd + '0x') != -1 and all(c in string.hexdigits for c in convStr[2:]):
                reply = str(int(convStr, 16))
                irc.privMsg(channelName, reply)
            elif convStr.isdigit():
                reply = str(hex(int(convStr)))
                irc.privMsg(channelName, reply)

        elif text.find(ipCmd) != -1:
            print(nickName + ' got @ip command!')
            ans = []
            ip = text[text.find(ipCmd) + len(ipCmd):]
            print('IP : ' + ip)
            if len(ip) <= 20:
                if not ip.isdigit():
                    reply = '0'
                else:
                    ans = utils.validIP(ip)
                    reply = str(len(ans))
                irc.privMsg(channelName, reply)
                for valid_ip in ans:
                    irc.privMsg(channelName, valid_ip)
                    time.sleep(1)

        elif text.find(helpCmd) != -1:
            print(nickName + ' got @help command!')
            irc.privMsg(channelName, '@repeat <Message>')
            irc.privMsg(channelName, '@convert <Number>')
            irc.privMsg(channelName, '@ip <String>')
