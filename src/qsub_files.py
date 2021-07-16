from operator import sub
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
#qsubFiles('../inputs')

def broken_resubmit(path_results, resubmit):
    resubmit = [ "TPA2_4b_2ea",
    "7ed_6b_3ea",
    "TPA2_14b_3ea",
    "TPA2_6b_3ea",
    "TPA2_16b_2ea",
    "TPA2_8b_2ea",
    "TPA2_10b_1ea",
    "7ed_8b_2ea",
    "TPA2_2b_1ea",
    "TPA2_3b_1ea",
    "7ed_9b_2ea",
    "TPA2_11b_1ea",
    "TPA2_9b_2ea",
    "3ed_14b_1ea",
    "2ed_9b_3ea",
    "7ed_5b_2ea",
    "TPA2_7b_3ea",
    "TPA2_15b_3ea",
    "7ed_7b_3ea",
    "TPA2_5b_2ea",
    "TPA2_16b_1ea",
    "TPA2_4b_1ea",
    "TPA2_2b_2ea",
    "7ed_8b_1ea",
    "TPA2_12b_3ea",
    "TPA2_8b_1ea",
    "TPA2_10b_2ea",
    "TPA2_11b_2ea",
    "7ed_3b_2ea",
    "TPA2_9b_1ea",
    "TPA2_1b_3ea",
    "TPA2_13b_3ea",
    "7ed_9b_1ea",
    "TPA2_3b_2ea",
    "5ed_15b_2ea",
    "TPA2_5b_1ea",
    "6ed_5b_1ea",
    "7ed_5b_1ea",
    "1ed_1b_1ea",
    "TPA2_6b_1ea",
    "TPA2_14b_1ea",
    "7ed_6b_1ea",
    "TPA2_12b_2ea",
    "TPA2_2b_3ea",
    "TPA2_10b_3ea",
    "5ed_3b_1ea",
    "3ed_14b_3ea",
    "TPA2_1b_2ea",
    "7ed_11b_3ea",
    "TPA2_11b_3ea",
    "TPA2_3b_3ea",
    "TPA2_13b_2ea",
    "7ed_7b_1ea",
    "2ed_12b_3ea",
    "TPA2_15b_1ea",
    "TPA2_7b_1ea",
    "6ed_15b_2ea",
    "TPA2_14b_2ea",
    "7ed_6b_2ea",
    "TPA2_4b_3ea",
    "TPA2_16b_3ea",
    "5ed_16b_1ea",
    "7ed_4b_3ea",
    "TPA2_6b_2ea",
    "6ed_12b_2ea",
    "TPA2_8b_3ea",
    "TPA2_12b_1ea",
    "7ed_12b_1ea",
    "7ed_8b_3ea",
    "7ed_9b_3ea",
    "TPA2_13b_1ea",
    "TPA2_9b_3ea",
    "TPA2_1b_1ea",
    "TPA2_7b_2ea",
    "7ed_5b_3ea",
    "1ed_12b_1ea",
    "3ed_10b_2ea",
    "TPA2_5b_3ea",
    "6ed_7b_2ea",
    "7ed_7b_2ea",
    "TPA2_15b_2ea",]
    os.chdir(path_results)
    for i in resubmit:
        os.chdir(i)
        os.chdir('mexc')
        cmd = 'qsub mexc.pbs'
        subprocess.call(cmd, shell=True)
        os.chdir("..")
        os.chdir("..")
broken_resubmit('../results')