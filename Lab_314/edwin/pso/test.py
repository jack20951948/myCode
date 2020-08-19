import numpy as np

mons_append_24 = [5, 8, 10, 11, 13, 15, 19, 21]
mons_append_24.append(24)
for k in range(24):
    for m in range(len(mons_append_24)):
        if k >= mons_append_24[m]:
            continue
        else:
            print(k, m)
            break