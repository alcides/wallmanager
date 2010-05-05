#!/usr/bin/env python

import subprocess, sys, os
mtmenu_dir = os.path.join(os.path.dirname(__file__), 'mtmenu')

while True:
    proc = subprocess.Popen([sys.executable, 'main.py', '-p', 'default:tuio,0.0.0.0:6001'],
				cwd=mtmenu_dir)
    retval = proc.wait()
    if retval == 0:
        break
