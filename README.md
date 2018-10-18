# 2017 Fall Computer Network Projects

## [Project 1](project1)
An IRC robot that provides some commands for users.

Install `irssi` from irssi.org and run
```
➜  irssi -c irc.freenode.net -p 6667
```

There are some commands in `irssi`:
`/CONNECT`, `/JOIN`, `/NICK`, `/PRIVMSG`, `/USER`

It was tested under Python3.6.2.  
Run `python main.py` in `project1` and use `irssi` to join same channel.  
The IRC robot provides four commands: `@help`, `@repeat`, `@ip`, `@convert`.  

## [Project 2](project2)
Simulation of Go-Back-N and Congestion Control Protocol

There are three files under `project2`:
1. Sender.py: Send a file through UDP with some policies to the Agent.
2. Agent.py: Drop some packets and pass the remaining packets to Receiver.
3. Receiver.py: Store received pakcets got from Agent.

Here are the example commands, and use `-h` to see more options for each program:
```
➜  python Agent.py --Port 2000                 
➜  python Receiver.py data/dest.txt
➜  python Sender.py data/source.txt --Port 2000
```
