#!/usr/local/bin/python3.6

from custodian.vasp.handlers import WalltimeHandler
from subprocess import *

command = "sbatch job_JH.sh"
Popen(command, shell=True)

h= WalltimeHandler(wall_time=36000,buffer_time=1000,electronic_step_stop=True)

import time
while True:
    if h.check():
        h.correct()
    time.sleep(100)

#h.check()
#h.correct()

exit()

