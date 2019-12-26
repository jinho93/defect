#!/usr/local/bin/python3.6
from subprocess import Popen


f = open('vAtoms.dat', 'r')

"""
It is available to control the variations
"""
r_a = 12
r_b = 15
r_c = 26


total_list = []
L = []

for i in f :
    if len(i) == 1:
        continue
    else:
        tmp_list = list(map(float,i.strip().split()))
        #print(tmp_list)

        """
        Screening Wigner-Seiz cell from vAtoms.dat file
        """
        if tmp_list[4] >= 0 and tmp_list[4] <= r_a :
            if tmp_list[5] >= 0 and tmp_list[5] <= r_b :
                if tmp_list[6] >= 0 and tmp_list[6] <= r_c :

                    total_list = list(map(float,tmp_list))
                    L.append(total_list)
                    #print(total_list)
                else:
                    continue
            else:
                continue
        else:
            continue

aver_r = float(( r_a + r_b + r_c )/3)
aver_V_list = []
aver_V = 0

for i, row in enumerate(L):
    #print(row)
    if row[0] >= aver_r :
        aver_V_list.append(row[3])
        #print(row[3])
        aver_V += float(row[3])
    else:
        continue

aver_V = aver_V / len(aver_V_list)
print(aver_V)


"""
Write the .idx file
"""

ff = open("vAtoms.itx", 'w')
ff.write("IGOR" + '\n')
ff.write("WAVES/D " + "r_cell" + " " + "V_lon" + " " + "V_def_ref" + " "
             + "V_def_ref_lon" + " " + "x_para " + "y_para "+"z_para "+'\n')
ff.write("BEGIN"+'\n')

for line in L:
    ff.write(' '.join(list(map(str, line))) + '\n')
ff.write("END" + '\n')

ff.write("X Display /W=(-1285,63,-673,525) V_def_ref,V_lon vs r_cell" + '\n')
ff.write("X AppendToGraph V_def_ref_lon vs r_cell"+'\n')
ff.write("X ModifyGraph gFont=\"Times New Roman\",gfSize=28,width=453.543,height=340.157" + '\n')
ff.write("X ModifyGraph mode=3" + '\n')
ff.write("X ModifyGraph marker(V_lon)=5,marker(V_def_ref_lon)=6" + '\n')
ff.write("X ModifyGraph rgb(V_lon)=(0,0,65535),rgb(V_def_ref_lon)=(0,0,0)" + '\n')
ff.write("X ModifyGraph msize=5" + '\n')
ff.write("X ModifyGraph tick=2" + '\n')
ff.write("X ModifyGraph mirror=1" + '\n')
ff.write("X ModifyGraph standoff=0" + '\n')
ff.write("X ModifyGraph axThick=1.5" + '\n')
ff.write("X ModifyGraph axisOnTop=1" + '\n')
ff.write("X ModifyGraph btLen=10" + '\n')
ff.write("X ModifyGraph manTick(left)={0,1,0,0},manMinor(left)={0,50}" + '\n')
ff.write("X ModifyGraph manTick(bottom)={0,5,0,0},manMinor(bottom)={0,50}" + '\n')
ff.write("X SetAxis left -2,1" + '\n')
ff.write("X SetAxis bottom 0,25" + '\n')
ff.write("X	Legend/C/N=text0/J/F=0/B=1/A=MC/X=25.33/Y=-26.18 \"\\\\s(V_def_ref) \\\\f02V\\\\f00\\\\Bq/b\\\\M\\r\\\\s(V_lon) \\\\f02V\\\\f00\\\\BPC\\\\M\\r\\\\s(V_def_ref_lon) ∆\\\\f02V\\\\f00\\\\BPC,q/b\\\\M\""+'\n')