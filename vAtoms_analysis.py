#!/usr/local/bin/python3.6

from subprocess import check_output

############EDIT !!!################
#epsilon
e_xx = 11.069788
e_yy = 11.069852
e_zz = 11.711368
e_xy = 0.000001
e_xz = 0.000383
e_yz = 0.000809
###############
#encut eV
ENCUT = 500
#path of bulk
bulk_path = "/scratch/jinho/2_defect_postprocessing/1_ZnIn2S4/3_opt/z_bulk_supercell/"
############EDIT  !!!###############



CHARGE = float(input("charge value(the number of electron ex) -1 state  q= 1 electron: "))

# covert eV to Ry unit
ENCUT = ENCUT * 0.073498618

##must edit path!!!
check_output(f"diff {bulk_path}loop_1/POSCAR ../../loop_1/POSCAR > diff_defect.txt; exit 0;", shell=True)

diff = open("diff_defect.txt", 'r')
line_t = []
while True:
    line = diff.readline()
    if not line: break
    line_t.append(line)
diff.close()

line_t_L = line_t[-1]

#defect site D_x: x position, D_y: y position, D_z: z position
D_x = float(line_t_L.split()[1])
D_y = float(line_t_L.split()[2])
D_z = float(line_t_L.split()[3])


comand = f'sxdefectalign --ecut {ENCUT:0.4f} --gstep 0.00001 --beta 1 --gamma 1 --expnorm 0 --printRho --charge {CHARGE:0.0f} --tensor {e_xx:0.6f},{e_yy:0.6f},{e_zz:0.6f},{e_yz:0.6f},{e_xz:0.6f},{e_xy:0.6f} --center {D_x:0.4f},{D_y:0.4f},{D_z:0.4f} --relative --vref ../../1_scf/LOCPOT --vdef {bulk_path}/1_scf/LOCPOT --vasp >> out.log'



print (comand)

check_output(comand, shell=True)

##########################################################
############ sxdefectaling ###############################
##########################################################

##########################################################
############# postprocessing #############################
##########################################################

f = open('vAtoms.dat', 'r')

"""
It is available to edit the variations
r_a, r_b, and r_c are half of a, b, and c parameters in bohr unit, respectively.
defect_a, defect_b, and defect_c are the positions of defect (a,b,c) in bohr unit, respectively.
"""
r_a = 22.0701 / 2
r_b = 25.4848 / 2
r_c = 46.4438 / 2
defect_a = 0
defect_b = 0
defect_c = 46.4438 * 0.4128


total_list = []
aver_list = []
aver_L = []
total_L = []

for i in f :
    if len(i) == 1:
        continue
    else:
        tmp_list = list(map(float,i.strip().split()))
        #print(tmp_list)

        """
        Screening Wigner-Seiz cell from vAtoms.dat file
        Only use for cubic cells
        Wigner-Seiz cell:
        a - a' =< x =< a + a'
        b - b' =< y =< b + b'
        c - c' =< z =< c + c'
        a, b, and c  are the defect position in bohr unit
        a', b', and c' are the half of cell parameters in bohr unit
        ellipse_cell = (x-a)^2/a'^2 + (y-b)^2/b'^2 + (z-c)^2/c'^2 = 1 ; formula of ellipse
        ellipse_cell >= 1 
        """

        if tmp_list[4] >= defect_a - r_a and tmp_list[4] <= defect_a + r_a :
            if tmp_list[5] >= defect_b - r_b and tmp_list[5] <= defect_b + r_b :
                if tmp_list[6] >= defect_c - r_c and tmp_list[6] <= defect_c + r_c :

                    total_list = list(map(float,tmp_list))
                    total_L.append(total_list)
                    #print('total')
                    #print(total_list)

                    ellipse_cell = (tmp_list[4]-defect_a)**2/(r_a**2) \
                                   + (tmp_list[5]-defect_b)**2/(r_b**2) \
                                   + (tmp_list[6]-defect_c)**2/(r_c**2)
                    if ellipse_cell >= 1 :
                        aver_list = list(map(float,tmp_list))
                        aver_L.append(aver_list)
                        #print('average')
                        #print(aver_list)

                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            continue

aver_V_list = []
# aver_V is the align value (C value)
aver_V = 0

for i, row in enumerate(aver_L):
    #print(row)
    aver_V_list.append(row[3])
    #print(row[3])
    aver_V += float(row[3])

aver_V = aver_V / len(aver_V_list)
print(aver_V)


"""
Create the .idx file to plot all data including Wigner-Seiz cell
"""

ff = open("vAtoms.itx", 'w')
ff.write("IGOR" + '\n')
ff.write("WAVES/D " + "r_cell" + " " + "V_lon" + " " + "V_def_ref" + " "
             + "V_def_ref_lon" + " " + "x_para " + "y_para "+"z_para "+'\n')
ff.write("BEGIN"+'\n')

for line in total_L:
    ff.write(' '.join(list(map(str, line))) + '\n')
ff.write("END" + '\n')

ff.write("WAVES/D align_r align_potential" + '\n')
ff.write("BEGIN"+'\n')
ff.write("0 "+ str(aver_V)+'\n')
ff.write("100 "+str(aver_V) +'\n')
ff.write("END" + '\n')

ff.write("X Display /W=(-1285,63,-673,525) V_def_ref,V_lon vs r_cell" + '\n')
ff.write("X AppendToGraph V_def_ref_lon vs r_cell"+'\n')
ff.write("X AppendToGraph align_potential vs align_r"+'\n')
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
ff.write("X ModifyGraph lstyle(align_potential)=7,lsize(align_potential)=1.5,rgb(align_potential)=(21845,21845,21845), mode(align_potential)=0" +'\n')
ff.write("X ModifyGraph manTick(left)={0,1,0,0},manMinor(left)={0,50}" + '\n')
ff.write("X ModifyGraph manTick(bottom)={0,5,0,0},manMinor(bottom)={0,50}" + '\n')
ff.write("X SetAxis left -2,1" + '\n')
ff.write("X SetAxis bottom 0,25" + '\n')
ff.write("X TextBox/C/N=text1/F=0/B=1/A=MC \"\\\\f02C\\\\f00 = "+ str("%0.3f" %aver_V) +"\""+'\n')
ff.write("X Legend/C/N=text0/J/F=0/B=1/A=MC/X=25.33/Y=-26.18"
         + " \"\\\\s(V_def_ref) \\\\f02V\\\\f00\\\\Bq/b\\\\M\\r\\\\s(V_lon)"
         + " \\\\f02V\\\\f00\\\\BPC\\\\M\\r\\\\s(V_def_ref_lon) D\\\\f02V\\\\"
         + "f00\\\\BPC,q/b\\\\M\\r\\\\s(align_potential) align\""+'\n')