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

def add_qsub_dir(qsub_dir, geom_dir, path_qsub_queue='../../qsub_queue'):
    if qsub_dir == 'None':
        return 0
    elif qsub_dir == './':
        qsub_path = geom_dir + '\n'
    else:
        qsub_path = "%s/%s\n" % (geom_dir, qsub_dir)
    print(os.getcwd(), qsub_path, '../../qsub_queue')
    with open(path_qsub_queue, 'a') as fp:
        fp.write(qsub_path)
    return 1

def fix_broken(resubmit, path_results='../results'):
    os.chdir(path_results)
    json = os.getcwd() + '/..'
    for i in resubmit:
        os.chdir(i)
        print(i)
        out_files = glob.glob("*.out*")
        out_completion = glob.glob("mex_o.*")
        if len(out_files) == 0 and len(out_completion) == 0:
            print("\topt")
            add_qsub_dir('./', i.lower())
            cmd = 'qsub mex.pbs'
            #print(os.getcwd(), cmd)
            #subprocess.call(cmd, shell=True)
        elif len(out_files) >= 1 and len(out_completion) == 1:
            cmd = 'touch name_o.o100000'
            print("\tfiles")
            #subprocess.call(cmd, shell=True)
        else:
            if os.path.exists('mexc'):
                os.chdir("mexc")
                out_files = glob.glob("*.out*")
                out_completion = glob.glob("mex_o.*")
                if len(out_files) == 0 and len(out_completion) == 0:
                    cmd = 'qsub mexc.pbs'
                    add_qsub_dir('mexc', i.lower(), '../../../qsub_queue')
                    #print(os.getcwd(), cmd)
                    #subprocess.call(cmd, shell=True)
                    print('\texc')
                os.chdir("..")
            else:
                print("no mexc")

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

    monitor_jobs = ['7ed_21b_6ea', '7ed_21b_3ea', '7ed_21b_8ea', '7ed_21b_11ea', '7ed_21b_5ea', '7ed_21b_2ea', '7ed_21b_7ea', '7ed_21b_4ea', '7ed_21b_10ea', '7ed_21b_9ea', '7ed_21b_1ea', '7ed_20b_6ea', '7ed_20b_3ea', '7ed_20b_8ea', '7ed_20b_11ea', '7ed_20b_5ea', '7ed_20b_2ea', '7ed_20b_7ea', '7ed_20b_4ea', '7ed_20b_10ea', '7ed_20b_9ea', '7ed_20b_1ea', '7ed_6b_6ea', '7ed_6b_3ea', '7ed_6b_8ea', '7ed_6b_11ea', '7ed_6b_5ea', '7ed_6b_2ea', '7ed_6b_7ea', '7ed_6b_4ea', '7ed_6b_10ea', '7ed_6b_9ea', '7ed_6b_1ea', '7ed_26b_6ea', '7ed_26b_3ea', '7ed_26b_8ea', '7ed_26b_11ea', '7ed_26b_5ea', '7ed_26b_2ea', '7ed_26b_7ea', '7ed_26b_4ea', '7ed_26b_10ea', '7ed_26b_9ea', '7ed_26b_1ea', '7ed_25b_6ea', '7ed_25b_3ea', '7ed_25b_8ea', '7ed_25b_11ea', '7ed_25b_5ea', '7ed_25b_2ea', '7ed_25b_7ea', '7ed_25b_4ea', '7ed_25b_10ea', '7ed_25b_9ea', '7ed_25b_1ea', '7ed_24b_6ea', '7ed_24b_3ea', '7ed_24b_8ea', '7ed_24b_11ea', '7ed_24b_5ea', '7ed_24b_2ea', '7ed_24b_7ea', '7ed_24b_4ea', '7ed_24b_10ea', '7ed_24b_9ea', '7ed_24b_1ea', '7ed_1b_6ea', '7ed_1b_3ea', '7ed_1b_8ea', '7ed_1b_11ea', '7ed_1b_5ea', '7ed_1b_2ea', '7ed_1b_7ea', '7ed_1b_4ea', '7ed_1b_10ea', '7ed_1b_9ea', '7ed_1b_1ea', '7ed_23b_6ea', '7ed_23b_3ea', '7ed_23b_8ea', '7ed_23b_11ea', '7ed_23b_5ea', '7ed_23b_2ea', '7ed_23b_7ea', '7ed_23b_4ea', '7ed_23b_10ea', '7ed_23b_9ea', '7ed_23b_1ea', '7ed_17b_6ea', '7ed_17b_3ea', '7ed_17b_8ea', '7ed_17b_11ea', '7ed_17b_5ea', '7ed_17b_2ea', '7ed_17b_7ea', '7ed_17b_4ea', '7ed_17b_10ea', '7ed_17b_9ea', '7ed_17b_1ea', '7ed_22b_6ea', '7ed_22b_3ea', '7ed_22b_8ea', '7ed_22b_11ea', '7ed_22b_5ea', '7ed_22b_2ea', '7ed_22b_7ea', '7ed_22b_4ea', '7ed_22b_10ea', '7ed_22b_9ea', '7ed_22b_1ea', '7ed_16b_6ea', '7ed_16b_3ea', '7ed_16b_8ea', '7ed_16b_11ea', '7ed_16b_5ea', '7ed_16b_2ea', '7ed_16b_7ea', '7ed_16b_4ea', '7ed_16b_10ea', '7ed_16b_9ea', '7ed_16b_1ea', '1ed_21b_6ea', '1ed_21b_3ea', '1ed_21b_8ea', '1ed_21b_11ea', '1ed_21b_5ea', '1ed_21b_2ea', '1ed_21b_7ea', '1ed_21b_4ea', '1ed_21b_10ea', '1ed_21b_9ea', '1ed_21b_1ea', '1ed_20b_6ea', '1ed_20b_3ea', '1ed_20b_8ea', '1ed_20b_11ea', '1ed_20b_5ea', '1ed_20b_2ea', '1ed_20b_7ea', '1ed_20b_4ea', '1ed_20b_10ea', '1ed_20b_9ea', '1ed_20b_1ea', '1ed_6b_6ea', '1ed_6b_3ea', '1ed_6b_8ea', '1ed_6b_11ea', '1ed_6b_5ea', '1ed_6b_2ea', '1ed_6b_7ea', '1ed_6b_4ea', '1ed_6b_10ea', '1ed_6b_9ea', '1ed_6b_1ea', '1ed_26b_6ea', '1ed_26b_3ea', '1ed_26b_8ea', '1ed_26b_11ea', '1ed_26b_5ea', '1ed_26b_2ea', '1ed_26b_7ea', '1ed_26b_4ea', '1ed_26b_10ea', '1ed_26b_9ea', '1ed_26b_1ea', '1ed_25b_6ea', '1ed_25b_3ea', '1ed_25b_8ea', '1ed_25b_11ea', '1ed_25b_5ea', '1ed_25b_2ea', '1ed_25b_7ea', '1ed_25b_4ea', '1ed_25b_10ea', '1ed_25b_9ea', '1ed_25b_1ea', '1ed_24b_6ea', '1ed_24b_3ea', '1ed_24b_8ea', '1ed_24b_11ea', '1ed_24b_5ea', '1ed_24b_2ea', '1ed_24b_7ea', '1ed_24b_4ea', '1ed_24b_10ea', '1ed_24b_9ea', '1ed_24b_1ea', '1ed_1b_6ea', '1ed_1b_3ea', '1ed_1b_8ea', '1ed_1b_11ea', '1ed_1b_5ea', '1ed_1b_2ea', '1ed_1b_7ea', '1ed_1b_4ea', '1ed_1b_10ea', '1ed_1b_9ea', '1ed_1b_1ea', '1ed_23b_6ea', '1ed_23b_3ea', '1ed_23b_8ea', '1ed_23b_11ea', '1ed_23b_5ea', '1ed_23b_2ea', '1ed_23b_7ea', '1ed_23b_4ea', '1ed_23b_10ea', '1ed_23b_9ea', '1ed_23b_1ea', '1ed_17b_6ea', '1ed_17b_3ea', '1ed_17b_8ea', '1ed_17b_11ea', '1ed_17b_5ea', '1ed_17b_2ea', '1ed_17b_7ea', '1ed_17b_4ea', '1ed_17b_10ea', '1ed_17b_9ea', '1ed_17b_1ea', '1ed_22b_6ea', '1ed_22b_3ea', '1ed_22b_8ea', '1ed_22b_11ea', '1ed_22b_5ea', '1ed_22b_2ea', '1ed_22b_7ea', '1ed_22b_4ea', '1ed_22b_10ea', '1ed_22b_9ea', '1ed_22b_1ea', '1ed_16b_6ea', '1ed_16b_3ea', '1ed_16b_8ea', '1ed_16b_11ea', '1ed_16b_5ea', '1ed_16b_2ea', '1ed_16b_7ea', '1ed_16b_4ea', '1ed_16b_10ea', '1ed_16b_9ea', '1ed_16b_1ea', '6ed_21b_6ea', '6ed_21b_3ea', '6ed_21b_8ea', '6ed_21b_11ea', '6ed_21b_5ea', '6ed_21b_2ea', '6ed_21b_7ea', '6ed_21b_4ea', '6ed_21b_10ea', '6ed_21b_9ea', '6ed_21b_1ea', '6ed_20b_6ea', '6ed_20b_3ea', '6ed_20b_8ea', '6ed_20b_11ea', '6ed_20b_5ea', '6ed_20b_2ea', '6ed_20b_7ea', '6ed_20b_4ea', '6ed_20b_10ea', '6ed_20b_9ea', '6ed_20b_1ea', '6ed_6b_6ea', '6ed_6b_3ea', '6ed_6b_8ea', '6ed_6b_11ea', '6ed_6b_5ea', '6ed_6b_2ea', '6ed_6b_7ea', '6ed_6b_4ea', '6ed_6b_10ea', '6ed_6b_9ea', '6ed_6b_1ea', '6ed_26b_6ea', '6ed_26b_3ea', '6ed_26b_8ea', '6ed_26b_11ea', '6ed_26b_5ea', '6ed_26b_2ea', '6ed_26b_7ea', '6ed_26b_4ea', '6ed_26b_10ea', '6ed_26b_9ea', '6ed_26b_1ea', '6ed_25b_6ea', '6ed_25b_3ea', '6ed_25b_8ea', '6ed_25b_11ea', '6ed_25b_5ea', '6ed_25b_2ea', '6ed_25b_7ea', '6ed_25b_4ea', '6ed_25b_10ea', '6ed_25b_9ea', '6ed_25b_1ea', '6ed_24b_6ea', '6ed_24b_3ea', '6ed_24b_8ea', '6ed_24b_11ea', '6ed_24b_5ea', '6ed_24b_2ea', '6ed_24b_7ea', '6ed_24b_4ea', '6ed_24b_10ea', '6ed_24b_9ea', '6ed_24b_1ea', '6ed_1b_6ea', '6ed_1b_3ea', '6ed_1b_8ea', '6ed_1b_11ea', '6ed_1b_5ea', '6ed_1b_2ea', '6ed_1b_7ea', '6ed_1b_4ea', '6ed_1b_10ea', '6ed_1b_9ea', '6ed_1b_1ea', '6ed_23b_6ea', '6ed_23b_3ea', '6ed_23b_8ea', '6ed_23b_11ea', '6ed_23b_5ea', '6ed_23b_2ea', '6ed_23b_7ea', '6ed_23b_4ea', '6ed_23b_10ea', '6ed_23b_9ea', '6ed_23b_1ea', '6ed_17b_6ea', '6ed_17b_3ea', '6ed_17b_8ea', '6ed_17b_11ea', '6ed_17b_5ea', '6ed_17b_2ea', '6ed_17b_7ea', '6ed_17b_4ea', '6ed_17b_10ea', '6ed_17b_9ea', '6ed_17b_1ea', '6ed_22b_6ea', '6ed_22b_3ea', '6ed_22b_8ea', '6ed_22b_11ea', '6ed_22b_5ea', '6ed_22b_2ea', '6ed_22b_7ea', '6ed_22b_4ea', '6ed_22b_10ea', '6ed_22b_9ea', '6ed_22b_1ea', '6ed_16b_6ea', '6ed_16b_3ea', '6ed_16b_8ea', '6ed_16b_11ea', '6ed_16b_5ea', '6ed_16b_2ea', '6ed_16b_7ea', '6ed_16b_4ea', '6ed_16b_10ea', '6ed_16b_9ea', '6ed_16b_1ea', '3ed_21b_6ea', '3ed_21b_3ea', '3ed_21b_8ea', '3ed_21b_11ea', '3ed_21b_5ea', '3ed_21b_2ea', '3ed_21b_7ea', '3ed_21b_4ea', '3ed_21b_10ea', '3ed_21b_9ea', '3ed_21b_1ea', '3ed_20b_6ea', '3ed_20b_3ea', '3ed_20b_8ea', '3ed_20b_11ea', '3ed_20b_5ea', '3ed_20b_2ea', '3ed_20b_7ea', '3ed_20b_4ea', '3ed_20b_10ea', '3ed_20b_9ea', '3ed_20b_1ea', '3ed_6b_6ea', '3ed_6b_3ea', '3ed_6b_8ea', '3ed_6b_11ea', '3ed_6b_5ea', '3ed_6b_2ea', '3ed_6b_7ea', '3ed_6b_4ea', '3ed_6b_10ea', '3ed_6b_9ea', '3ed_6b_1ea', '3ed_26b_6ea', '3ed_26b_3ea', '3ed_26b_8ea', '3ed_26b_11ea', '3ed_26b_5ea', '3ed_26b_2ea', '3ed_26b_7ea', '3ed_26b_4ea', '3ed_26b_10ea', '3ed_26b_9ea', '3ed_26b_1ea', '3ed_25b_6ea', '3ed_25b_3ea', '3ed_25b_8ea', '3ed_25b_11ea', '3ed_25b_5ea', '3ed_25b_2ea', '3ed_25b_7ea', '3ed_25b_4ea', '3ed_25b_10ea', '3ed_25b_9ea', '3ed_25b_1ea', '3ed_24b_6ea', '3ed_24b_3ea', '3ed_24b_8ea', '3ed_24b_11ea', '3ed_24b_5ea', '3ed_24b_2ea', '3ed_24b_7ea', '3ed_24b_4ea', '3ed_24b_10ea', '3ed_24b_9ea', '3ed_24b_1ea', '3ed_1b_6ea', '3ed_1b_3ea', '3ed_1b_8ea', '3ed_1b_11ea', '3ed_1b_5ea', '3ed_1b_2ea', '3ed_1b_7ea', '3ed_1b_4ea', '3ed_1b_10ea', '3ed_1b_9ea', '3ed_1b_1ea', '3ed_23b_6ea', '3ed_23b_3ea', '3ed_23b_8ea', '3ed_23b_11ea', '3ed_23b_5ea', '3ed_23b_2ea', '3ed_23b_7ea', '3ed_23b_4ea', '3ed_23b_10ea', '3ed_23b_9ea', '3ed_23b_1ea', '3ed_17b_6ea', '3ed_17b_3ea', '3ed_17b_8ea', '3ed_17b_11ea', '3ed_17b_5ea', '3ed_17b_2ea', '3ed_17b_7ea', '3ed_17b_4ea', '3ed_17b_10ea', '3ed_17b_9ea', '3ed_17b_1ea', '3ed_22b_6ea', '3ed_22b_3ea', '3ed_22b_8ea', '3ed_22b_11ea', '3ed_22b_5ea', '3ed_22b_2ea', '3ed_22b_7ea', '3ed_22b_4ea', '3ed_22b_10ea', '3ed_22b_9ea', '3ed_22b_1ea', '3ed_16b_6ea', '3ed_16b_3ea', '3ed_16b_8ea', '3ed_16b_11ea', '3ed_16b_5ea', '3ed_16b_2ea', '3ed_16b_7ea', '3ed_16b_4ea', '3ed_16b_10ea', '3ed_16b_9ea', '3ed_16b_1ea', '5ed_21b_6ea', '5ed_21b_3ea', '5ed_21b_8ea', '5ed_21b_11ea', '5ed_21b_5ea', '5ed_21b_2ea', '5ed_21b_7ea', '5ed_21b_4ea', '5ed_21b_10ea', '5ed_21b_9ea', '5ed_21b_1ea', '5ed_20b_6ea', '5ed_20b_3ea', '5ed_20b_8ea', '5ed_20b_11ea', '5ed_20b_5ea', '5ed_20b_2ea', '5ed_20b_7ea', '5ed_20b_4ea', '5ed_20b_10ea', '5ed_20b_9ea', '5ed_20b_1ea', '5ed_6b_6ea', '5ed_6b_3ea', '5ed_6b_8ea', '5ed_6b_11ea', '5ed_6b_5ea', '5ed_6b_2ea', '5ed_6b_7ea', '5ed_6b_4ea', '5ed_6b_10ea', '5ed_6b_9ea', '5ed_6b_1ea', '5ed_26b_6ea', '5ed_26b_3ea', '5ed_26b_8ea', '5ed_26b_11ea', '5ed_26b_5ea', '5ed_26b_2ea', '5ed_26b_7ea', '5ed_26b_4ea', '5ed_26b_10ea', '5ed_26b_9ea', '5ed_26b_1ea', '5ed_25b_6ea', '5ed_25b_3ea', '5ed_25b_8ea', '5ed_25b_11ea', '5ed_25b_5ea', '5ed_25b_2ea', '5ed_25b_7ea', '5ed_25b_4ea', '5ed_25b_10ea', '5ed_25b_9ea', '5ed_25b_1ea', '5ed_24b_6ea', '5ed_24b_3ea', '5ed_24b_8ea', '5ed_24b_11ea', '5ed_24b_5ea', '5ed_24b_2ea', '5ed_24b_7ea', '5ed_24b_4ea', '5ed_24b_10ea', '5ed_24b_9ea', '5ed_24b_1ea', '5ed_1b_6ea', '5ed_1b_3ea', '5ed_1b_8ea', '5ed_1b_11ea', '5ed_1b_5ea', '5ed_1b_2ea', '5ed_1b_7ea', '5ed_1b_4ea', '5ed_1b_10ea', '5ed_1b_9ea', '5ed_1b_1ea', '5ed_23b_6ea', '5ed_23b_3ea', '5ed_23b_8ea', '5ed_23b_11ea', '5ed_23b_5ea', '5ed_23b_2ea', '5ed_23b_7ea', '5ed_23b_4ea', '5ed_23b_10ea', '5ed_23b_9ea', '5ed_23b_1ea', '5ed_17b_6ea', '5ed_17b_3ea', '5ed_17b_8ea', '5ed_17b_11ea', '5ed_17b_5ea', '5ed_17b_2ea', '5ed_17b_7ea', '5ed_17b_4ea', '5ed_17b_10ea', '5ed_17b_9ea', '5ed_17b_1ea', '5ed_22b_6ea', '5ed_22b_3ea', '5ed_22b_8ea', '5ed_22b_11ea', '5ed_22b_5ea', '5ed_22b_2ea', '5ed_22b_7ea', '5ed_22b_4ea', '5ed_22b_10ea', '5ed_22b_9ea', '5ed_22b_1ea', '5ed_16b_6ea', '5ed_16b_3ea', '5ed_16b_8ea', '5ed_16b_11ea', '5ed_16b_5ea', '5ed_16b_2ea', '5ed_16b_7ea', '5ed_16b_4ea', '5ed_16b_10ea', '5ed_16b_9ea', '5ed_16b_1ea', '2ed_21b_6ea', '2ed_21b_3ea', '2ed_21b_8ea', '2ed_21b_11ea', '2ed_21b_5ea', '2ed_21b_2ea', '2ed_21b_7ea', '2ed_21b_4ea', '2ed_21b_10ea', '2ed_21b_9ea', '2ed_21b_1ea', '2ed_20b_6ea', '2ed_20b_3ea', '2ed_20b_8ea', '2ed_20b_11ea', '2ed_20b_5ea', '2ed_20b_2ea', '2ed_20b_7ea', '2ed_20b_4ea', '2ed_20b_10ea', '2ed_20b_9ea', '2ed_20b_1ea', '2ed_6b_6ea', '2ed_6b_3ea', '2ed_6b_8ea', '2ed_6b_11ea', '2ed_6b_5ea', '2ed_6b_2ea', '2ed_6b_7ea', '2ed_6b_4ea', '2ed_6b_10ea', '2ed_6b_9ea', '2ed_6b_1ea', '2ed_26b_6ea', '2ed_26b_3ea', '2ed_26b_8ea', '2ed_26b_11ea', '2ed_26b_5ea', '2ed_26b_2ea', '2ed_26b_7ea', '2ed_26b_4ea', '2ed_26b_10ea', '2ed_26b_9ea', '2ed_26b_1ea', '2ed_25b_6ea', '2ed_25b_3ea', '2ed_25b_8ea', '2ed_25b_11ea', '2ed_25b_5ea', '2ed_25b_2ea', '2ed_25b_7ea', '2ed_25b_4ea', '2ed_25b_10ea', '2ed_25b_9ea', '2ed_25b_1ea', '2ed_24b_6ea', '2ed_24b_3ea', '2ed_24b_8ea', '2ed_24b_11ea', '2ed_24b_5ea', '2ed_24b_2ea', '2ed_24b_7ea', '2ed_24b_4ea', '2ed_24b_10ea', '2ed_24b_9ea', '2ed_24b_1ea', '2ed_1b_6ea', '2ed_1b_3ea', '2ed_1b_8ea', '2ed_1b_11ea', '2ed_1b_5ea', '2ed_1b_2ea', '2ed_1b_7ea', '2ed_1b_4ea', '2ed_1b_10ea', '2ed_1b_9ea', '2ed_1b_1ea', '2ed_23b_6ea', '2ed_23b_3ea', '2ed_23b_8ea', '2ed_23b_11ea', '2ed_23b_5ea', '2ed_23b_2ea', '2ed_23b_7ea', '2ed_23b_4ea', '2ed_23b_10ea', '2ed_23b_9ea', '2ed_23b_1ea', '2ed_17b_6ea', '2ed_17b_3ea', '2ed_17b_8ea', '2ed_17b_11ea', '2ed_17b_5ea', '2ed_17b_2ea', '2ed_17b_7ea', '2ed_17b_4ea', '2ed_17b_10ea', '2ed_17b_9ea', '2ed_17b_1ea', '2ed_22b_6ea', '2ed_22b_3ea', '2ed_22b_8ea', '2ed_22b_11ea', '2ed_22b_5ea', '2ed_22b_2ea', '2ed_22b_7ea', '2ed_22b_4ea', '2ed_22b_10ea', '2ed_22b_9ea', '2ed_22b_1ea', '2ed_16b_6ea', '2ed_16b_3ea', '2ed_16b_8ea', '2ed_16b_11ea', '2ed_16b_5ea', '2ed_16b_2ea', '2ed_16b_7ea', '2ed_16b_4ea', '2ed_16b_10ea', '2ed_16b_9ea', '2ed_16b_1ea']
    monitor_jobs = [ '5ed_6b_3ea', '5ed_6b_8ea', '5ed_6b_11ea', '5ed_6b_5ea', '5ed_6b_2ea', '5ed_6b_7ea', '5ed_6b_4ea', '5ed_6b_10ea', '5ed_6b_9ea', '5ed_6b_1ea', '5ed_26b_6ea', '5ed_26b_3ea', '5ed_26b_8ea', '5ed_26b_11ea', '5ed_26b_5ea', '5ed_26b_2ea', '5ed_26b_7ea', '5ed_26b_4ea', '5ed_26b_10ea', '5ed_26b_9ea', '5ed_26b_1ea', '5ed_25b_6ea', '5ed_25b_3ea', '5ed_25b_8ea', '5ed_25b_11ea', '5ed_25b_5ea', '5ed_25b_2ea', '5ed_25b_7ea', '5ed_25b_4ea', '5ed_25b_10ea', '5ed_25b_9ea', '5ed_25b_1ea', '5ed_24b_6ea', '5ed_24b_3ea', '5ed_24b_8ea', '5ed_24b_11ea', '5ed_24b_5ea', '5ed_24b_2ea', '5ed_24b_7ea', '5ed_24b_4ea', '5ed_24b_10ea', '5ed_24b_9ea', '5ed_24b_1ea', '5ed_1b_6ea', '5ed_1b_3ea', '5ed_1b_8ea', '5ed_1b_11ea', '5ed_1b_5ea', '5ed_1b_2ea', '5ed_1b_7ea', '5ed_1b_4ea', '5ed_1b_10ea', '5ed_1b_9ea', '5ed_1b_1ea', '5ed_23b_6ea', '5ed_23b_3ea', '5ed_23b_8ea', '5ed_23b_11ea', '5ed_23b_5ea', '5ed_23b_2ea', '5ed_23b_7ea', '5ed_23b_4ea', '5ed_23b_10ea', '5ed_23b_9ea', '5ed_23b_1ea', '5ed_17b_6ea', '5ed_17b_3ea', '5ed_17b_8ea', '5ed_17b_11ea', '5ed_17b_5ea', '5ed_17b_2ea', '5ed_17b_7ea', '5ed_17b_4ea', '5ed_17b_10ea', '5ed_17b_9ea', '5ed_17b_1ea', '5ed_22b_6ea', '5ed_22b_3ea', '5ed_22b_8ea', '5ed_22b_11ea', '5ed_22b_5ea', '5ed_22b_2ea', '5ed_22b_7ea', '5ed_22b_4ea', '5ed_22b_10ea', '5ed_22b_9ea', '5ed_22b_1ea', '5ed_16b_6ea', '5ed_16b_3ea', '5ed_16b_8ea', '5ed_16b_11ea', '5ed_16b_5ea', '5ed_16b_2ea', '5ed_16b_7ea', '5ed_16b_4ea', '5ed_16b_10ea', '5ed_16b_9ea', '5ed_16b_1ea', '2ed_21b_6ea', '2ed_21b_3ea', '2ed_21b_8ea', '2ed_21b_11ea', '2ed_21b_5ea', '2ed_21b_2ea', '2ed_21b_7ea', '2ed_21b_4ea', '2ed_21b_10ea', '2ed_21b_9ea', '2ed_21b_1ea', '2ed_20b_6ea', '2ed_20b_3ea', '2ed_20b_8ea', '2ed_20b_11ea', '2ed_20b_5ea', '2ed_20b_2ea', '2ed_20b_7ea', '2ed_20b_4ea', '2ed_20b_10ea', '2ed_20b_9ea', '2ed_20b_1ea', '2ed_6b_6ea', '2ed_6b_3ea', '2ed_6b_8ea', '2ed_6b_11ea', '2ed_6b_5ea', '2ed_6b_2ea', '2ed_6b_7ea', '2ed_6b_4ea', '2ed_6b_10ea', '2ed_6b_9ea', '2ed_6b_1ea', '2ed_26b_6ea', '2ed_26b_3ea', '2ed_26b_8ea', '2ed_26b_11ea', '2ed_26b_5ea', '2ed_26b_2ea', '2ed_26b_7ea', '2ed_26b_4ea', '2ed_26b_10ea', '2ed_26b_9ea', '2ed_26b_1ea', '2ed_25b_6ea', '2ed_25b_3ea', '2ed_25b_8ea', '2ed_25b_11ea', '2ed_25b_5ea', '2ed_25b_2ea', '2ed_25b_7ea', '2ed_25b_4ea', '2ed_25b_10ea', '2ed_25b_9ea', '2ed_25b_1ea', '2ed_24b_6ea', '2ed_24b_3ea', '2ed_24b_8ea', '2ed_24b_11ea', '2ed_24b_5ea', '2ed_24b_2ea', '2ed_24b_7ea', '2ed_24b_4ea', '2ed_24b_10ea', '2ed_24b_9ea', '2ed_24b_1ea', '2ed_1b_6ea', '2ed_1b_3ea', '2ed_1b_8ea', '2ed_1b_11ea', '2ed_1b_5ea', '2ed_1b_2ea', '2ed_1b_7ea', '2ed_1b_4ea', '2ed_1b_10ea', '2ed_1b_9ea', '2ed_1b_1ea', '2ed_23b_6ea', '2ed_23b_3ea', '2ed_23b_8ea', '2ed_23b_11ea', '2ed_23b_5ea', '2ed_23b_2ea', '2ed_23b_7ea', '2ed_23b_4ea', '2ed_23b_10ea', '2ed_23b_9ea', '2ed_23b_1ea', '2ed_17b_6ea', '2ed_17b_3ea', '2ed_17b_8ea', '2ed_17b_11ea', '2ed_17b_5ea', '2ed_17b_2ea', '2ed_17b_7ea', '2ed_17b_4ea', '2ed_17b_10ea', '2ed_17b_9ea', '2ed_17b_1ea', '2ed_22b_6ea', '2ed_22b_3ea', '2ed_22b_8ea', '2ed_22b_11ea', '2ed_22b_5ea', '2ed_22b_2ea', '2ed_22b_7ea', '2ed_22b_4ea', '2ed_22b_10ea', '2ed_22b_9ea', '2ed_22b_1ea', '2ed_16b_6ea', '2ed_16b_3ea', '2ed_16b_8ea', '2ed_16b_11ea', '2ed_16b_5ea', '2ed_16b_2ea', '2ed_16b_7ea', '2ed_16b_4ea', '2ed_16b_10ea', '2ed_16b_9ea', '2ed_16b_1ea']
    #fix_broken(resubmit)
    #fix_mexc(resubmit)
    #fix_mex(resubmit)
    
    monitor_jobs = ['7ed_21b_6ea', '7ed_21b_3ea', '7ed_21b_8ea', '7ed_21b_11ea', '7ed_21b_5ea', '7ed_21b_2ea', '7ed_21b_7ea', '7ed_21b_4ea', '7ed_21b_10ea', '7ed_21b_9ea', '7ed_21b_1ea', '7ed_20b_6ea', '7ed_20b_3ea', '7ed_20b_8ea', '7ed_20b_11ea', '7ed_20b_5ea', '7ed_20b_2ea', '7ed_20b_7ea', '7ed_20b_4ea', '7ed_20b_10ea', '7ed_20b_9ea', '7ed_20b_1ea', '7ed_6b_6ea', '7ed_6b_3ea', '7ed_6b_8ea', '7ed_6b_11ea', '7ed_6b_5ea', '7ed_6b_2ea', '7ed_6b_7ea', '7ed_6b_4ea', '7ed_6b_10ea', '7ed_6b_9ea', '7ed_6b_1ea', '7ed_26b_6ea', '7ed_26b_3ea', '7ed_26b_8ea', '7ed_26b_11ea', '7ed_26b_5ea', '7ed_26b_2ea', '7ed_26b_7ea', '7ed_26b_4ea', '7ed_26b_10ea', '7ed_26b_9ea', '7ed_26b_1ea', '7ed_25b_6ea', '7ed_25b_3ea', '7ed_25b_8ea', '7ed_25b_11ea', '7ed_25b_5ea', '7ed_25b_2ea', '7ed_25b_7ea', '7ed_25b_4ea', '7ed_25b_10ea', '7ed_25b_9ea', '7ed_25b_1ea', '7ed_24b_6ea', '7ed_24b_3ea', '7ed_24b_8ea', '7ed_24b_11ea', '7ed_24b_5ea', '7ed_24b_2ea', '7ed_24b_7ea', '7ed_24b_4ea', '7ed_24b_10ea', '7ed_24b_9ea', '7ed_24b_1ea', '7ed_1b_6ea', '7ed_1b_3ea', '7ed_1b_8ea', '7ed_1b_11ea', '7ed_1b_5ea', '7ed_1b_2ea', '7ed_1b_7ea', '7ed_1b_4ea', '7ed_1b_10ea', '7ed_1b_9ea', '7ed_1b_1ea', '7ed_23b_6ea', '7ed_23b_3ea', '7ed_23b_8ea', '7ed_23b_11ea', '7ed_23b_5ea', '7ed_23b_2ea', '7ed_23b_7ea', '7ed_23b_4ea', '7ed_23b_10ea', '7ed_23b_9ea', '7ed_23b_1ea', '7ed_17b_6ea', '7ed_17b_3ea', '7ed_17b_8ea', '7ed_17b_11ea', '7ed_17b_5ea', '7ed_17b_2ea', '7ed_17b_7ea', '7ed_17b_4ea', '7ed_17b_10ea', '7ed_17b_9ea', '7ed_17b_1ea', '7ed_22b_6ea', '7ed_22b_3ea', '7ed_22b_8ea', '7ed_22b_11ea', '7ed_22b_5ea', '7ed_22b_2ea', '7ed_22b_7ea', '7ed_22b_4ea', '7ed_22b_10ea', '7ed_22b_9ea', '7ed_22b_1ea', '7ed_16b_6ea', '7ed_16b_3ea', '7ed_16b_8ea', '7ed_16b_11ea', '7ed_16b_5ea', '7ed_16b_2ea', '7ed_16b_7ea', '7ed_16b_4ea', '7ed_16b_10ea', '7ed_16b_9ea', '7ed_16b_1ea', '1ed_21b_6ea', '1ed_21b_3ea', '1ed_21b_8ea', '1ed_21b_11ea', '1ed_21b_5ea', '1ed_21b_2ea', '1ed_21b_7ea', '1ed_21b_4ea', '1ed_21b_10ea', '1ed_21b_9ea', '1ed_21b_1ea', '1ed_20b_6ea', '1ed_20b_3ea', '1ed_20b_8ea', '1ed_20b_11ea', '1ed_20b_5ea', '1ed_20b_2ea', '1ed_20b_7ea', '1ed_20b_4ea', '1ed_20b_10ea', '1ed_20b_9ea', '1ed_20b_1ea', '1ed_6b_6ea', '1ed_6b_3ea', '1ed_6b_8ea', '1ed_6b_11ea', '1ed_6b_5ea', '1ed_6b_2ea', '1ed_6b_7ea', '1ed_6b_4ea', '1ed_6b_10ea', '1ed_6b_9ea', '1ed_6b_1ea', '1ed_26b_6ea', '1ed_26b_3ea', '1ed_26b_8ea', '1ed_26b_11ea', '1ed_26b_5ea', '1ed_26b_2ea', '1ed_26b_7ea', '1ed_26b_4ea', '1ed_26b_10ea', '1ed_26b_9ea', '1ed_26b_1ea', '1ed_25b_6ea', '1ed_25b_3ea', '1ed_25b_8ea', '1ed_25b_11ea', '1ed_25b_5ea', '1ed_25b_2ea', '1ed_25b_7ea', '1ed_25b_4ea', '1ed_25b_10ea', '1ed_25b_9ea', '1ed_25b_1ea', '1ed_24b_6ea', '1ed_24b_3ea', '1ed_24b_8ea', '1ed_24b_11ea', '1ed_24b_5ea', '1ed_24b_2ea', '1ed_24b_7ea', '1ed_24b_4ea', '1ed_24b_10ea', '1ed_24b_9ea', '1ed_24b_1ea', '1ed_1b_6ea', '1ed_1b_3ea', '1ed_1b_8ea', '1ed_1b_11ea', '1ed_1b_5ea', '1ed_1b_2ea', '1ed_1b_7ea', '1ed_1b_4ea', '1ed_1b_10ea', '1ed_1b_9ea', '1ed_1b_1ea', '1ed_23b_6ea', '1ed_23b_3ea', '1ed_23b_8ea', '1ed_23b_11ea', '1ed_23b_5ea', '1ed_23b_2ea', '1ed_23b_7ea', '1ed_23b_4ea', '1ed_23b_10ea', '1ed_23b_9ea', '1ed_23b_1ea', '1ed_17b_6ea', '1ed_17b_3ea', '1ed_17b_8ea', '1ed_17b_11ea', '1ed_17b_5ea', '1ed_17b_2ea', '1ed_17b_7ea', '1ed_17b_4ea', '1ed_17b_10ea', '1ed_17b_9ea', '1ed_17b_1ea', '1ed_22b_6ea', '1ed_22b_3ea', '1ed_22b_8ea', '1ed_22b_11ea', '1ed_22b_5ea', '1ed_22b_2ea', '1ed_22b_7ea', '1ed_22b_4ea', '1ed_22b_10ea', '1ed_22b_9ea', '1ed_22b_1ea', '1ed_16b_6ea', '1ed_16b_3ea', '1ed_16b_8ea', '1ed_16b_11ea', '1ed_16b_5ea', '1ed_16b_2ea', '1ed_16b_7ea', '1ed_16b_4ea', '1ed_16b_10ea', '1ed_16b_9ea', '1ed_16b_1ea', '6ed_21b_6ea', '6ed_21b_3ea', '6ed_21b_8ea', '6ed_21b_11ea', '6ed_21b_5ea', '6ed_21b_2ea', '6ed_21b_7ea', '6ed_21b_4ea', '6ed_21b_10ea', '6ed_21b_9ea', '6ed_21b_1ea', '6ed_20b_6ea', '6ed_20b_3ea', '6ed_20b_8ea', '6ed_20b_11ea', '6ed_20b_5ea', '6ed_20b_2ea', '6ed_20b_7ea', '6ed_20b_4ea', '6ed_20b_10ea', '6ed_20b_9ea', '6ed_20b_1ea', '6ed_6b_6ea', '6ed_6b_3ea', '6ed_6b_8ea', '6ed_6b_11ea', '6ed_6b_5ea', '6ed_6b_2ea', '6ed_6b_7ea', '6ed_6b_4ea', '6ed_6b_10ea', '6ed_6b_9ea', '6ed_6b_1ea', '6ed_26b_6ea', '6ed_26b_3ea', '6ed_26b_8ea', '6ed_26b_11ea', '6ed_26b_5ea', '6ed_26b_2ea', '6ed_26b_7ea', '6ed_26b_4ea', '6ed_26b_10ea', '6ed_26b_9ea', '6ed_26b_1ea', '6ed_25b_6ea', '6ed_25b_3ea', '6ed_25b_8ea', '6ed_25b_11ea', '6ed_25b_5ea', '6ed_25b_2ea', '6ed_25b_7ea', '6ed_25b_4ea', '6ed_25b_10ea', '6ed_25b_9ea', '6ed_25b_1ea', '6ed_24b_6ea', '6ed_24b_3ea', '6ed_24b_8ea', '6ed_24b_11ea', '6ed_24b_5ea', '6ed_24b_2ea', '6ed_24b_7ea', '6ed_24b_4ea', '6ed_24b_10ea', '6ed_24b_9ea', '6ed_24b_1ea', '6ed_1b_6ea', '6ed_1b_3ea', '6ed_1b_8ea', '6ed_1b_11ea', '6ed_1b_5ea', '6ed_1b_2ea', '6ed_1b_7ea', '6ed_1b_4ea', '6ed_1b_10ea', '6ed_1b_9ea', '6ed_1b_1ea', '6ed_23b_6ea', '6ed_23b_3ea', '6ed_23b_8ea', '6ed_23b_11ea', '6ed_23b_5ea', '6ed_23b_2ea', '6ed_23b_7ea', '6ed_23b_4ea', '6ed_23b_10ea', '6ed_23b_9ea', '6ed_23b_1ea', '6ed_17b_6ea', '6ed_17b_3ea', '6ed_17b_8ea', '6ed_17b_11ea', '6ed_17b_5ea', '6ed_17b_2ea', '6ed_17b_7ea', '6ed_17b_4ea', '6ed_17b_10ea', '6ed_17b_9ea', '6ed_17b_1ea', '6ed_22b_6ea', '6ed_22b_3ea', '6ed_22b_8ea', '6ed_22b_11ea', '6ed_22b_5ea', '6ed_22b_2ea', '6ed_22b_7ea', '6ed_22b_4ea', '6ed_22b_10ea', '6ed_22b_9ea', '6ed_22b_1ea', '6ed_16b_6ea', '6ed_16b_3ea', '6ed_16b_8ea', '6ed_16b_11ea', '6ed_16b_5ea', '6ed_16b_2ea', '6ed_16b_7ea', '6ed_16b_4ea', '6ed_16b_10ea', '6ed_16b_9ea', '6ed_16b_1ea', '3ed_21b_6ea', '3ed_21b_3ea', '3ed_21b_8ea', '3ed_21b_11ea', '3ed_21b_5ea', '3ed_21b_2ea', '3ed_21b_7ea', '3ed_21b_4ea', '3ed_21b_10ea', '3ed_21b_9ea', '3ed_21b_1ea', '3ed_20b_6ea', '3ed_20b_3ea', '3ed_20b_8ea', '3ed_20b_11ea', '3ed_20b_5ea', '3ed_20b_2ea', '3ed_20b_7ea', '3ed_20b_4ea', '3ed_20b_10ea', '3ed_20b_9ea', '3ed_20b_1ea', '3ed_6b_6ea', '3ed_6b_3ea', '3ed_6b_8ea', '3ed_6b_11ea', '3ed_6b_5ea', '3ed_6b_2ea', '3ed_6b_7ea', '3ed_6b_4ea', '3ed_6b_10ea', '3ed_6b_9ea', '3ed_6b_1ea', '3ed_26b_6ea', '3ed_26b_3ea', '3ed_26b_8ea', '3ed_26b_11ea', '3ed_26b_5ea', '3ed_26b_2ea', '3ed_26b_7ea', '3ed_26b_4ea', '3ed_26b_10ea', '3ed_26b_9ea', '3ed_26b_1ea', '3ed_25b_6ea', '3ed_25b_3ea', '3ed_25b_8ea', '3ed_25b_11ea', '3ed_25b_5ea', '3ed_25b_2ea', '3ed_25b_7ea', '3ed_25b_4ea', '3ed_25b_10ea', '3ed_25b_9ea', '3ed_25b_1ea', '3ed_24b_6ea', '3ed_24b_3ea', '3ed_24b_8ea', '3ed_24b_11ea', '3ed_24b_5ea', '3ed_24b_2ea', '3ed_24b_7ea', '3ed_24b_4ea', '3ed_24b_10ea', '3ed_24b_9ea', '3ed_24b_1ea', '3ed_1b_6ea', '3ed_1b_3ea', '3ed_1b_8ea', '3ed_1b_11ea', '3ed_1b_5ea', '3ed_1b_2ea', '3ed_1b_7ea', '3ed_1b_4ea', '3ed_1b_10ea', '3ed_1b_9ea', '3ed_1b_1ea', '3ed_23b_6ea', '3ed_23b_3ea', '3ed_23b_8ea', '3ed_23b_11ea', '3ed_23b_5ea', '3ed_23b_2ea', '3ed_23b_7ea', '3ed_23b_4ea', '3ed_23b_10ea', '3ed_23b_9ea', '3ed_23b_1ea', '3ed_17b_6ea', '3ed_17b_3ea', '3ed_17b_8ea', '3ed_17b_11ea', '3ed_17b_5ea', '3ed_17b_2ea', '3ed_17b_7ea', '3ed_17b_4ea', '3ed_17b_10ea', '3ed_17b_9ea', '3ed_17b_1ea', '3ed_22b_6ea', '3ed_22b_3ea', '3ed_22b_8ea', '3ed_22b_11ea', '3ed_22b_5ea', '3ed_22b_2ea', '3ed_22b_7ea', '3ed_22b_4ea', '3ed_22b_10ea', '3ed_22b_9ea', '3ed_22b_1ea', '3ed_16b_6ea', '3ed_16b_3ea', '3ed_16b_8ea', '3ed_16b_11ea', '3ed_16b_5ea', '3ed_16b_2ea', '3ed_16b_7ea', '3ed_16b_4ea', '3ed_16b_10ea', '3ed_16b_9ea', '3ed_16b_1ea', '5ed_21b_6ea', '5ed_21b_3ea', '5ed_21b_8ea', '5ed_21b_11ea', '5ed_21b_5ea', '5ed_21b_2ea', '5ed_21b_7ea', '5ed_21b_4ea', '5ed_21b_10ea', '5ed_21b_9ea', '5ed_21b_1ea', '5ed_20b_6ea', '5ed_20b_3ea', '5ed_20b_8ea', '5ed_20b_11ea', '5ed_20b_5ea', '5ed_20b_2ea', '5ed_20b_7ea', '5ed_20b_4ea', '5ed_20b_10ea', '5ed_20b_9ea', '5ed_20b_1ea', '5ed_6b_6ea', '5ed_6b_3ea', '5ed_6b_8ea', '5ed_6b_11ea', '5ed_6b_5ea', '5ed_6b_2ea', '5ed_6b_7ea', '5ed_6b_4ea', '5ed_6b_10ea', '5ed_6b_9ea', '5ed_6b_1ea', '5ed_26b_6ea', '5ed_26b_3ea', '5ed_26b_8ea', '5ed_26b_11ea', '5ed_26b_5ea', '5ed_26b_2ea', '5ed_26b_7ea', '5ed_26b_4ea', '5ed_26b_10ea', '5ed_26b_9ea', '5ed_26b_1ea', '5ed_25b_6ea', '5ed_25b_3ea', '5ed_25b_8ea', '5ed_25b_11ea', '5ed_25b_5ea', '5ed_25b_2ea', '5ed_25b_7ea', '5ed_25b_4ea', '5ed_25b_10ea', '5ed_25b_9ea', '5ed_25b_1ea', '5ed_24b_6ea', '5ed_24b_3ea', '5ed_24b_8ea', '5ed_24b_11ea', '5ed_24b_5ea', '5ed_24b_2ea', '5ed_24b_7ea', '5ed_24b_4ea', '5ed_24b_10ea', '5ed_24b_9ea', '5ed_24b_1ea', '5ed_1b_6ea', '5ed_1b_3ea', '5ed_1b_8ea', '5ed_1b_11ea', '5ed_1b_5ea', '5ed_1b_2ea', '5ed_1b_7ea', '5ed_1b_4ea', '5ed_1b_10ea', '5ed_1b_9ea', '5ed_1b_1ea', '5ed_23b_6ea', '5ed_23b_3ea', '5ed_23b_8ea', '5ed_23b_11ea', '5ed_23b_5ea', '5ed_23b_2ea', '5ed_23b_7ea', '5ed_23b_4ea', '5ed_23b_10ea', '5ed_23b_9ea', '5ed_23b_1ea', '5ed_17b_6ea', '5ed_17b_3ea', '5ed_17b_8ea', '5ed_17b_11ea', '5ed_17b_5ea', '5ed_17b_2ea', '5ed_17b_7ea', '5ed_17b_4ea', '5ed_17b_10ea', '5ed_17b_9ea', '5ed_17b_1ea', '5ed_22b_6ea', '5ed_22b_3ea', '5ed_22b_8ea', '5ed_22b_11ea', '5ed_22b_5ea', '5ed_22b_2ea', '5ed_22b_7ea', '5ed_22b_4ea', '5ed_22b_10ea', '5ed_22b_9ea', '5ed_22b_1ea', '5ed_16b_6ea', '5ed_16b_3ea', '5ed_16b_8ea', '5ed_16b_11ea', '5ed_16b_5ea', '5ed_16b_2ea', '5ed_16b_7ea', '5ed_16b_4ea', '5ed_16b_10ea', '5ed_16b_9ea', '5ed_16b_1ea', '2ed_21b_6ea', '2ed_21b_3ea', '2ed_21b_8ea', '2ed_21b_11ea', '2ed_21b_5ea', '2ed_21b_2ea', '2ed_21b_7ea', '2ed_21b_4ea', '2ed_21b_10ea', '2ed_21b_9ea', '2ed_21b_1ea', '2ed_20b_6ea', '2ed_20b_3ea', '2ed_20b_8ea', '2ed_20b_11ea', '2ed_20b_5ea', '2ed_20b_2ea', '2ed_20b_7ea', '2ed_20b_4ea', '2ed_20b_10ea', '2ed_20b_9ea', '2ed_20b_1ea', '2ed_6b_6ea', '2ed_6b_3ea', '2ed_6b_8ea', '2ed_6b_11ea', '2ed_6b_5ea', '2ed_6b_2ea', '2ed_6b_7ea', '2ed_6b_4ea', '2ed_6b_10ea', '2ed_6b_9ea', '2ed_6b_1ea', '2ed_26b_6ea', '2ed_26b_3ea', '2ed_26b_8ea', '2ed_26b_11ea', '2ed_26b_5ea', '2ed_26b_2ea', '2ed_26b_7ea', '2ed_26b_4ea', '2ed_26b_10ea', '2ed_26b_9ea', '2ed_26b_1ea', '2ed_25b_6ea', '2ed_25b_3ea', '2ed_25b_8ea', '2ed_25b_11ea', '2ed_25b_5ea', '2ed_25b_2ea', '2ed_25b_7ea', '2ed_25b_4ea', '2ed_25b_10ea', '2ed_25b_9ea', '2ed_25b_1ea', '2ed_24b_6ea', '2ed_24b_3ea', '2ed_24b_8ea', '2ed_24b_11ea', '2ed_24b_5ea', '2ed_24b_2ea', '2ed_24b_7ea', '2ed_24b_4ea', '2ed_24b_10ea', '2ed_24b_9ea', '2ed_24b_1ea', '2ed_1b_6ea', '2ed_1b_3ea', '2ed_1b_8ea', '2ed_1b_11ea', '2ed_1b_5ea', '2ed_1b_2ea', '2ed_1b_7ea', '2ed_1b_4ea', '2ed_1b_10ea', '2ed_1b_9ea', '2ed_1b_1ea', '2ed_23b_6ea', '2ed_23b_3ea', '2ed_23b_8ea', '2ed_23b_11ea', '2ed_23b_5ea', '2ed_23b_2ea', '2ed_23b_7ea', '2ed_23b_4ea', '2ed_23b_10ea', '2ed_23b_9ea', '2ed_23b_1ea', '2ed_17b_6ea', '2ed_17b_3ea', '2ed_17b_8ea', '2ed_17b_11ea', '2ed_17b_5ea', '2ed_17b_2ea', '2ed_17b_7ea', '2ed_17b_4ea', '2ed_17b_10ea', '2ed_17b_9ea', '2ed_17b_1ea', '2ed_22b_6ea', '2ed_22b_3ea', '2ed_22b_8ea', '2ed_22b_11ea', '2ed_22b_5ea', '2ed_22b_2ea', '2ed_22b_7ea', '2ed_22b_4ea', '2ed_22b_10ea', '2ed_22b_9ea', '2ed_22b_1ea', '2ed_16b_6ea', '2ed_16b_3ea', '2ed_16b_8ea', '2ed_16b_11ea', '2ed_16b_5ea', '2ed_16b_2ea', '2ed_16b_7ea', '2ed_16b_4ea', '2ed_16b_10ea', '2ed_16b_9ea', '2ed_16b_1ea']
    monitor_jobs = ['7ed_21b_8ea', '7ed_21b_2ea', '7ed_21b_10ea', '7ed_20b_6ea', '7ed_20b_3ea', '7ed_20b_11ea', '7ed_20b_5ea', '7ed_20b_2ea', '7ed_20b_7ea', '7ed_20b_4ea', '7ed_20b_10ea', '7ed_20b_9ea', '7ed_20b_1ea', '7ed_6b_6ea', '7ed_6b_3ea', '7ed_6b_8ea', '7ed_6b_11ea', '7ed_6b_5ea', '7ed_6b_2ea', '7ed_6b_4ea', '7ed_6b_10ea', '7ed_6b_9ea', '7ed_6b_1ea', '7ed_25b_6ea', '7ed_25b_8ea', '7ed_25b_5ea', '7ed_25b_2ea', '7ed_25b_10ea', '7ed_25b_9ea', '7ed_24b_6ea', '7ed_1b_6ea', '7ed_1b_3ea', '7ed_1b_8ea', '7ed_1b_11ea', '7ed_1b_5ea', '7ed_1b_2ea', '7ed_1b_4ea', '7ed_1b_10ea', '7ed_1b_9ea', '7ed_23b_6ea', '7ed_23b_8ea', '7ed_23b_11ea', '7ed_23b_5ea', '7ed_23b_2ea', '7ed_23b_7ea', '7ed_23b_10ea', '7ed_23b_1ea', '7ed_17b_6ea', '7ed_17b_3ea', '7ed_17b_8ea', '7ed_17b_11ea', '7ed_17b_5ea', '7ed_17b_2ea', '7ed_17b_7ea', '7ed_17b_4ea', '7ed_17b_10ea', '7ed_17b_9ea', '7ed_17b_1ea', '7ed_22b_6ea', '7ed_22b_3ea', '7ed_22b_11ea', '7ed_22b_5ea', '7ed_22b_10ea', '7ed_22b_1ea', '7ed_16b_6ea', '7ed_16b_3ea', '7ed_16b_8ea', '7ed_16b_11ea', '7ed_16b_5ea', '7ed_16b_2ea', '7ed_16b_7ea', '7ed_16b_4ea', '7ed_16b_10ea', '7ed_16b_9ea', '7ed_16b_1ea', '1ed_21b_5ea', '1ed_21b_4ea', '1ed_21b_10ea', '1ed_21b_1ea', '1ed_20b_6ea', '1ed_20b_3ea', '1ed_20b_8ea', '1ed_20b_11ea', '1ed_20b_2ea', '1ed_20b_4ea', '1ed_20b_10ea', '1ed_20b_9ea', '1ed_20b_1ea', '1ed_6b_6ea', '1ed_6b_3ea', '1ed_6b_8ea', '1ed_6b_11ea', '1ed_6b_2ea', '1ed_6b_4ea', '1ed_6b_10ea', '1ed_6b_9ea', '1ed_6b_1ea', '1ed_25b_6ea', '1ed_25b_3ea', '1ed_25b_8ea', '1ed_25b_11ea', '1ed_25b_10ea', '1ed_24b_6ea', '1ed_24b_8ea', '1ed_24b_11ea', '1ed_24b_5ea', '1ed_24b_2ea', '1ed_24b_9ea', '1ed_24b_1ea', '1ed_1b_3ea', '1ed_1b_2ea', '1ed_1b_4ea', '1ed_1b_10ea', '1ed_1b_9ea', '1ed_1b_1ea', '1ed_23b_3ea', '1ed_23b_5ea', '1ed_23b_2ea', '1ed_23b_7ea', '1ed_23b_10ea', '1ed_23b_9ea', '1ed_23b_1ea', '1ed_17b_6ea', '1ed_17b_3ea', '1ed_17b_8ea', '1ed_17b_11ea', '1ed_17b_2ea', '1ed_17b_7ea', '1ed_17b_4ea', '1ed_17b_10ea', '1ed_17b_9ea', '1ed_17b_1ea', '1ed_22b_8ea', '1ed_22b_11ea', '1ed_22b_10ea', '1ed_22b_9ea', '1ed_22b_1ea', '1ed_16b_6ea', '1ed_16b_3ea', '1ed_16b_8ea', '1ed_16b_11ea', '1ed_16b_5ea', '1ed_16b_2ea', '1ed_16b_7ea', '1ed_16b_4ea', '1ed_16b_10ea', '1ed_16b_9ea', '1ed_16b_1ea', '6ed_21b_3ea', '6ed_20b_6ea', '6ed_20b_3ea', '6ed_20b_8ea', '6ed_20b_11ea', '6ed_20b_5ea', '6ed_20b_2ea', '6ed_26b_11ea', '6ed_23b_9ea', '6ed_16b_5ea', '6ed_16b_4ea', '3ed_26b_7ea', '3ed_26b_9ea', '3ed_26b_1ea', '3ed_16b_5ea', '5ed_6b_8ea', '5ed_6b_11ea', '5ed_6b_5ea', '5ed_6b_2ea', '5ed_6b_7ea', '5ed_6b_4ea', '5ed_6b_10ea', '5ed_6b_9ea', '5ed_6b_1ea', '5ed_25b_6ea', '5ed_25b_3ea', '5ed_25b_8ea', '5ed_25b_11ea', '5ed_25b_5ea', '5ed_25b_2ea', '5ed_25b_7ea', '5ed_25b_4ea', '5ed_25b_10ea', '5ed_25b_9ea', '5ed_25b_1ea', '5ed_24b_6ea', '5ed_24b_3ea', '5ed_24b_8ea', '5ed_24b_11ea', '5ed_24b_5ea', '5ed_24b_2ea', '5ed_24b_7ea', '5ed_24b_4ea', '5ed_24b_10ea', '5ed_24b_9ea', '5ed_24b_1ea', '5ed_1b_6ea', '5ed_1b_8ea', '5ed_1b_11ea', '5ed_1b_5ea', '5ed_1b_2ea', '5ed_1b_7ea', '5ed_1b_4ea', '5ed_1b_10ea', '5ed_1b_9ea', '5ed_23b_6ea', '5ed_23b_3ea', '5ed_23b_8ea', '5ed_23b_11ea', '5ed_23b_5ea', '5ed_23b_2ea', '5ed_23b_7ea', '5ed_23b_4ea', '5ed_23b_10ea', '5ed_23b_9ea', '5ed_23b_1ea', '5ed_17b_6ea', '5ed_17b_3ea', '5ed_17b_8ea', '5ed_17b_11ea', '5ed_17b_5ea', '5ed_17b_2ea', '5ed_17b_7ea', '5ed_17b_4ea', '5ed_17b_10ea', '5ed_17b_9ea', '5ed_17b_1ea', '5ed_22b_8ea', '5ed_22b_11ea', '5ed_22b_5ea', '5ed_22b_2ea', '5ed_22b_7ea', '5ed_22b_4ea', '5ed_22b_9ea', '5ed_22b_1ea', '5ed_16b_6ea', '5ed_16b_3ea', '5ed_16b_8ea', '5ed_16b_11ea', '5ed_16b_5ea', '5ed_16b_2ea', '5ed_16b_7ea', '5ed_16b_4ea', '5ed_16b_10ea', '5ed_16b_9ea', '5ed_16b_1ea', '2ed_21b_6ea', '2ed_21b_3ea', '2ed_21b_8ea', '2ed_21b_5ea', '2ed_21b_2ea', '2ed_21b_7ea', '2ed_21b_4ea', '2ed_21b_10ea', '2ed_21b_9ea', '2ed_20b_3ea', '2ed_20b_11ea', '2ed_20b_5ea',
    '2ed_20b_2ea', '2ed_20b_4ea', '2ed_20b_10ea', '2ed_6b_6ea', '2ed_6b_3ea', '2ed_6b_11ea', '2ed_6b_9ea', '2ed_6b_1ea', '2ed_25b_6ea', '2ed_25b_3ea', '2ed_25b_8ea', '2ed_25b_11ea', '2ed_25b_2ea', '2ed_25b_7ea', '2ed_25b_4ea', '2ed_25b_10ea', '2ed_25b_9ea', '2ed_25b_1ea', '2ed_24b_6ea', '2ed_24b_3ea', '2ed_24b_8ea', '2ed_24b_11ea', '2ed_24b_5ea', '2ed_24b_2ea', '2ed_24b_7ea', '2ed_24b_4ea', '2ed_24b_10ea', '2ed_24b_9ea', '2ed_24b_1ea', '2ed_1b_6ea', '2ed_1b_3ea', '2ed_1b_8ea', '2ed_1b_11ea', '2ed_1b_5ea', '2ed_1b_2ea', '2ed_1b_7ea', '2ed_1b_4ea', '2ed_1b_10ea', '2ed_1b_9ea', '2ed_1b_1ea', '2ed_23b_6ea', '2ed_23b_3ea', '2ed_23b_8ea', '2ed_23b_11ea', '2ed_23b_5ea', '2ed_23b_2ea', '2ed_23b_7ea', '2ed_23b_4ea', '2ed_23b_10ea', '2ed_23b_9ea', '2ed_23b_1ea', '2ed_17b_6ea', '2ed_17b_3ea', '2ed_17b_8ea', '2ed_17b_11ea', '2ed_17b_5ea', '2ed_17b_2ea', '2ed_17b_7ea', '2ed_17b_4ea', '2ed_17b_10ea', '2ed_17b_9ea', '2ed_17b_1ea', '2ed_22b_6ea', '2ed_22b_3ea', '2ed_22b_8ea', '2ed_22b_5ea', '2ed_22b_2ea', '2ed_22b_7ea', '2ed_22b_4ea', '2ed_22b_1ea', '2ed_16b_6ea', '2ed_16b_3ea', '2ed_16b_8ea', '2ed_16b_11ea', '2ed_16b_5ea', '2ed_16b_2ea', '2ed_16b_7ea', '2ed_16b_4ea', '2ed_16b_10ea', '2ed_16b_9ea', '2ed_16b_1ea']
    #fix_broken(monitor_jobs)
    #fix_mex(monitor_jobs)
    #failed = ['7ed_5b_2ea', '7ed_1b_3ea', '3ed_1b_3ea']

    dirs_to_check = ['mexc', 'bhandhlyp', 'pbe1pbe']
    #fix_mexc(failed)
    #rerun failed_gathered_excitations for getting last steps
    failed_gathered_excitations(monitor_jobs, dirs_to_check, qsubFailed1=True)
    #failed_gathered_excitations(monitor_jobs, dirs_to_check)
    
