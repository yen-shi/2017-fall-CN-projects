from socket import *
from utils import *
import numpy as np
import argparse
import time

def parse():
    parser = argparse.ArgumentParser(description='CN_HW2 Agent')
    parser.add_argument('--loss_rate', type=float, default=0.2)
    parser.add_argument('--forwardIP', type=str, default='127.0.0.1')
    parser.add_argument('--forwardPort', type=int, default=6666)
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
    forwardIP       = args.forwardIP
    forwardPort     = args.forwardPort
    recordIP        = None
    recordPort      = None
    loss_rate       = args.loss_rate

    drop_num        = 0.0
    total_num       = 0.0

    serverSocket    = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind((serverIP, serverPort))
    print('Bind to {}:{}'.format(serverIP, serverPort))

    while (True):
        # Receive packet
        packet, clientAddress = serverSocket.recvfrom(4096)
        rcvpkt, correct = pkt_receive(packet)
        if correct:
            # Forward packet
            if not (clientAddress[0] == forwardIP and
                    clientAddress[1] == forwardPort):
                if recordIP == None:
                    recordIP = clientAddress[0]
                    recordPort = clientAddress[1]
                if rcvpkt[0] != -1:
                    print('get     data    #{}'.format(rcvpkt[0]))
                    total_num += 1
                    if np.random.uniform() > loss_rate:
                        serverSocket.sendto(packet, (forwardIP, forwardPort))
                        print('fwd     data    #%d,       loss rate = %1.4f' % (rcvpkt[0], drop_num / total_num))
                    else:
                        drop_num += 1
                        print('drop    data    #%d,       loss rate = %1.4f' % (rcvpkt[0], drop_num / total_num))
                else:
                    print('get     fin')
                    serverSocket.sendto(packet, (forwardIP, forwardPort))
                    print('fwd     fin')
            else:
                serverSocket.sendto(packet, (recordIP, recordPort))
                if rcvpkt[0] != -1:
                    print('get     ack     #{}'.format(rcvpkt[0]))
                    print('fwd     ack     #{}'.format(rcvpkt[0]))
                else:
                    print('get     finack')
                    print('fwd     finack')
                    break
        else:
            print('Get wrong data: ', rcvpkt)

if __name__ == '__main__':
    start_time = time.time()
    print('Start agent')
    args = parse()
    run(args)
    print('Elapsed time: %.6f s' % (time.time() - start_time))
