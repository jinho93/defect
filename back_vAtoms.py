
log_2 = open('out.log', 'r')
line_log_2 = []

while True:
    line_2 = log_2.readline()
    if not line_2: break
    line_log_2.append(line_2)
log_2.close()

corr_E = line_log_2[-1].split()[3]
print("Defect correction (eV): " + corr_E)