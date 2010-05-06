#!/usr/bin/env python

import subprocess, sys, os
mtmenu_dir = os.path.join(os.path.dirname(__file__), 'mtmenu')


f = open('mtmenu/out.txt', 'w')
while True:
    proc = subprocess.Popen([sys.executable, 'main.py', '-p', 'default:tuio,0.0.0.0:6001'],
				cwd=mtmenu_dir, shell=False, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    
    stdout, stderr = proc.communicate()
    if stdout:
        f.write(stdout)
    f.write(20*"=")
    if stderr:
        f.write(stderr)
				
    #retval = proc.wait()
    #if retval == 0:
    #    break

f.close()