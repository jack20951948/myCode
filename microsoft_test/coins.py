import os
try:
    t = int(input())
except:
    print("input error!")
    os._exit(0)
ans = list(range(t))
for i in range(t):
    condition = input().split()
    try:
        condition = list(map(int, condition))
    except:
        print("input error!")
        os._exit(0)
    if condition[0] > 1000 or condition[1] > 1000:
        print("input error!")
        os._exit(0)
    source = input().split()
    try:
        source = list(map(int, source))
    except:
        print("input error!")
        os._exit(0)
    source.sort()
    for soc in source:
        if soc > (pow(2,31) - 1):
            print("input error!")
            os._exit(0)
    if condition[0] != len(source):
        print("input error!")
        os._exit(0)
    money_left = condition[1]
    ans[i] = 0
    while money_left != 0:
        if source[-1] > money_left:
            if len(source) > 1:
                source.pop()
            else:
                ans[i] = -1
                money_left = 0
        else:
            money_left -= source[-1]
            ans[i] += 1
    # print(ans)
for an in ans:
    print(an)