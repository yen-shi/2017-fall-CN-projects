from socket import *
from utils import *
import numpy as np
import argparse
import time
import pickle

def parse():
    parser = argparse.ArgumentParser(description='CN_HW2 Sender')
    parser.add_argument('source', type=str)
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
    filename        = args.source
    packet_size     = args.packet_size
    threshold       = args.threshold

    clientSocket    = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(0.01)
    print('Send data to {}:{}'.format(serverIP, serverPort))

    # Initializes window variables (upper and lower window bounds, position of next seq number)
    base        = 1
    nidx        = 0
    window      = np.array([1])
    time_out    = args.time_out

    # Send data
    fileOpen    = open(filename, 'rb') 
    done        = False
    lastackreceived = time.time()
    datas           = read_pkts(fileOpen, packet_size)
    fileOpen.close()
    oldSize     = 1

    while base != len(datas) + 1:
        # Send data in window
        if nidx < len(window):
            # Send packet
            # Ref: https://wiki.python.org/moin/UdpCommunication
            data = datas[window[nidx] - 1]
            clientSocket.sendto(pickle.dumps(data), (serverIP, serverPort))
            if data[0] == -1:
                print('send    fin')
            else:
                print('send    data    #{},       winSize = {}'.format(data[0], window.size))
            nidx += 1
        # Receipt of an ack
        try:
            packet, serverAddress = clientSocket.recvfrom(4096)
            rcvpkt, correct = pkt_receive(packet)
            if correct:
                if rcvpkt[0] == -1:
                    print('recv    finack')
                    base += 1
                    break
                else:
                    print('recv    ack     #{}'.format(rcvpkt[0]))
                    lastackreceived = time.time()
                    # Double window size
                    if rcvpkt[0] == base:
                        base += 1
                        if rcvpkt[0] == window[-1]:
                            oldSize = window.size
                            newSize = min(oldSize * 2, threshold) if oldSize < threshold else oldSize + 1
                            window = np.arange(base, base+newSize) 
                            nidx = 0
                    elif rcvpkt[0] == base - 1:
                        oldSize = window.size
                        window = np.arange(base, base+1) 
            else:
                print('Get wrong data: ', rcvpkt)
        # TIMEOUT                    
        except:
            if (time.time() - lastackreceived > time_out):
                threshold = max(int(oldSize) // 2, 1)
                print('time    out,              threshold = {}'.format(threshold))
                window = np.arange(base, base+1)
                data = datas[window[0] - 1]
                clientSocket.sendto(pickle.dumps(data), (serverIP, serverPort))
                if (data[0] != -1):
                    print('resnd   data    #{},       winSize = {}'.format(data[0], window.size))
                else:
                    print('resnd   fin')
                lastackreceived = time.time()

    clientSocket.close()

if __name__ == '__main__':
    start_time = time.time()
    print('Start transmission.')
    args = parse()
    run(args)
    print('File transmission success!')
    print('Elapsed time: %.6f s' % (time.time() - start_time))
