import os
import itertools
import glob
import subprocess
import time

from .ES_extraction import ES_extraction
from .absorpt import absorpt

from .molecule_json import Molecule
from .molecule_json import Molecule_exc
from .molecule_json import MoleculeList
from .molecule_json import MoleculeList_exc
# from .error_mexc_dyes_v2 import main as err_v2

# requires obabel installed...
# brew install obabel
# conda install -c openbabel openbabel


def read_user():
    with open("user", "r") as fp:
        return fp.read().rstrip()


def collectLocalStructures(subdirectories, banned=[]):
    localStructuresDict = {}
    number_locals = 0

    for num, i in enumerate(subdirectories):
        os.chdir(i)
        print("\n%s\n" % i)
        localStructuresDict["local{0}".format(num + 1)] = []
        localSmiles = glob.glob("*.smi")
        for j in localSmiles:
            # print(j[:-4])
            if j[:-4] not in banned:
                # print(j[:-4])
                with open(j) as f:
                    smiles = f.read()
                    smiles = smiles.split("\n")
                    smiles[0] = smiles[0].rstrip()
                    localStructuresDict["local{0}".format(num + 1)].append(
                        (smiles[0], j[:-4], smiles[1])
                    )
                    #  smiles[0]==smiles, j[:-4]==local_name, smiles[1]==name
            else:
                print(j[:-4], "skipped due to banned")

        os.chdir("..")
        number_locals += 1
    print(localStructuresDict)

    return localStructuresDict


def permutationDict(localStructuresDict):

    pre_perm = []

    for key, value in localStructuresDict.items():
        pre_perm = pre_perm + [value]

    post_perm = list(itertools.product(*pre_perm))
    # print(len(post_perm))
    return post_perm


def smilesRingCleanUp(f, s, t):
    print()
    smi1, na1, form1 = f
    smi2, na2, form2 = s
    smi3, na3, form3 = t
    name = na1 + "_" + na2 + "_" + na3
    formalName = form1 + "::" + form2 + "::" + form3
    cmd = "../src/number_rings.pl '%s' '%s' '%s'" % (smi1, smi2, smi3)
    line = subprocess.getoutput(cmd)
    return line, name, formalName


def generateMolecules(
    smiles_tuple_list,
    method_opt,
    basis_set_opt,
    mem_com_opt,
    mem_pbs_opt,
    cluster,
):
    monitor_jobs = []
    if not os.path.exists("results"):
        os.mkdir("results")
    if not os.path.exists("results/smiles_input"):
        os.mkdir("results/smiles_input")

    os.chdir("results")

    for num, i in enumerate(smiles_tuple_list):
        first, second, third = i
        line, name, formalName = smilesRingCleanUp(first, second, third)
        mol_lst = MoleculeList()
        if os.path.exists("../results.json"):
            mol_lst.setData("../results.json")
        else:
            print("Creating results.json\n")
            mol_lst.sendToFile("../results.json")

        if mol_lst.checkMolecule(line):
            print(
                "\nMolecule already exists and the name smiles is... \n%s\n"
                % line
            )
            continue
        mol = Molecule()
        mol.setSMILES(line)
        file = open("smiles_input/{0}.smi".format(name), "w+")
        file.write(line)
        file.close()
        cmd = "obabel -ismi smiles_input/{0}.smi -oxyz --gen3D".format(name)
        carts = subprocess.check_output(cmd, shell=True)
        carts = str(carts)
        carts = carts.rstrip()
        carts = carts.splitlines()
        for n, i in enumerate(carts):
            carts[n] = i.split("\\n")
        carts_cleaned = []
        invalid = True
        for n, i in enumerate(carts[0]):
            if n > 1:
                carts_cleaned.append(i)
                invalid = False
        if invalid:
            print("invalid line{0}".format(num), line)
            invalid = True
            continue
        del carts_cleaned[-1]

        # print(carts_cleaned)
        os.mkdir(name)
        err = subprocess.call("touch %s/info.json" % name, shell=True)

        mol.setName(name)
        mol.setParts(formalName)
        mol.setLocalName(name)
        mol.sendToFile("%s/info.json" % name)

        data = ""
        for line in carts_cleaned:
            data += line + "\n"

        # TODO: fix to be new input file format
        error_mexc_dyes_v1.gaussianInputFiles(
            0,
            method_opt,
            basis_set_opt,
            mem_com_opt,
            mem_pbs_opt,
            cluster,
            baseName="mex",
            procedure="OPT",
            data=data,
            dir_name=name,
        )
        add_qsub_dir("./", name, "../qsub_queue")

        # need to add qsub here for v2

        mol_lst.addMolecule(mol)
        mol_lst.sendToFile("../results.json")
        monitor_jobs.append(name)
    os.chdir("..")
    print(monitor_jobs)
    return monitor_jobs


def submitOpt(monitor_jobs):
    os.chdir("results")
    for i in monitor_jobs:
        os.chdir(i)
        cmd = "qsub mex.pbs"
        subprocess.call(cmd, shell=True)
        os.chdir("..")
    os.chdir("..")


def add_excitation_data(
    dir_name,
    baseName,
    method_mexc,
    basis_set_mexc,
):
    occVal, virtVal = ES_extraction(
        "%s/%s.out" % (dir_name, baseName)
    )
    if occVal == virtVal and occVal == 0:
        print("failed to add")
        return 0, 0
    mol = Molecule()
    mol.setData("info.json")
    mol.setHOMO(occVal)
    mol.setLUMO(virtVal)
    mol.appendExcitations(
        absorpt("mexc/mexc.out", method_mexc, basis_set_mexc)
    )
    mol.toJSON()
    mol.sendToFile("info.json")
    mol_lst = MoleculeList()
    mol_lst.setData("../../results.json")
    mol_lst.updateMolecule(mol)
    mol_lst.sendToFile("../../results.json")


def jobResubmit(
    monitor_jobs,
    min_delay,
    number_delays,
    method_opt,
    basis_set_opt,
    mem_com_opt,
    mem_pbs_opt,
    method_mexc,
    basis_set_mexc,
    mem_com_mexc,
    mem_pbs_mexc,
    cluster,
    route="results",
    add_methods={
        "methods": [],
        "basis_set": [],
        "mem_com": [],
        "mem_pbs": [],
    },
):
    """
    Modified from ice_analog_spectra_generator repo
    """
    add_methods_length = len(add_methods["methods"])

    if (
        add_methods_length != len(add_methods["basis_set"])
        and add_methods_length != len(add_methods["mem_com"])
        and add_methods_length != len(add_methods["mem_pbs"])
    ):
        print(
            "add_methods must have values that have lists of the same length.\nTerminating jobResubmit before start"
        )
        return []
    resubmission_max = add_methods_length

    mol_lst = MoleculeList()
    if os.path.exists("results.json"):
        mol_lst.setData("results.json")
    else:
        mol_lst.sendToFile("results.json")

    min_delay = min_delay * 60
    # cluster_list = glob.glob("%s/*" % route)
    complete = []
    resubmissions = []
    for i in range(len(monitor_jobs)):
        complete.append(0)
        resubmissions.append(2)
        # resubmissions.append(resubmission_max)
    calculations_complete = False
    # comment change directory below in production
    os.chdir(route)

    for i in range(number_delays):
        # time.sleep(min_delay)
        for num, j in enumerate(monitor_jobs):
            os.chdir(j)
            delay = i
            mexc_check = glob.glob("mexc")
            if len(mexc_check) > 0:
                complete[num] = 1
                mexc_check_out = glob.glob("mexc/mexc.o*")
                mexc_check_out_complete = glob.glob("mexc/*_o*")

                # if complete[num] != 2 and len(mexc_check_out) > 0 and len(mexc_check_out_complete) > 0:
                if (
                    complete[num] < 2
                    and len(mexc_check_out) > 0
                    and len(mexc_check_out_complete) > 0
                ):

                    occVal, virtVal = ES_extraction(
                        "mexc/mexc.out"
                    )
                    if occVal == virtVal and occVal == 0:
                        print(j)
                    mol = Molecule()
                    mol.setData("info.json")
                    mol.setHOMO(occVal)
                    mol.setLUMO(virtVal)
                    # Testing below
                    mol.setExictations(
                        absorpt("mexc/mexc.out", method_mexc, basis_set_mexc)
                    )

                    mol.toJSON()
                    mol.sendToFile("info.json")

                    # mol_lst.addMolecule(mol)
                    mol_lst = MoleculeList()
                    mol_lst.setData("../../results.json")
                    mol_lst.updateMolecule(mol)
                    mol_lst.sendToFile("../../results.json")

                    complete[num] = 2

                # if complete[num] >= 2

            if complete[num] < 1:
                print("directory for", j)
                action, resubmissions = error_mexc_dyes_v1.main(
                    num,
                    method_opt,
                    basis_set_opt,
                    mem_com_opt,
                    mem_pbs_opt,
                    method_mexc,
                    basis_set_mexc,
                    mem_com_mexc,
                    mem_pbs_mexc,
                    resubmissions,
                    delay,
                    cluster,
                    j,
                    xyzSmiles=True,
                )
            elif complete[num] == 2:
                pos = complete[num] - 2
                action, resubmissions = error_mexc_dyes_v1.main(
                    num,
                    method_opt,
                    basis_set_opt,
                    mem_com_opt,
                    mem_pbs_opt,
                    add_methods["methods"][pos],
                    add_methods["basis_set"][pos],
                    add_methods["mem_com"][pos],
                    add_methods["mem_pbs"][pos],
                    resubmissions,
                    delay,
                    cluster,
                    j,
                    xyzSmiles=False,
                )

            pos = complete[num] - 2
            if pos >= 0:
                dir_name = add_methods["methods"][pos].lower()
                mexc_check_out = glob.glob("%s/mexc.o*" % dir_name)
                mexc_check_out_complete = glob.glob("%s/*_o*" % dir_name)
                if (
                    complete[num] < 3
                    and len(mexc_check_out) > 0
                    and len(mexc_check_out_complete) > 0
                ):
                    add_excitation_data(
                        dir_name,
                        "mexc",
                        add_methods["methods"][pos],
                        add_methods["basis_set"][pos],
                    )

            mexc_check = []
            if complete[num] < 2:
                print(complete[num], i)
                print(j)
            os.chdir("..")
        stage = 0
        for k in range(len(complete)):
            stage += complete[k]
            # if stage == len(complete)*2:
            if stage == len(complete) * add_methods_length:
                calculations_complete = True

        if calculations_complete == True:
            print(complete)
            print("\nCalculations are complete.")
            print("Took %.2f hours" % (i * min_delay / 60))
            return complete
        print("Completion List\n", complete, "\n")
        print("delay %d" % (i))
        """
        qsub_funct
        """
        time.sleep(min_delay)
    for i in range(len(resubmissions)):
        if resubmissions[i] < 2:
            print("Not finished %d: %s" % (resubmissions[i], monitor_jobs[i]))
    os.chdir("..")
    return complete


def check_add_methods(add_methods, funct_name):
    ln = len(add_methods["methods"])
    if (
        ln == len(add_methods["basis_set"])
        and ln == len(add_methods["mem_com"])
        and ln == len(add_methods["mem_pbs"])
    ):
        return True
    else:
        print(
            "\nadd_methods must have values that have lists of the same length.\nTerminating %s before start\n"
            % funct_name
        )
        return False


def qsub(path="."):
    print("qsub dir", path)
    resetDirNum = len(path.split("/"))
    if path != ".":
        os.chdir(path)
    pbs_file = glob.glob("*.pbs")[0]
    cmd = "qsub %s" % pbs_file
    print(os.getcwd(), "cmd", cmd)
    failure = subprocess.call(cmd, shell=True)
    if path != ".":
        for i in range(resetDirNum):
            os.chdir("..")


def add_qsub_dir(qsub_dir, geom_dir, path_qsub_queue="../../qsub_queue"):
    if qsub_dir == "None":
        return 0
    elif qsub_dir == "./":
        qsub_path = geom_dir + "\n"
    else:
        qsub_path = "%s/%s\n" % (geom_dir, qsub_dir)
    print(os.getcwd(), qsub_path, "../../qsub_queue")
    with open(path_qsub_queue, "a") as fp:
        fp.write(qsub_path)
    return 1


def qsub_to_max(max_queue=100, user=""):
    with open("../qsub_queue", "r") as fp:
        qsubs = fp.readlines()
    cmd = "qstat -u %s | wc -l > ../qsub_len" % user
    subprocess.call(cmd, shell=True)
    print("qsub_to_max", os.getcwd(), "../qsub_len", "../qsub_queue")
    with open("../qsub_len", "r") as fp:
        current_queue = int(fp.read()) - 5
    os.remove("../qsub_len")
    dif = max_queue - current_queue
    print("dif is", dif)
    if dif > 0:
        cnt = 0
        while cnt < dif and len(qsubs) > 0:
            qsub_path = qsubs.pop(0)
            qsub_path = qsub_path.rstrip().replace("\n", "")
            print("\n", qsub_path, os.getcwd(), "\n")
            qsub(qsub_path)
            cnt += 1
    with open("../qsub_queue", "w") as fp:
        for i in qsubs:
            fp.write(i)
    return 1


def r_qsub_dir(method_mexc, solvent):
    if method_mexc == "CAM-B3LYP":
        qsub_dir = "mexc"
    else:
        qsub_dir = method_mexc.lower()
    if solvent != "":
        qsub_dir += "_%s" % solvent
    return qsub_dir


def jobResubmit_v2(
    monitor_jobs,
    min_delay,
    number_delays,
    method_opt,
    basis_set_opt,
    mem_com_opt,
    mem_pbs_opt,
    method_mexc,
    basis_set_mexc,
    mem_com_mexc,
    mem_pbs_mexc,
    cluster,
    route="results",
    add_methods={
        "methods": [],
        "basis_set": [],
        "solvent": [],
        "mem_com": [],
        "mem_pbs": [],
    },
    max_queue=200,
    results_json="results.json",
    user=read_user(),
    identify_zeros=False,
    create_smiles=True,
):
    """
    Modified from jobResubmit above
    """
    if identify_zeros:
        zeros_lst = []
    if not os.path.exists("qsub_queue"):
        subprocess.call("touch qsub_queue", shell=True)

    if not check_add_methods(add_methods, "jobResubmit_v2"):
        return []

    add_methods_length = len(add_methods["methods"])
    mol_lst = MoleculeList()
    if os.path.exists("results.json"):
        mol_lst.setData("results.json")
    else:
        mol_lst.sendToFile("results.json")

    min_delay = min_delay * 60
    complete = []
    resubmissions = []
    for i in range(len(monitor_jobs)):
        complete.append(0)
        resubmissions.append(2)
    calculations_complete = False
    print(os.getcwd())
    os.chdir(route)

    for i in range(number_delays):
        # time.sleep(min_delay)
        for num, j in enumerate(monitor_jobs):
            os.chdir(j)
            delay = i
            mexc_check = glob.glob("mexc")
            if len(mexc_check) > 0:
                complete[num] = 1
                mexc_check_out = glob.glob("mexc/mexc.o*")
                mexc_check_out_complete = glob.glob("mexc/*_o*")
                if (
                    complete[num] < 2
                    and len(mexc_check_out) > 0
                    and len(mexc_check_out_complete) > 0
                ):
                    """
                    #occVal, virtVal = ES_extraction('mexc/mexc.out')
                    #if occVal == virtVal and occVal == 0:
                    #    print(j)
                    mol = Molecule()
                    mol.setData('info.json')
                    #mol.setHOMO(occVal)
                    #mol.setLUMO(virtVal)
                    # Testing below
                    #mol.setExictations(absorpt('mexc/mexc.out', method_mexc, basis_set_mexc))

                    mol.toJSON()
                    mol.sendToFile('info.json')

                    #mol_lst.addMolecule(mol)
                    mol_lst = MoleculeList()
                    print(os.getcwd())
                    #mol_lst.setData("../../results.json")
                    mol_lst.setData("../../%s" % results_json)
                    mol_lst.updateMolecule(mol)
                    #mol_lst.sendToFile('../../results.json')
                    mol_lst.sendToFile('../../%s' % results_json)
                    """

                    complete[num] = 2

                # if complete[num] >= 2

            if complete[num] < 1:
                if identify_zeros:
                    zeros_lst.append(j)
                print("directory for", j)
                # action, resubmissions, qsub_dir = err_v2(
                #     num,
                #     method_opt,
                #     basis_set_opt,
                #     mem_com_opt,
                #     mem_pbs_opt,
                #     method_mexc,
                #     basis_set_mexc,
                #     mem_com_mexc,
                #     mem_pbs_mexc,
                #     resubmissions,
                #     delay,
                #     cluster,
                #     j,
                #     xyzSmiles=create_smiles,
                # )
                if qsub_dir != "None":
                    add_qsub_dir(qsub_dir.lower(), j)
            if complete[num] <= 2:
                for pos in range(add_methods_length):
                    test_dir = r_qsub_dir(
                        add_methods["methods"][pos],
                        add_methods["solvent"][pos],
                    )
                    if not os.path.exists(test_dir):
                        print("add method", add_methods)
                        # (
                        #     action,
                        #     resubmissions,
                        #     qsub_dir,
                        # ) = err_v2(
                        #     num,
                        #     method_opt,
                        #     basis_set_opt,
                        #     mem_com_opt,
                        #     mem_pbs_opt,
                        #     add_methods["methods"][pos],
                        #     add_methods["basis_set"][pos],
                        #     add_methods["mem_com"][pos],
                        #     add_methods["mem_pbs"][pos],
                        #     resubmissions,
                        #     delay,
                        #     cluster,
                        #     j,
                        #     xyzSmiles=False,
                        #     solvent=add_methods["solvent"][pos],
                        # )
                        # print(pos, os.getcwd())
                        if qsub_dir != "None":
                            add_qsub_dir(qsub_dir.lower(), j)
                    else:
                        complete[num] += 1

            mexc_check = []
            os.chdir("..")
        stage = 0
        for k in range(len(complete)):
            stage += complete[k]
            # if stage == len(complete)*2:
            if stage == len(complete) * (add_methods_length + 2):
                calculations_complete = True

        qsub_to_max(max_queue, user)
        # qsub_to_max(max_queue, 'r2652')
        if calculations_complete == True:
            print(complete)
            print("\nCalculations are complete.")
            print("Took %.2f hours" % (i * min_delay / 60))
            return complete
        print("Completion List\n", complete, "\n")
        print("delay %d" % (i))
        """
        qsub_funct
        """
        if identify_zeros:
            print("identified zeros:", zeros_lst)
        time.sleep(min_delay)
    for i in range(len(resubmissions)):
        if resubmissions[i] < 2:
            print("Not finished %d: %s" % (resubmissions[i], monitor_jobs[i]))
    os.chdir("..")
    return complete


def read_ds_from_file(filename, path="./dataset_names/"):
    ds = []
    with open(path + filename, "r") as fp:
        ds = fp.read().split("\n")
        clean = []
        for i in ds:
            if i != "":
                clean.append(i)
    return clean


def qmgr(
    config={
        "options": {
            "opt": True,
            "exc": True,
            "cluster": "map",
            "max_queue": 200,
            "minDelay": 0.01,
            "maxAttempts": 2,
            "pathResults": "./results",
            "datasetNamesPath": "./dataset_names",
        },
        "opt": {
            "method_opt": "STO-3G",
            "basis_set_opt": "6-31G",
            "mem_com_opt": "1600",
            "mem_pbs_opt": "10",
            "solvent": "",
            "GuassianKeyWord": "",
            "submit": True,
        },
        "exc": [
            {
                "method_opt": "CAM-B3LYP",
                "basis_set_opt": "6-311G(d,p)",
                "mem_com_opt": "1600",
                "mem_pbs_opt": "10",
                "solvent": "",
                "nstates": 10,
                "GuassianKeyWord": "",
            },
            {
                "method_opt": "PBE1PBE",
                "basis_set_opt": "6-311G(d,p)",
                "mem_com_opt": "1600",
                "mem_pbs_opt": "10",
                "solvent": "",
                "nstates": 10,
                "GuassianKeyWord": "",
            },
            {
                "method_opt": "bhandhlyp",
                "basis_set_opt": "6-311G(d,p)",
                "mem_com_opt": "1600",
                "mem_pbs_opt": "10",
                "solvent": "",
                "nstates": 10,
                "GuassianKeyWord": "",
            },
        ],
    }
):
    """
    Use with main.py and input.json
    """
    job_dirs = read_ds_from_file(config['options']['datasetNamesPath'], '')
    print(job_dirs)
    path = config["options"]['pathResults']

    minDelay = config['options']['minDelay'] * 60
    for i in range(config['options']['maxAttempts']):
        for job in job_dirs:
            lPath = path + '/' + job
            print(lPath)

        print(i, 'out of', config["options"]['maxAttempts'])
        time.sleep(minDelay)

    return


def gather_general_smiles(monitor_jobs, path_results="./results"):
    os.chdir(path_results)
    for i in monitor_jobs:
        os.chdir(i)
        out_files = glob.glob("*.out*")

        if len(out_files) == 0:
            print("NO OUT FILE")
            return

        last_out = out_files[0]
        highest = 1
        for i in range(len(out_files)):
            t = out_files[i][-1]
            if t == "t":
                t = 1
            else:
                t = int(t)
            if t > highest:
                t = highest
                last_out = out_files[i]
        with open(last_out, "r") as fp:
            lines = fp.readlines()
        error_mexc_dyes_v1.find_geom(
            lines,
            error=False,
            filename=last_out,
            imaginary=False,
            geomDirName=i,
        )

        os.chdir("..")


def gather_excitation_data(
    path_results,
    monitor_jobs,
    add_methods,
    method_mexc,
    basis_set_mexc,
    baseName="mexc",
    results_json="results.json",
    exc_json=False,
):
    if not check_add_methods(add_methods, "gather_excitation_data"):
        return
    pops = ""
    for i in path_results:
        if i == "/":
            pops += "../"

    mol_lst = MoleculeList_exc()
    mol_lst.setData("%s" % results_json)

    os.chdir(path_results)

    failed = []
    for i in monitor_jobs:
        os.chdir(i)

        if not os.path.exists("mexc/mexc.out"):
            print(i, "does not have mexc/mexc.out")
            os.chdir("..")
            continue
        if exc_json:
            mol = Molecule_exc()
            mol.setData("info.json")
        else:
            mol = Molecule()
            mol.setData("info.json")
            occVal, virtVal = ES_extraction("mexc/mexc.out")
            if occVal == 0 and occVal == 0:
                print(i, "no data found in mexc/mexc.out\n")
                failed.append(i)
                os.chdir("..")
                continue
            mol.setHOMO(occVal)
            mol.setLUMO(virtVal)

        excitations = absorpt(
            "mexc/mexc.out", method_mexc, basis_set_mexc, exc_json=True
        )
        if i == "5ed_16b_8ea":
            print(i, excitations)

        if excitations == []:
            if i not in failed:
                failed.append(i)
                print(i, "\n")
            os.chdir("..")
            continue
        mol.setExictations(excitations)

        methods_len = len(add_methods["methods"])

        for j in range(methods_len):
            method = add_methods["methods"][j]
            basis_set = add_methods["basis_set"][j]
            lPath = "%s/%s.out" % (method.lower(), baseName)
            if os.path.exists(lPath):

                mol.appendExcitations(
                    absorpt(lPath, method, basis_set, exc_json=exc_json)
                )
            else:
                if i not in failed:
                    failed.append(i)
        mol_lst.updateMolecule(mol, exc_json=exc_json)
        os.chdir("..")

    mol_lst.sendToFile("%s%s" % (pops, results_json))
    print("FAILED:", failed)
    return True


def clean_dir_name(dir_name):
    return dir_name.replace("-", "").replace(",", "")


def main():
    three_types = [
        "eDonors",
        "backbones",
        "eAcceptors",
    ]  # Name of subdirectories holding the local structures

    banned = []

    localStructuresDict = collectLocalStructures(three_types, banned)
    smiles_tuple_list = permutationDict(localStructuresDict)
    print("smiles_tuple_list", smiles_tuple_list)
    three_types = [
        "eDonors",
        "backbones",
        "eAcceptors",
    ]  # Name of subdirectories holding the local structures

    resubmit_delay_min = 60 * 6  # 60 * 12
    resubmit_max_attempts = 120

    # geometry optimization options
    method_opt = "B3LYP"
    # method_opt = "HF"
    basis_set_opt = "6-311G(d,p)"
    # basis_set_opt = "6-31G"
    mem_com_opt = "1600"  # mb
    mem_pbs_opt = "10"  # gb

    # TD-DFT options
    method_mexc = "CAM-B3LYP"
    basis_set_mexc = "6-311G(d,p)"
    mem_com_mexc = "1600"  # mb
    mem_pbs_mexc = "10"  # gb"

    # cluster='map'
    cluster = "seq"

    # comment for testing
    monitor_jobs = generateMolecules(
        smiles_tuple_list,
        method_opt,
        basis_set_opt,
        mem_com_opt,
        mem_pbs_opt,
        cluster,
    )
    # monitor_jobs = generateMolecules(smiles_tuple_list, method_opt, basis_set_opt,
    #            mem_com_opt, mem_pbs_opt, cluster)

    add_methods = {
        "methods": ["CAM-B3LYP", "bhandhlyp", "PBE1PBE"],
        "basis_set": ["6-311G(d,p)", "6-311G(d,p)", "6-311G(d,p)"],
        "solvent": ["", "", ""],
        "mem_com": ["1600", "1600", "1600"],
        "mem_pbs": ["10", "10", "10"],
    }
    #    monitor_jobs = ['NL3','NL5','NL12','NL13','ND1','ND2','ND3','AP11','AP14','AP16','AP17','RR6','YZ7','YZ12','YZ15','JD21','C218']
    # monitor_jobs = ['RR6']

    """
    complete = jobResubmit_v2(monitor_jobs, resubmit_delay_min, resubmit_max_attempts,
                           method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                           method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                           #cluster, route='Benchmark/results', add_methods=add_methods,
                           cluster, route='results', add_methods=add_methods,
                           max_queue=200, results_json='results.json',
                           identify_zeros=True, create_smiles=False
    )
    """

    # gather_general_smiles(monitor_jobs)
    with open("results_cp/ds_all3/dyes", "r") as fp:
        ds_all = fp.readlines()
        for i in range(len(ds_all)):
            ds_all[i] = ds_all[i].rstrip()
    print(ds_all)
    gather_excitation_data(
        # "./results_cp/ds_all3",
        "./results",
        ds_all,
        add_methods,
        method_mexc,
        basis_set_mexc,
        results_json="results_exc.json",
        exc_json=True,
    )
    # DS_ALL
    # ds2 = 727 dyes
    # ds1&2 = 1007
    # ds3 = ?
    """
    module load python
    """


if __name__ == "__main__":
    main()

# rsync --update -ra dir1 dir2
