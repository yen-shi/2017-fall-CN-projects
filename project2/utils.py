import hashlib
import pickle

def pkt_receive(pkt):
    rcvpkt = pickle.loads(pkt)
    c = rcvpkt[-1]
    del rcvpkt[-1]
    h = hashlib.sha256()
    h.update(pickle.dumps(rcvpkt))
    correct = (c == h.digest())
    return rcvpkt, correct

# Create packet(seqnum,data,checksum)
# Ref: https://www.devdungeon.com/content/working-binary-data-python
#      https://docs.python.org/3/library/hashlib.html
#      https://docs.python.org/3/library/pickle.html
#      https://wiki.python.org/moin/UdpCommunication
#      https://stackoverflow.com/questions/7107075/sending-and-receiving-arrays-via-sockets
def pkt_send(num, data=None):
    if data == None:
        sndpkt = [num]
    else:
        sndpkt = [num, data]
    h = hashlib.sha256()
    h.update(pickle.dumps(sndpkt))
    sndpkt.append(h.digest())
    return sndpkt

def read_pkts(fileOpen, packet_size):
    dataNum = 1
    datas = []
    while True:
        data = fileOpen.read(packet_size)
        if data:
            datas.append(pkt_send(dataNum, data))
            dataNum += 1
        else:
            datas.append(pkt_send(-1))
            break
    return datas
