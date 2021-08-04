from operator import sub
import os
import glob
import subprocess
from typing import Tuple
import json

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

def qsub(path='.'):
    resetDirNum = len(path.split("/"))
    if path != '.':
        os.chdir(path)
    pbs_file = glob.glob("*.pbs")[0]
    cmd = 'qsub %s' % pbs_file
    print(os.getcwd(), "cmd", cmd)
    failure = subprocess.call(cmd, shell=True)
    if path != '.':
        for i in range(resetDirNum):
            os.chdir("..")


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

def fix_mexc(resubmit, base_dir='mexc', baseName='mexc'):
    os.chdir("../results")
    for i in resubmit:
        print(i)
        if os.path.exists("%s/%s" % (i, base_dir)):
            os.chdir("%s/%s" % (i, base_dir))
            
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
                    create_o = "mexc_o.o%s0000" % str(i+15)
                    print('touch %s' % create_o)
                    #subprocess.call("echo " + create_o, shell=True)
                    subprocess.call("touch " + create_o, shell=True)
            os.chdir("../..")
        else:
            print(i,'does not have mexc')
def failed_gathered_excitations(failed, dirs_to_check, qsubFailed1=False, path_results='../results'):
    os.chdir(path_results)
    complete_dict = {}
    for i in failed:
        os.chdir(i)
        # 0 if no dir, 1 if out file, 2 if cannot read out
        local_lst = []
        for j in dirs_to_check:
            local = {}
            if not os.path.exists(j):
                local[j] = 0
            else:
                if not os.path.exists("%s/%s" % (j, 'mexc.out')):
                    local[j] = 1
                    if qsubFailed1:
                        qsub("%s" % j)
                else:

                    out_files = len(glob.glob("%s/*.out*" % j))
                    out_completion = len(glob.glob("%s/*_o*" % j))
                    if out_files <= out_completion and out_files > 0:
                        local[j] = 3
                    else: 
                        local[j] = 2 
            local_lst.append(local)
        complete_dict[i] = local_lst
        os.chdir("..")
    os.chdir("../src")
    #print(complete_dict)
    data = json.dumps(complete_dict, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    print(os.getcwd())
    with open('exc.json', 'w') as fp:
        fp.write(data)
        #fp.write("end")
    #print(data)
    #print(json.dumps(complete_dict, default=lambda o: o.__dict__,
    #       sort_keys=True, indent=4))


if __name__ == "__main__":
    resubmit = [ 
        ]
    #broken_resubmit('../results')
    
    #fix_broken(resubmit)
    #fix_mexc(resubmit)
    #fix_mex(resubmit)
    failed = ['7ed_5b_2ea', '7ed_1b_3ea', '3ed_1b_3ea']

    #dirs_to_check = ['mexc', 'bhandhlyp', 'pbe1pbe']
    #fix_mexc(failed)
    #failed_gathered_excitations(failed, dirs_to_check, qsubFailed1=False)