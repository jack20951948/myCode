import os
n = int(input())
num_str = input()
num_list = num_str.split()
if n != len(num_list):
    print("Input error!")
    os._exit(0)
total=0
for i in num_list:
    total += int(i)
print(total)
