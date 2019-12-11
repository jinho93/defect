#!/usr/local/bin/python3.6

from custodian.vasp.handlers import WalltimeHandler
from subprocess import *

command = "sbatch job_JH.sh"
Popen(command, shell=True)

h= WalltimeHandler(wall_time=36000,buffer_time=1000,electronic_step_stop=True)
#h.check()
#h.correct()

exit()

