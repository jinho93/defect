#!/usr/local/bin/python3.6

f = open('vAtoms.dat', 'r')

total_list = []
L = []

for i in f:
    if i.strip()[0] == ' ':
        if len(L) == 0:
            continue
        else:
            total_list.append(L)
            L = []
    else:
        tmp_list = list(map(float, i.strip().split()))

print(tmp_list)