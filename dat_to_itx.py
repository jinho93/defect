#!/usr/local/bin/python3.6
from numpy import loadtxt

##EDIT!!


VBM = float(input("VBM value :  "))

MAX = max(loadtxt('BAND.dat')[:, 2])

f = open('BAND.dat', 'r')
total_list = []
L = []
for i in f:

#read # and just pass!
    if i.strip()[0] == '#':
        if len(L) == 0:
            continue
        else:
            total_list.append(L)
            L = []
    else:
        tmp_list = list(map(float, i.strip().split()))
        ## edit to multiply const
        tmp_list[0] = '%.6f' % (tmp_list[0])
        tmp_list[1] = '%.10f' % (tmp_list[1] + VBM)
        tmp_list[2] = '%.6f' % (tmp_list[2] / MAX * 2)
        L.append(tmp_list)

if len(L) != 0:
    total_list.append(L)

ff = open("band" + ".itx", 'w')
ff.write("IGOR" + '\n')

for idx, L in enumerate(total_list):
    ff.write("WAVES/D" + " " + "b" + str(idx) + "_B" + " " + "b" + str(idx) + "_E" + " " + "b" + str(idx) + "_W" + '\n')
    ff.write("BEGIN" + '\n')

    for line in L:
        ff.write(' '.join(list(map(str, line))) + '\n')
    ff.write("END" + '\n')

    if idx == 0:
        ff.write("X Display /W=(57,45,452,253) " + "b" + str(idx) + "_E" + " vs " + "b" + str(idx) + "_B" + '\n')
        ff.write("X ModifyGraph zColor(b0_E)={b0_W,0," + "2" + ",Red,1}" + '\n')
    else:
        ff.write("X AppendToGraph " + "b" + str(idx) + "_E" + " vs " + "b" + str(idx) + "_B" + '\n')
        ff.write("X ModifyGraph zColor(" + "b" + str(idx) + "_E)={b" + str(idx) + "_W,0," + "2" + ",Red,1}" + '\n')
#  ff.write("X ModifyGraph rgb("+"b"+str(idx)+"_E"+")=(7,115,65418)"+'\n')
# Control color

ff.write("X ModifyGraph gFont=\"Times New Roman\",gfSize=24,width=255.118,height=340.157" + '\n')
ff.write("X ModifyGraph marker=19" + '\n')
ff.write("X ModifyGraph mrkThick=2,lsize=2,rgb=(0,0,65535)" + '\n')
ff.write("X ModifyGraph tick=2,mirror=1,axThick=2,standoff=0" + '\n')
ff.write("X SetAxis left -4,4" + '\n')
ff.write("X ModifyGraph axisOnTop=1" + '\n')
ff.write("X ModifyGraph zero(left)=8,zeroThick(left)=2" + '\n')
ff.write("X ModifyGraph btLen=10" + '\n')
ff.write("X ModifyGraph nticks(bottom)=4" + '\n')
ff.write("X ModifyGraph mode=3,marker=19,msize=1" + '\n')

ff.close()
