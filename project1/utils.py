def inRange(num):
    val = int(num) <= 255 and int(num) >= 0
    notZer = str(int(num)) == num
    return val and notZer

def validIP(ip):
    ret = []
    for i in range(1,4):
        for j in range(1,4):
            for k in range(1,4):
                if (i + j + k < len(ip)):
                    if (inRange(ip[0:i]) and inRange(ip[i:i+j]) and inRange(ip[i+j:i+j+k]) and inRange(ip[i+j+k:])):
                        ret.append(ip[0:i] + '.' + ip[i:i+j] + '.' + ip[i+j:i+j+k] + '.' + ip[i+j+k:])
    return ret
