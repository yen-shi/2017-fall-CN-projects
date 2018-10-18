from socket import *
from utils import *
import argparse
import time
import pickle

def parse():
    parser = argparse.ArgumentParser(description='CN_HW2 Receiver')
    parser.add_argument('dest', type=str)
    parser.add_argument('--buffer_size', type=int, default=32)
    try:
        from argument import add_arguments
        parser = add_arguments(parser)
    except:
        pass
    args = parser.parse_args()
    print('Argument list:')
    print(args)
    return args

def run(args):
    # Set configurations
    serverIP        = args.IP
    serverPort      = args.Port
    filename        = args.dest
    packet_size     = args.packet_size
    buffer_size     = args.buffer_size

    serverSocket    = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((serverIP, serverPort))
    print('Bind to {}:{}'.format(serverIP, serverPort))

    # Initializes packet variables 
    expectedseqnum = 1
    ACK = 1
    ack = []
    dataBuf = []
    
    # RECEIVES DATA
    fileOpen = open(filename, 'wb')
    lastpktreceived = time.time()	

    while (True):
        # Receive packet
        rcvpkt = []
        packet, clientAddress = serverSocket.recvfrom(4096)
        rcvpkt, correct = pkt_receive(packet)
        lastpktreceived = time.time()
        if correct:
            if (rcvpkt[0] == expectedseqnum and len(dataBuf) != buffer_size):
                print('recv    data    #{}'.format(expectedseqnum))
                dataBuf.append(rcvpkt[1])
                sndpkt = pkt_send(expectedseqnum)
                serverSocket.sendto(pickle.dumps(sndpkt), (clientAddress[0], clientAddress[1]))
                print('send    ack     #{}'.format(expectedseqnum))
                expectedseqnum += 1
            elif (rcvpkt[0] == -1):
                print('recv    fin')
                sndpkt = pkt_send(-1)
                serverSocket.sendto(pickle.dumps(sndpkt), (clientAddress[0], clientAddress[1]))
                print('send    finack')
                break
            else:
                print('drop    data    #{}'.format(rcvpkt[0]))
                sndpkt = pkt_send(expectedseqnum-1)
                serverSocket.sendto(pickle.dumps(sndpkt), (clientAddress[0], clientAddress[1]))
                print('send    ack     #{}'.format(expectedseqnum-1))
                if len(dataBuf) == buffer_size:
                    print('flush')
                    for data in dataBuf:
                        fileOpen.write(data)
                    dataBuf = []
        else:
            print('Get wrong data: ', rcvpkt)
    if len(dataBuf) != 0:
        print('flush')
        for data in dataBuf:
            fileOpen.write(data)
        dataBuf = []
    fileOpen.close()
    
if __name__ == '__main__':
    start_time = time.time()
    print('Start transmission.')
    args = parse()
    run(args)
    print('File transmission success!')
    print('Elapsed time: %.6f s' % (time.time() - start_time))
