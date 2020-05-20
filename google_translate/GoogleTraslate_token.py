import requests
import re
import json
import time

def getGoogleToken(a, TKK):
    def RL(a, b):
        for d in range(0, len(b)-2, 3):
            c = b[d + 2]
            c = ord(c[0]) - 87 if 'a' <= c else int(c)
            c = a >> c if '+' == b[d + 1] else a << c
            a = a + c & 4294967295 if '+' == b[d] else a ^ c
        return a

    g = []
    f = 0
    while f < len(a):
        c = ord(a[f])
        if 128 > c:
            g.append(c)
        else:
            if 2048 > c:
                g.append((c >> 6) | 192)
            else:
                if (55296 == (c & 64512)) and (f + 1 < len(a)) and (56320 == (ord(a[f+1]) & 64512)):
                    f += 1
                    c = 65536 + ((c & 1023) << 10) + (ord(a[f]) & 1023)
                    g.append((c >> 18) | 240)
                    g.append((c >> 12) & 63 | 128)
                else:
                    g.append((c >> 12) | 224)
                    g.append((c >> 6) & 63 | 128)
            g.append((c & 63) | 128)
        f += 1

    e = TKK.split('.')
    h = int(e[0]) or 0
    t = h
    for item in g:
        t += item
        t = RL(t, '+-a^+6')
    t = RL(t, '+-3^+b+-f')
    t ^= int(e[1]) or 0
    if 0 > t:
        t = (t & 2147483647) + 2147483648
    result = t % 1000000
    return str(result) + '.' + str(result ^ h)

if __name__ == "__main__":
    res = requests.get('https://translate.google.cn', timeout = 3)
    res.raise_for_status()
    result = re.search(r'tkk\:\'(\d+\.\d+)?\'', res.text).group(1)

    print("TKK: ", result)
    print("token: ", getGoogleToken('apple', result))