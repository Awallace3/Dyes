import os
import glob
import subprocess
import json
import shutil
import sys
from error_mexc_dyes_v2 import method_dir_generator

sys.path.append("/Users/austinwallace/research/Dyes")
from dataset_names import ds
from final import qsub_to_max
from final import add_qsub_dir


class RMError(Exception):
    """could not remove directory"""
    pass


def remove_folder(path):
    # check if folder exists
    if os.path.exists(path):
        # remove if exists
        shutil.rmtree(path)
    else:
        # throw your exception to handle this special scenario
        raise RMError("your exception")


def qsubFiles(path_to_input_dirs, pbs_name="mex.pbs", monitor_jobs=[]):
    os.chdir(path_to_input_dirs)
    if len(monitor_jobs) == 0:
        directories = glob.glob("*")
    else:
        directories = monitor_jobs
    for i in directories:
        os.chdir(i)
        qsub = 'qsub %s' % pbs_name
        print(i, qsub, os.getcwd())
        subprocess.call(qsub, shell=True)
        os.chdir("..")


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
        print("hello")
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
    failed = []
    for i in resubmit:
        os.chdir(i)
        # print(i)
        out_files = glob.glob("*.out*")
        out_completion = glob.glob("mex_o.*")
        if len(out_files) == 0 and len(out_completion) == 0:
            print("\topt")
            add_qsub_dir('./', i.lower())
            # cmd = 'qsub mex.pbs'
            # print(os.getcwd(), cmd)
            # subprocess.call(cmd, shell=True)

        elif len(out_files) > len(out_completion):
            # elif len(out_files) >= 1 and len(out_completion) == 1:
            outs = len(out_files)
            comp = len(out_completion)
            dif = outs - comp
            while (dif > 0):
                cmd = 'touch name_o.o100000'
                print(cmd)
                subprocess.call(cmd, shell=True)
                dif -= 1
            print("\tfiles", i)
        elif len(out_files) < len(out_completion):
            outs = len(out_files)
            comp = len(out_completion)
            dif = comp - outs
            while (dif > 0):
                comp_fname = out_completion.pop()
                cmd = "rm %s" % comp_fname
                print(cmd)
                subprocess.call(cmd, shell=True)
                dif -= 1
        else:
            if os.path.exists('mex'):
                os.chdir("mexc")
                out_files = glob.glob("*.out*")
                out_completion = glob.glob("mex_o.*")
                if len(out_files) == 0 and len(out_completion) == 0:
                    print("fix_broken mexc else", i)
            else:
                print('\tfailed')
                failed.append(i)

        os.chdir("..")

    return failed


def fix_mex(resubmit):
    os.chdir("../results")

    for i in resubmit:
        print(i)
        os.chdir(i)
        out_files = glob.glob("*.out*")
        out_completion = glob.glob("*_o*")
        len_file = len(out_files)
        len_complete = len(out_completion)
        if len_complete > len_file:
            for i in range(len_complete - len_file):
                del_o = out_completion.pop()
                # subprocess.call("echo " + del_o, shell=True)
                print("rm %s" % del_o)
                subprocess.call("rm " + del_o, shell=True)
        elif len_complete < len_file:
            for i in range((len_file - len_complete)):
                create_o = "mex_o.o%s0000" % str(i + 15)
                print("touch %s" % create_o)
                # subprocess.call("echo " + create_o, shell=True)
                subprocess.call("touch " + create_o, shell=True)
        os.chdir("..")


def fix_mexc(resubmit, base_dir="mexc", baseName="mexc"):
    os.chdir("../results")
    for i in resubmit:
        print(i)
        if os.path.exists("%s/%s" % (i, base_dir)):
            os.chdir("%s/%s" % (i, base_dir))

            out_files = glob.glob("*.out*")
            out_completion = glob.glob("*_o*")
            len_file = len(out_files)
            len_complete = len(out_completion)
            if len_complete > len_file:
                for i in range(len_complete - len_file):
                    del_o = out_completion.pop()
                    # subprocess.call("echo " + del_o, shell=True)
                    print("rm %s" % del_o)
                    subprocess.call("rm " + del_o, shell=True)
            elif len_complete < len_file:
                for i in range((len_file - len_complete)):
                    create_o = "mexc_o.o%s0000" % str(i + 15)
                    print("touch %s" % create_o)
                    # subprocess.call("echo " + create_o, shell=True)
                    subprocess.call("touch " + create_o, shell=True)
            os.chdir("../..")
        else:
            print(i, "does not have mexc")


def failed_gathered_excitations(failed,
                                dirs_to_check,
                                qsubFailed1=False,
                                path_results="../results"):
    def_dir = os.getcwd()
    os.chdir(path_results)
    complete_dict = {}
    marked_for_death = []
    memory_issues = []
    for i in failed:
        os.chdir(i)
        # 0 if no dir, 1 if out file, 2 if cannot read out
        local = {}
        for j in dirs_to_check:
            if not os.path.exists(j):
                local[j] = 0
            else:
                if not os.path.exists("%s/%s" % (j, "mexc.out")):
                    local[j] = 1
                    if qsubFailed1:
                        qsub_dir = method_dir_generator(j, "")
                        add_qsub_dir(qsub_dir, i, '../qsub_queue')
                else:
                    out_files = len(glob.glob("%s/*.out*" % j))
                    out_completion = len(glob.glob("%s/*_o*" % j))
                    if 0 < out_files <= out_completion:
                        local[j] = 3
                        path = "%s/%s" % (j, "mexc.out")
                        with open(path, "r") as fp:
                            if len(fp.readlines()) < 10:
                                marked_for_death.append(i + "/" + j)
                            if "error termination request processed by link" in fp.read(
                            ).lower():
                                memory_issues.append(path)
                            if "error in internal coordinate system bad geom" in fp.read(
                            ).lower():
                                memory_issues.append(path)
                    else:
                        local[j] = 2
        cnt = 0
        for k, v in local.items():
            cnt += v
        if cnt != 9:
            complete_dict[i] = local
        os.chdir("..")
    os.chdir(def_dir)
    print(complete_dict)
    data = json.dumps(complete_dict,
                      default=lambda o: o.__dict__,
                      sort_keys=True,
                      indent=4)
    with open("tmp.dat", "w") as fp:
        for i in marked_for_death:
            fp.write(i + "\n")
    with open("exc.json", "w") as fp:
        fp.write(data)
        # fp.write("end")
    # print(data)
    # print(json.dumps(complete_dict, default=lambda o: o.__dict__,
    #       sort_keys=True, indent=4))
    print(memory_issues, len(memory_issues))
    return complete_dict, marked_for_death, memory_issues


def increase_memory(increment=2):
    # os.remove('mexc.out')
    # os.remove('mexc.pbs')
    return


def rm_dir(path_results, kill):
    def_dir = os.getcwd()
    os.chdir(path_results)
    print(os.getcwd())
    for i in kill:
        cmd = 'rm -r %s' % i
        print(cmd)
        subprocess.call(cmd, shell=True)
    os.chdir(def_dir)


def gather_results_dirs(path_results):
    files = glob.glob(path_results + '/*')
    ls = []
    for i in files:
        if "smiles" not in i:
            clean = i.split("/")[-1]
            ls.append(clean)
    return ls


def qsub_dir_time(path_results, minutes=60, steps=10):
    def_d = os.getcwd()
    os.chdir(path_results)
    for i in range(steps):
        qsub_to_max(max_queue=500, def_dir="../..")
        os.sleep(60 * minutes)
    os.chdir(def_d)
    return


def resubmit_ds_all():
    """
    Checks results_cp/ds_all5 directory for
    failed excitation calculations and resubmits the calculations
    """
    dirs_to_check = ['mexc', 'bhandhlyp', 'pbe1pbe']
    ls = ds.ds_all5('../pickles/fix.pickle')
    # ls = ds.ds_all5('../pickles/ds_all5.pickle')
    cdict, marked, memory = failed_gathered_excitations(
        ls,
        dirs_to_check,
        path_results="../results_cp/ds_all5",
        qsubFailed1=False)
    print(len(marked), len(memory), len(cdict), len(ls))
    # qsub_dir_time(path_results='results_cp/ds_all5', minutes=360)
    return


if __name__ == "__main__":
    resubmit_ds_all()
    # rm_dir('../results', marked)
    # print('cdict:', cdict)
    # failed_gathered_excitations(monitor_jobs, dirs_to_check)
