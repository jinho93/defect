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