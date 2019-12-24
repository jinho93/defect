#!/usr/local/bin/python3.6

from custodian.vasp.handlers import WalltimeHandler
from subprocess import Popen
import os
import signal
import time

ppp = Popen(['mpirun -np 8 /home/jinho/programs/src/vasp.5.4.4_std/bin/vasp_std > stdout.log']
      , shell=True, stdin=None, stdout=None, stderr=None, close_fds=True, preexec_fn=os.setpgrp)

h= WalltimeHandler(wall_time=36000,buffer_time=1000,electronic_step_stop=True)

while True:
    if h.check():
        h.correct()
    time.sleep(100)

os.killpg(os.getpgid(ppp.pid), signal.SIGTERM)

exit()

