import os
import glob
import subprocess

def qsubFiles(path_to_input_dirs, pbs_name="mex.pbs"):
    os.chdir(path_to_input_dirs)
    directories = glob.glob("*")
    for i in directories:
        os.chdir(i)
        qsub = 'qsub %s' % pbs_name
        print(i, qsub)
        subprocess.call(qsub, shell=True)
        os.chdir("..")
qsubFiles('../inputs')