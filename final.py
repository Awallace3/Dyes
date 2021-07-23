from operator import add
import numpy as np
import os
import itertools
import glob
import subprocess
import time
import sys
import subprocess



sys.path.insert(1, './src') # this adds src to python path at runtime for modules
import error_mexc_dyes_v1
import error_mexc_dyes_v2
import ES_extraction
from absorpt import absorpt
from molecule_json import Molecule
from molecule_json import MoleculeList
# requires obabel installed...
    # brew install obabel
    # conda install -c openbabel openbabel

def collectLocalStructures (subdirectories):
    localStructuresDict = {}
    number_locals = 0
    
    for num, i in enumerate(subdirectories):
        os.chdir(i)
        localStructuresDict['local{0}'.format(num+1)] = []
        localSmiles = glob.glob('*.smi')
        for j in localSmiles:
            with open(j) as f:
                smiles = f.read()
                smiles = smiles.split("\n")
                smiles[0] = smiles[0].rstrip()
                localStructuresDict['local{0}'.format(num+1)].append((smiles[0], j[:-4], smiles[1]))
                #  smiles[0]==smiles, j[:-4]==local_name, smiles[1]==name

        
        os.chdir("..")
        number_locals += 1
    print(localStructuresDict)
    
    return localStructuresDict

def permutationDict(localStructuresDict):

    pre_perm = []

    for key, value in localStructuresDict.items():
        pre_perm = pre_perm + [value]

    post_perm = list(itertools.product(*pre_perm))
    
    return post_perm

def smilesRingCleanUp(f, s, t):
    combinedString = ''
    current_val = 0
    lst1 = []
    claimed = []
    double = []
    smi1, na1, form1 = f
    smi2, na2, form2 = s
    smi3, na3, form3 = t
    name = na1 + "_" + na2 + "_" + na3
    formalName = form1 +"::"+form2+"::"+form3
    print(name)
    smi1 = smi1.replace("1", "7")
    smi1 = smi1.replace("2", "6")
    smi2 = smi2.replace("1", "5")
    smi2 = smi2.replace("2", "4")
    line = smi1 + "." + smi2 + "." + smi3

    return line, name, formalName


def generateMolecules (smiles_tuple_list, 
                method_opt, basis_set_opt,
                mem_com_opt, mem_pbs_opt, cluster): 
    #if not os.path.exists("inputs"):
    #    os.mkdir('inputs')
    xyzDict = {}
    monitor_jobs = []
    if not os.path.exists('results'):
        os.mkdir('results')
    if not os.path.exists('results/smiles_input'):
        os.mkdir('results/smiles_input')
    
    os.chdir('results')
    
    for num, i in enumerate(smiles_tuple_list):
        first, second, third = i
        line, name, formalName = smilesRingCleanUp(first, second, third)

        # CHECK LOCATION

        mol_lst = MoleculeList()
        if os.path.exists('../results.json'):
            mol_lst.setData("../results.json")
        else:
            print("Creating results.json\n")
            mol_lst.sendToFile("../results.json")

        if mol_lst.checkMolecule(line):
            print('\nMolecule already exists and the name smiles is... \n%s\n' % line)
            continue
        mol = Molecule()
        mol.setSMILES(line)
        
        print("line{0}:".format(num), line)
        line = line.replace("BBA", "9")
        line = line.replace("BBD", "8")
        print("line{0}:".format(num), line)
        file = open('smiles_input/{0}.smi'.format(name), 'w+')
        file.write(line)
        file.close()
        
        cmd = "obabel -ismi smiles_input/{0}.smi -oxyz --gen3D".format(name)
        carts = subprocess.check_output(cmd, shell=True)
        #subprocess.call(cmd, shell=True)
        carts = str(carts)
        carts = carts.rstrip()
        
        carts = carts.splitlines()
        
        for n, i in enumerate(carts):
            carts[n] = i.split('\\n')

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

        print(carts_cleaned)
        os.mkdir(name)
        err = subprocess.call("touch %s/info.json" % name, shell=True)

        mol.setName(name)
        mol.setParts(formalName)
        mol.setLocalName(name)
        mol.sendToFile('%s/info.json' % name)

        data = ''
        for line in carts_cleaned:
            data += line+'\n'
            
        error_mexc_dyes_v1.gaussianInputFiles(
                    0, method_opt, 
                    basis_set_opt, mem_com_opt, 
                    mem_pbs_opt, cluster, 
                    baseName='mex', procedure='OPT', data=data,
                    dir_name=name
        )

        # need to add qsub here for v2

        mol_lst.addMolecule(mol)
        mol_lst.sendToFile("../results.json")
        monitor_jobs.append(name)
        print(monitor_jobs)
    os.chdir("..")
    return monitor_jobs


def submitOpt(monitor_jobs):
    os.chdir('results')
    for i in monitor_jobs:
        os.chdir(i)
        cmd = 'qsub mex.pbs'
        subprocess.call(cmd, shell=True)
        os.chdir("..")
    os.chdir('..')

def add_excitation_data(
        dir_name, baseName,
        method_mexc, basis_set_mexc,

    ):
    occVal, virtVal = ES_extraction.ES_extraction('%s/%s.out' % (dir_name, baseName))
    if occVal == virtVal and occVal == 0:
        print('failed to add')
        return 0, 0
    mol = Molecule()
    mol.setData('info.json')
    mol.setHOMO(occVal)
    mol.setLUMO(virtVal)
    mol.appendExcitations(absorpt('mexc/mexc.out', method_mexc, basis_set_mexc))
    mol.toJSON()
    mol.sendToFile('info.json')
    mol_lst = MoleculeList()
    mol_lst.setData("../../results.json")
    mol_lst.updateMolecule(mol)
    mol_lst.sendToFile('../../results.json')


def jobResubmit(monitor_jobs, min_delay, number_delays,
                method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                cluster, route='results',
                add_methods= {
                    "methods" : [],
                    "basis_set" : [],
                    "mem_com" : [],
                    "mem_pbs" : []
                }
                ):
    """
    Modified from ice_analog_spectra_generator repo
    """
    add_methods_length = len(add_methods['methods'])

    if add_methods_length != len(add_methods['basis_set']) and add_methods_length != len(add_methods['mem_com']) and add_methods_length != len(add_methods['mem_pbs']):
        print("add_methods must have values that have lists of the same length.\nTerminating jobResubmit before start")
        return []
    resubmission_max = add_methods_length
        
    mol_lst = MoleculeList()
    if os.path.exists('results.json'):
        mol_lst.setData("results.json")
    else:
        mol_lst.sendToFile("results.json")

    
    min_delay = min_delay * 60
    #cluster_list = glob.glob("%s/*" % route)
    complete = []
    resubmissions = []
    for i in range(len(monitor_jobs)):
        complete.append(0)
        resubmissions.append(2)
        #resubmissions.append(resubmission_max)
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
                mexc_check_out_complete = glob.glob('mexc/*_o*')

                #if complete[num] != 2 and len(mexc_check_out) > 0 and len(mexc_check_out_complete) > 0:
                if complete[num] < 2 and len(mexc_check_out) > 0 and len(mexc_check_out_complete) > 0:
                    
                    occVal, virtVal = ES_extraction.ES_extraction('mexc/mexc.out')
                    if occVal == virtVal and occVal == 0:
                        print(j)
                    mol = Molecule()
                    mol.setData('info.json')
                    mol.setHOMO(occVal)
                    mol.setLUMO(virtVal)
                    # Testing below
                    mol.setExictations(absorpt('mexc/mexc.out', method_mexc, basis_set_mexc))
                    
                    mol.toJSON()
                    mol.sendToFile('info.json')
                     
                    #mol_lst.addMolecule(mol)
                    mol_lst = MoleculeList()
                    mol_lst.setData("../../results.json")
                    mol_lst.updateMolecule(mol)
                    mol_lst.sendToFile('../../results.json')
                    
                    complete[num] = 2

                #if complete[num] >= 2


            if complete[num] < 1:
                print("directory for", j)
                action, resubmissions = error_mexc_dyes_v1.main(
                    num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                    method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                    resubmissions, delay, cluster, j, xyzSmiles=True
                )
            elif complete[num] == 2:
                pos = complete[num] - 2
                action, resubmissions = error_mexc_dyes_v1.main(
                    num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                    add_methods["methods"][pos], add_methods['basis_set'][pos],
                    add_methods["mem_com"][pos], add_methods["mem_pbs"][pos],
                    resubmissions, delay, cluster, j, xyzSmiles=False
                )
                
             
            pos = complete[num] - 2
            if pos >= 0:
                dir_name = add_methods['methods'][pos].lower()
                mexc_check_out = glob.glob("%s/mexc.o*" % dir_name)
                mexc_check_out_complete = glob.glob('%s/*_o*' % dir_name)
                if complete[num] < 3 and len(mexc_check_out) >0 and len (mexc_check_out_complete) > 0:
                    add_excitation_data(dir_name, 'mexc', add_methods['methods'][pos], add_methods['basis_set'][pos])
            
            mexc_check = []
            if complete[num] < 2:
                print(complete[num], i)
                print(j)
            os.chdir('..')
        stage = 0
        for k in range(len(complete)):
            stage += complete[k]
            #if stage == len(complete)*2:
            if stage == len(complete)*add_methods_length:
                calculations_complete = True

        if calculations_complete == True:
            print(complete)
            print('\nCalculations are complete.')
            print('Took %.2f hours' % (i*min_delay / 60))
            return complete
        print('Completion List\n', complete, '\n')
        print('delay %d' % (i))
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
    ln = len(add_methods['methods'])
    if ln == len(add_methods['basis_set']) and ln == len(add_methods['mem_com']) and ln == len(add_methods['mem_pbs']):
        return True 
    else:
        print("\nadd_methods must have values that have lists of the same length.\nTerminating %s before start\n" % funct_name)
        return False 

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


def add_qsub_dir(qsub_dir, geom_dir):
    if qsub_dir == 'None':
        return 0
    elif qsub_dir == './':
        qsub_path = geom_dir
    else:
        qsub_path = "%s/%s" % (geom_dir, qsub_dir)
    with open('../qsub_queue', 'a') as fp:
        fp.write(qsub_path)
    return 1

def qsub_to_max(max_queue=100, user=""):
    with open("../qsub_queue", 'r') as fp:
        qsubs = fp.readlines()

    cmd = "qstat -u \"r%s\" > ../qsub_len" % user
    subprocess.call(cmd, shell=True)
    with open('../qsub_len', 'r') as fp:
        current_queue = len(fp.readlines())-5
    dif = max_queue - current_queue
    if dif > 0:
        cnt = 0
        while (cnt < dif and len(qsubs) > 0):
            qsub_path = qsubs.pop(0)
            qsub(qsub_path)
            cnt +=1
    with open('../qsub_queue', 'w') as fp:
        for i in qsubs:
            fp.write(i)
    return 1



def jobResubmit_v2(monitor_jobs, min_delay, number_delays,
                method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                cluster, route='results',
                add_methods= {
                    "methods" : [],
                    "basis_set" : [],
                    "mem_com" : [],
                    "mem_pbs" : []
                },
                max_queue=200
                ):
    """
    Modified from jobResubmit above
    """
    if not os.path.exists("qsub_queue"):
        subprocess.call("touch qsub_queue", shell=True)
    
    if not check_add_methods(add_methods, "jobResubmit_v2"):
        return []

    add_methods_length = len(add_methods['methods'])
    mol_lst = MoleculeList()
    if os.path.exists('results.json'):
        mol_lst.setData("results.json")
    else:
        mol_lst.sendToFile("results.json")

    
    min_delay = min_delay * 60
    #cluster_list = glob.glob("%s/*" % route)
    complete = []
    resubmissions = []
    for i in range(len(monitor_jobs)):
        complete.append(0)
        resubmissions.append(2)
        #resubmissions.append(resubmission_max)
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
                mexc_check_out_complete = glob.glob('mexc/*_o*')
                if complete[num] < 2 and len(mexc_check_out) > 0 and len(mexc_check_out_complete) > 0:
                    occVal, virtVal = ES_extraction.ES_extraction('mexc/mexc.out')
                    if occVal == virtVal and occVal == 0:
                        print(j)
                    mol = Molecule()
                    mol.setData('info.json')
                    mol.setHOMO(occVal)
                    mol.setLUMO(virtVal)
                    # Testing below
                    mol.setExictations(absorpt('mexc/mexc.out', method_mexc, basis_set_mexc))
                    
                    mol.toJSON()
                    mol.sendToFile('info.json')
                     
                    #mol_lst.addMolecule(mol)
                    mol_lst = MoleculeList()
                    mol_lst.setData("../../results.json")
                    mol_lst.updateMolecule(mol)
                    mol_lst.sendToFile('../../results.json')
                    
                    complete[num] = 2

                #if complete[num] >= 2

            if complete[num] < 1:
                print("directory for", j)
                action, resubmissions, qsub_dir = error_mexc_dyes_v2.main(
                    num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                    method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                    resubmissions, delay, cluster, j, xyzSmiles=True
                )
                add_qsub_dir(qsub_dir, j)
                for pos in range(add_methods_length):
                    action, resubmissions, qsub_dir = error_mexc_dyes_v2.main(
                        num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                        add_methods["methods"][pos], add_methods['basis_set'][pos],
                        add_methods["mem_com"][pos], add_methods["mem_pbs"][pos],
                        resubmissions, delay, cluster, j, xyzSmiles=False
                    )
                    add_qsub_dir(qsub_dir, j)
            

            mexc_check = []
            os.chdir('..')
        stage = 0
        for k in range(len(complete)):
            stage += complete[k]
            #if stage == len(complete)*2:
            if stage == len(complete)*add_methods_length:
                calculations_complete = True

        if calculations_complete == True:
            print(complete)
            print('\nCalculations are complete.')
            print('Took %.2f hours' % (i*min_delay / 60))
            return complete
        print('Completion List\n', complete, '\n')
        print('delay %d' % (i))
        """
        qsub_funct
        """
        qsub_to_max(max_queue, 'r2652')
        time.sleep(min_delay)
    for i in range(len(resubmissions)):
        if resubmissions[i] < 2:
            print("Not finished %d: %s" % (resubmissions[i], monitor_jobs[i]))
    os.chdir("..")
    return complete

def gather_general_smiles(monitor_jobs, path_results='./results'):
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
            if t =='t':
                t = 1
            else:
                t = int(t)
            if t > highest:
                t = highest
                last_out = out_files[i]
        with open(last_out, 'r') as fp:
            lines = fp.readlines()
        error_mexc_dyes_v1.find_geom(lines, error=False, filename=last_out,
                                    imaginary=False, geomDirName=i
        )

        os.chdir('..')



def gather_excitation_data(path_results, monitor_jobs, add_methods, 
    method_mexc, basis_set_mexc, baseName='mexc'
    ):
    if not check_add_methods(add_methods, "gather_excitation_data"):
        return 
    os.chdir(path_results)
    failed = []
    for i in monitor_jobs:
        os.chdir(i)
        if not os.path.exists('mexc/mexc.out'):
            print(i, 'does not have mexc/mexc.out')
            os.chdir("..")
            continue
        occVal, virtVal = ES_extraction.ES_extraction('mexc/mexc.out')
        if occVal == virtVal and occVal == 0:
            print(i, "no data found in mexc/mexc.out\n")
            failed.append(i)
            os.chdir("..")
            continue
        mol = Molecule()
        mol.setData('info.json')
        mol.setHOMO(occVal)
        mol.setLUMO(virtVal)
        excitations = absorpt('mexc/mexc.out', method_mexc, basis_set_mexc)
        if excitations == []:
            if i not in failed:
                failed.append(i)
                print(i, '\n')
            os.chdir("..")
            continue
        mol.setExictations(excitations)
        
        methods_len = len(add_methods['methods'])
        try:
            for j in range(methods_len):
                method = add_methods['methods'][j]
                basis_set = add_methods['basis_set'][j]
                
                mol.appendExcitations(absorpt('%s/%s.out' % (method.lower(), baseName), method, basis_set))
        except:
            failed.append(i)



        mol.toJSON()
        #mol.sendToFile('info.json')
        mol_lst = MoleculeList()
        mol_lst.setData("../../results.json")
        mol_lst.updateMolecule(mol)
        mol_lst.sendToFile('../../results.json')
    

        os.chdir("..")
    print("FAILED:", failed)
    return True

def main():
    """
    print("\n\tstart\n")
    three_types = ["eDonors", "backbones", "eAcceptors"] # Name of subdirectories holding the local structures

    localStructuresDict = collectLocalStructures(three_types) # p
    
    smiles_tuple_list = permutationDict(localStructuresDict)
    """
    
    #resubmit_delay_min = 60 * 12
    #resubmit_max_attempts = 5
    resubmit_delay_min = 0.01 # 60 * 12
    resubmit_max_attempts = 1

    # geometry optimization options
    method_opt = "B3LYP"
    #method_opt = "HF"
    basis_set_opt = "6-311G(d,p)"
    #basis_set_opt = "6-31G"
    mem_com_opt = "1600"  # mb
    mem_pbs_opt = "10"  # gb

    # TD-DFT options
    method_mexc = "CAM-B3LYP"
    basis_set_mexc = "6-311G(d,p)"
    mem_com_mexc = "1600"  # mb
    mem_pbs_mexc = "10"  # gb"
    cluster='map'
    #cluster='seq'

    add_methods = {
        "methods" : ["PBE1PBE"],
        "basis_set" : ["6-311G(d,p)"],
        "mem_com" : ["1600"],
        "mem_pbs" : ["10"]
    }
    add_methods = {
        "methods" : ["bhandhlyp"],
        "basis_set" : ["6-311G(d,p)"],
        "mem_com" : ["1600"],
        "mem_pbs" : ["10"]
    }
    """
    """
    add_methods = {
        "methods" : ["bhandhlyp", "PBE1PBE"],
        "basis_set" : ["6-311G(d,p)", "6-311G(d,p)"],
        "mem_com" : ["1600", "1600"],
        "mem_pbs" : ["10", "10"]
    }




    """
    # comment for testing
    monitor_jobs = generateMolecules(smiles_tuple_list, method_opt, basis_set_opt,
                mem_com_opt, mem_pbs_opt, cluster)
    """
    monitor_jobs =  ['3ed_11b_3ea', 'TPA2_4b_2ea', '7ed_6b_3ea', '6ed_6b_3ea', '7ed_14b_3ea', '5ed_7b_1ea', '5ed_14b_1ea', '2ed_13b_1ea', 'TPA2_14b_3ea', '1ed_3b_2ea', '6ed_16b_1ea', '1ed_11b_1ea', '3ed_13b_2ea', 'TPA2_6b_3ea', '7ed_4b_2ea', '7ed_16b_2ea', '6ed_4b_2ea', '1ed_1b_3ea', '1ed_9b_1ea', '3ed_8b_3ea', '2ed_8b_3ea', 'TPA2_16b_2ea', '3ed_15b_1ea', '7ed_2b_1ea', '6ed_2b_1ea', '7ed_10b_1ea', '5ed_3b_3ea', 'TPA2_8b_2ea', '5ed_10b_3ea', '1ed_15b_3ea', '2ed_6b_2ea', '3ed_6b_2ea', 'TPA2_10b_1ea', '6ed_12b_3ea', '5ed_1b_2ea', '6ed_8b_2ea', '7ed_8b_2ea', 'TPA2_2b_1ea', '2ed_15b_2ea', '5ed_12b_2ea', '6ed_10b_2ea', '1ed_5b_1ea', '2ed_4b_3ea', '3ed_4b_3ea', '6ed_11b_2ea', '1ed_4b_1ea', '2ed_5b_3ea', '3ed_5b_3ea', '1ed_16b_2ea', '5ed_13b_2ea', '2ed_14b_2ea', 'TPA2_3b_1ea', '6ed_9b_2ea', '7ed_9b_2ea', '2ed_7b_2ea', '3ed_7b_2ea', 'TPA2_11b_1ea', '6ed_13b_3ea', '1ed_14b_3ea', '5ed_11b_3ea', '2ed_16b_3ea', 'TPA2_9b_2ea', '7ed_3b_1ea', '6ed_3b_1ea', '7ed_11b_1ea', '5ed_2b_3ea', '3ed_14b_1ea', '1ed_8b_1ea', '3ed_9b_3ea', '2ed_1b_1ea', '3ed_1b_1ea', '2ed_9b_3ea', '7ed_5b_2ea', '6ed_5b_2ea', 'TPA2_7b_3ea', '3ed_12b_2ea', '1ed_10b_1ea', 'TPA2_15b_3ea', '1ed_2b_2ea', '2ed_12b_1ea', '5ed_15b_1ea', '7ed_7b_3ea', '6ed_7b_3ea', '7ed_15b_3ea', '5ed_6b_1ea', 'TPA2_5b_2ea', '3ed_10b_3ea', '3ed_13b_1ea', '6ed_4b_1ea', '7ed_16b_1ea', '7ed_4b_1ea', '5ed_5b_3ea', '2ed_11b_3ea', '5ed_16b_3ea', '1ed_13b_3ea', 'TPA2_16b_1ea', '1ed_9b_2ea', '6ed_14b_3ea', '5ed_7b_2ea', 'TPA2_4b_1ea', '2ed_13b_2ea', '5ed_14b_2ea', '1ed_11b_2ea', '6ed_16b_2ea', '1ed_3b_1ea', '3ed_2b_3ea', '2ed_2b_3ea', 'TPA2_2b_2ea', '7ed_12b_3ea', '7ed_8b_1ea', '6ed_8b_1ea', '5ed_1b_1ea', '5ed_9b_3ea', '5ed_12b_1ea', '2ed_15b_1ea', 'TPA2_12b_3ea', '1ed_5b_2ea', '6ed_10b_1ea', '3ed_15b_2ea', 'TPA2_8b_1ea', '7ed_10b_2ea', '6ed_2b_2ea', '7ed_2b_2ea', '1ed_7b_3ea', 'TPA2_10b_2ea', '3ed_6b_1ea', '2ed_6b_1ea', '1ed_6b_3ea', 'TPA2_11b_2ea', '3ed_7b_1ea', '2ed_7b_1ea', '7ed_11b_2ea', '6ed_3b_2ea', '7ed_3b_2ea', 'TPA2_9b_1ea', 'TPA2_1b_3ea', '3ed_14b_2ea', '1ed_16b_1ea', 'TPA2_13b_3ea', '1ed_4b_2ea', '6ed_11b_1ea', '2ed_14b_1ea', '5ed_13b_1ea', '6ed_1b_3ea', '7ed_13b_3ea', '7ed_9b_1ea', '6ed_9b_1ea', '7ed_1b_3ea', '5ed_8b_3ea', 'TPA2_3b_2ea', '3ed_16b_3ea', '1ed_2b_1ea', '3ed_3b_3ea', '2ed_3b_3ea', '1ed_10b_2ea', '5ed_15b_2ea', '2ed_12b_2ea', 'TPA2_5b_1ea', '5ed_6b_2ea', '3ed_1b_2ea', '2ed_1b_2ea', '1ed_8b_2ea', '6ed_15b_3ea', '1ed_12b_3ea', '2ed_10b_3ea', '6ed_5b_1ea', '7ed_5b_1ea', '5ed_4b_3ea', '3ed_12b_1ea', '3ed_8b_1ea', '2ed_8b_1ea', '6ed_14b_2ea', '1ed_1b_1ea', '1ed_9b_3ea', '1ed_13b_2ea', '5ed_16b_2ea', '2ed_11b_2ea', 'TPA2_6b_1ea', '5ed_5b_2ea', '6ed_16b_3ea', '2ed_2b_2ea', 'TPA2_14b_1ea', '3ed_2b_2ea', '1ed_11b_3ea', '5ed_14b_3ea', '2ed_13b_3ea', '5ed_7b_3ea', '7ed_6b_1ea', '7ed_14b_1ea', '6ed_6b_1ea', '3ed_11b_1ea', '2ed_4b_1ea', 'TPA2_12b_2ea', '3ed_4b_1ea', '1ed_5b_3ea', '7ed_12b_2ea', '5ed_9b_2ea', 'TPA2_2b_3ea', '1ed_15b_1ea', '1ed_7b_2ea', '6ed_12b_1ea', 'TPA2_10b_3ea', '5ed_10b_1ea', '5ed_3b_1ea', '7ed_2b_3ea', '7ed_10b_3ea', '6ed_2b_3ea', '3ed_15b_3ea', '3ed_14b_3ea', 'TPA2_1b_2ea', '5ed_2b_1ea', '7ed_3b_3ea', '7ed_11b_3ea', '6ed_3b_3ea', '5ed_11b_1ea', '2ed_16b_1ea', '1ed_6b_2ea', '6ed_13b_1ea', 'TPA2_11b_3ea', '1ed_14b_1ea', '3ed_16b_2ea', 'TPA2_3b_3ea', '7ed_1b_2ea', '6ed_1b_2ea', '7ed_13b_2ea', '5ed_8b_2ea', '2ed_5b_1ea', 'TPA2_13b_2ea', '3ed_5b_1ea', '1ed_4b_3ea', '3ed_10b_1ea', '5ed_6b_3ea', '7ed_7b_1ea', '7ed_15b_1ea', '6ed_7b_1ea', '2ed_12b_3ea', '5ed_15b_3ea', '1ed_10b_3ea', '2ed_3b_2ea', 'TPA2_15b_1ea', '3ed_3b_2ea', '5ed_4b_2ea', 'TPA2_7b_1ea', '2ed_10b_2ea', '1ed_12b_2ea', '3ed_9b_1ea', '2ed_1b_3ea', '3ed_1b_3ea', '2ed_9b_1ea', '6ed_15b_2ea', '1ed_8b_3ea', '3ed_2b_1ea', 'TPA2_14b_2ea', '2ed_2b_1ea', '1ed_3b_3ea', '6ed_6b_2ea', '7ed_14b_2ea', '7ed_6b_2ea', 'TPA2_4b_3ea', '3ed_11b_2ea', '1ed_13b_1ea', '1ed_1b_2ea', '6ed_14b_1ea', '2ed_8b_2ea', 'TPA2_16b_3ea', '3ed_8b_2ea', '2ed_11b_1ea', '5ed_16b_1ea', '5ed_5b_1ea', '7ed_16b_3ea', '6ed_4b_3ea', '7ed_4b_3ea', 'TPA2_6b_2ea', '3ed_13b_3ea', '3ed_6b_3ea', '2ed_6b_3ea', '6ed_12b_2ea', '1ed_7b_1ea', '1ed_15b_2ea', '5ed_10b_2ea', 'TPA2_8b_3ea', '5ed_3b_2ea', '6ed_10b_3ea', '3ed_4b_2ea', 'TPA2_12b_1ea', '2ed_4b_2ea', '5ed_12b_3ea', '2ed_15b_3ea', '5ed_1b_3ea', '5ed_9b_1ea', '7ed_12b_1ea', '7ed_8b_3ea', '6ed_8b_3ea', '3ed_16b_1ea', '5ed_8b_1ea', '7ed_13b_1ea', '6ed_1b_1ea', '7ed_9b_3ea', '6ed_9b_3ea', '7ed_1b_1ea', '2ed_14b_3ea', '5ed_13b_3ea', '1ed_16b_3ea', '6ed_11b_3ea', '3ed_5b_2ea', 'TPA2_13b_1ea', '2ed_5b_2ea', '5ed_2b_2ea', 'TPA2_9b_3ea', 'TPA2_1b_1ea', '2ed_16b_2ea', '5ed_11b_2ea', '1ed_14b_2ea', '3ed_7b_3ea', '2ed_7b_3ea', '6ed_13b_2ea', '1ed_6b_1ea', '3ed_12b_3ea', 'TPA2_7b_2ea', '5ed_4b_1ea', '6ed_5b_3ea', '7ed_5b_3ea', '2ed_10b_1ea', '6ed_15b_1ea', '2ed_9b_2ea', '3ed_9b_2ea', '1ed_12b_1ea', '3ed_10b_2ea', 'TPA2_5b_3ea', '6ed_7b_2ea', '7ed_15b_2ea', '7ed_7b_2ea', '3ed_3b_1ea', 'TPA2_15b_2ea', '2ed_3b_1ea', '1ed_2b_3ea']

    #monitor_jobs = ['7ed_5b_2ea', '7ed_1b_3ea', '3ed_1b_3ea']

    """
    complete = jobResubmit(monitor_jobs, resubmit_delay_min, resubmit_max_attempts,
                           method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                           method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                           cluster, route='results', add_methods=add_methods
                           )
    """
    monitor_jobs = ['test_1',]
    complete = jobResubmit_v2(monitor_jobs, resubmit_delay_min, resubmit_max_attempts,
                           method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                           method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                           cluster, route='results', add_methods=add_methods,
                           max_queue=200
    )
    

    """
    #tmp.qsub file for listings
    #path/to/qsub/file/

    # comment out qsub in error_mexc_dyes_v1.py    
    return bool, resubmissions, qsub_dir
    # in resubmit
    bool, resubmissions, qsub_dir
    * use queue data structure
    qsub_list.enque(qsub_dir)

    # call function in job_resubmit on sleep time
    cmd = 'qstat -u \"user_var\" > tmp.qstat'
    subprocess.call(cmd, shell=True)
    with open('tmp.qstat', 'r') as fp:
        running = fp.readlines()[-1:0]
        running_tot = (len(fp.readlines()) - 5)

    for i in range(max_qsub - running):
        qsub_path = qsub_list.dequeue()
        qsub(qsub_path)
    """
    
    #gather_general_smiles(monitor_jobs)
    
    gather_excitation_data('./results', monitor_jobs, add_methods, method_mexc, basis_set_mexc)
    '''
    module load python
    source activate rdkit
    home6/r2532/chem/dyemoleculecata/
    '''
main()

# rsync --update -ra dir1/ dir2