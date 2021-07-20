from operator import sub
import os
import glob
import subprocess
from typing import Tuple

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
    os.chdir(path_results)
    for i in resubmit:
        os.chdir(i)
        os.chdir('mexc')
        cmd = 'qsub mexc.pbs'
        subprocess.call(cmd, shell=True)
        os.chdir("..")
        os.chdir("..")
def fix_broken(resubmit, path_results='../results'):
    os.chdir(path_results)
    for i in resubmit:
        os.chdir(i)
        out_files = glob.glob("*.out*")
        out_completion = glob.glob("mex_o.*")
        if len(out_files) == 0 and len(out_completion) == 0:
            cmd = 'qsub mex.pbs'
            #print(os.getcwd(), cmd)
            #subprocess.call(cmd, shell=True)
        elif len(out_files) >= 1 and len(out_completion) == 1:
            cmd = 'touch name_o.o100000'
            #print(os.getcwd(), cmd)
            #subprocess.call(cmd, shell=True)
        else:
            os.chdir("mexc")
            out_files = glob.glob("*.out*")
            out_completion = glob.glob("mex_o.*")
            if len(out_files) == 0 and len(out_completion) == 0:
                cmd = 'qsub mexc.pbs'
                print(os.getcwd(), cmd)
                subprocess.call(cmd, shell=True)
            

        os.chdir("..")

def fix_mex(resubmit):
    os.chdir("../results")
    
    for i in resubmit:
        print(i)
        os.chdir(i)
        out_files = glob.glob("*.out*")
        out_completion = glob.glob("*_o*")
        len_file = len(out_files)
        len_complete = len(out_completion)
        #print("len_complete", len(out_completion), "len_outfiles", len(out_files))
        if len_complete > len_file:
            for i in range(len_complete-len_file):
                del_o = out_completion.pop()
                #subprocess.call("echo " + del_o, shell=True)
                print('rm %s' % del_o)
                subprocess.call("rm " + del_o, shell=True)
        elif len_complete < len_file:
            for i in range((len_file - len_complete)):
                create_o = "mex_o.o%s0000" % str(i+15)
                print('touch %s' % create_o)
                #subprocess.call("echo " + create_o, shell=True)
                subprocess.call("touch " + create_o, shell=True)
        os.chdir("..")

def fix_mexc(resubmit):
    os.chdir("../results")
    for i in resubmit:
        print(i)
        if os.path.exists(i+"/mexc"):
            os.chdir(i+"/mexc")
            
            out_files = glob.glob("*.out*")
            out_completion = glob.glob("mexc_o.*")
            len_file = len(out_files)
            len_complete = len(out_completion)
            #print("len_complete", len(out_completion), "len_outfiles", len(out_files))
            if len_complete > len_file:
                for i in range(len_complete-len_file):
                    del_o = out_completion.pop()
                    #subprocess.call("echo " + del_o, shell=True)
                    print('rm %s' % del_o)
                    subprocess.call("rm " + del_o, shell=True)
            elif len_complete < len_file:
                for i in range((len_file - len_complete)):
                    create_o = "mexc_o.o%s0000" % str(i+15)
                    print('touch %s' % create_o)
                    #subprocess.call("echo " + create_o, shell=True)
                    subprocess.call("touch " + create_o, shell=True)
            os.chdir("../..")
        else:
            print(i,'does not have mexc')
# Case 0:
"""
"TPA2_4b_2ea",
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
"""
# Case 1:
"""
"2ed_9b_3ea",
"TPA2_8b_1ea",
"7ed_9b_1ea",
"7ed_3b_2ea",
"5ed_15b_2ea",
"6ed_5b_1ea",
"3ed_14b_3ea",
"7ed_7b_1ea",
"2ed_12b_3ea",
"6ed_15b_2ea",
"1ed_12b_1ea",
"3ed_10b_2ea",
"6ed_7b_2ea",
"""
# Case 2:
"""
"3ed_14b_1ea",
"7ed_5b_2ea",
"1ed_1b_1ea",
"5ed_3b_1ea",
"5ed_16b_1ea",
"6ed_12b_2ea",
"7ed_12b_1ea",
"""

# Case 3:
"""
   "TPA2_7b_3ea",
    "TPA2_15b_3ea",
    "7ed_7b_3ea",
    "TPA2_5b_2ea",
    "TPA2_16b_1ea",
    "TPA2_4b_1ea",
    "TPA2_2b_2ea",
    "7ed_8b_1ea",
    "TPA2_12b_3ea",
    "TPA2_10b_2ea",
    "TPA2_11b_2ea",
    "TPA2_9b_1ea",
    "TPA2_1b_3ea",
    "TPA2_13b_3ea",
    "TPA2_3b_2ea",
    "TPA2_5b_1ea",
    "7ed_5b_1ea",
    "TPA2_6b_1ea",
    "TPA2_14b_1ea",
    "7ed_6b_1ea"
    "TPA2_12b_2ea",
    "TPA2_2b_3ea",
    "TPA2_10b_3ea",
    "TPA2_11b_3ea",
    "TPA2_3b_3ea",
    "TPA2_13b_2ea",
    "TPA2_15b_1ea",
    "TPA2_7b_1ea",
    "TPA2_14b_2ea",
    "7ed_6b_2ea",
    "TPA2_4b_3ea",
    "TPA2_16b_3ea",
    "7ed_4b_3ea",
    "TPA2_6b_2ea",
    "TPA2_8b_3ea",
    "TPA2_12b_1ea",
    "7ed_8b_3ea",
    "7ed_9b_3ea",
    "TPA2_13b_1ea",
    "TPA2_9b_3ea",
    "TPA2_1b_1ea",
    "TPA2_7b_2ea",
    "7ed_5b_3ea",
    "TPA2_5b_3ea",
    "7ed_7b_2ea",
    "TPA2_15b_2ea",

"""

# Case 4:
"""
    "7ed_11b_3ea",
    "TPA2_1b_2ea",
"""

resubmit = [ 
    ]

#broken_resubmit('../results')

fix_broken(resubmit)
#fix_mexc(resubmit)
#fix_mex(resubmit)