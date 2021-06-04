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
    #print(post_perm[0])        
    
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
    #print("line:", line)

    return line, name, formalName


def generateMolecules (smiles_tuple_list, 
                method_opt, basis_set_opt,
                mem_com_opt, mem_pbs_opt, cluster): 
    #if not os.path.exists("inputs"):
    #    os.mkdir('inputs')
    #print(number_locals)
    #print(smiles_tuple_list)
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
            #print(i)
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

        mol_lst.addMolecule(mol)
        mol_lst.sendToFile("../results.json")
        monitor_jobs.append(name)
        print(monitor_jobs)
    os.chdir("..")
    #print(xyzDict)
    #print(name+";;;"+formalName)
    return monitor_jobs


def submitOpt(monitor_jobs):
    os.chdir('results')
    for i in monitor_jobs:
        os.chdir(i)
        print('qsub in %s' % i)
        cmd = 'qsub mex.pbs'
        subprocess.call(cmd, shell=True)
        os.chdir("..")
    os.chdir('..')

def jobResubmit(monitor_jobs, min_delay, number_delays,
                method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                cluster, route='results'
                ):
    """
    Modified from ice_analog_spectra_generator repo
    """
    mol_lst = MoleculeList()
    if os.path.exists('results.json'):
        print("exists")
        mol_lst.setData("results.json")
    else:
        print("does not exist")
        mol_lst.sendToFile("results.json")

    
    min_delay = min_delay * 60
    cluster_list = glob.glob("%s/*" % route)
    print(cluster_list)
    complete = []
    resubmissions = []
    for i in range(len(monitor_jobs)):
        complete.append(0)
        resubmissions.append(2)
    calculations_complete = False
    # comment change directory below in production
    os.chdir(route)
    for i in range(number_delays):
        # time.sleep(min_delay)
        for num, j in enumerate(monitor_jobs):
            print(j)
            os.chdir(j)
            delay = i
            mexc_check = glob.glob("mexc")
            # print(mexc_check)
            if len(mexc_check) > 0:
                print('{0} entered mexc checkpoint 1'.format(num+1))
                complete[num] = 1
                mexc_check_out = glob.glob("mexc/mexc.o*")
                mexc_check_out_complete = glob.glob('mexc/*_o*')

                if complete[num] != 2 and len(mexc_check_out) > 0 and len(mexc_check_out_complete) > 0:
                    print('{0} entered mexc checkpoint 2'.format(num+1))
                    
                    occVal, virtVal = ES_extraction.ES_extraction('mexc/mexc.out')
                    mol = Molecule()
                    mol.setData('info.json')
                    mol.setHOMO(occVal)
                    mol.setLUMO(virtVal)
                    # Testing below
                    mol.setExictations(absorpt('mexc/mexc.out'))

                    mol.toJSON()
                    mol.sendToFile('info.json')
                    
                    #mol_lst.addMolecule(mol)
                    mol_lst.updateMolecule(mol)
                    #print(mol_lst)
                    mol_lst.sendToFile('../../results.json')

                    complete[num] = 2

            if complete[num] < 1:
                action, resubmissions = error_mexc_dyes_v1.main(
                    num, method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                    method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                    resubmissions, delay, cluster, j
                )
                print(resubmissions)
            
            mexc_check = []
            os.chdir('..')
        stage = 0
        for k in range(len(complete)):
            stage += complete[k]
            if stage == len(complete)*2:
                calculations_complete = True

        if calculations_complete == True:
            print(complete)
            print('\nCalculations are complete.')
            print('Took %.2f hours' % (i*min_delay / 60))
            return complete
        print('Completion List\n', complete, '\n')
        print('delay %d' % (i))
        time.sleep(min_delay)
    return complete


def main():
    """
    print("\n\tstart\n")
    three_types = ["eDonors", "backbones", "eAcceptors"] # Name of subdirectories holding the local structures

    localStructuresDict = collectLocalStructures(three_types) # p
    
    smiles_tuple_list = permutationDict(localStructuresDict)
    """
    
    resubmit_delay_min = 0.01 # 60 * 12
    resubmit_max_attempts = 3

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
    cluster='seq' 
    """
    # comment for testing
    monitor_jobs = generateMolecules(smiles_tuple_list, method_opt, basis_set_opt,
                mem_com_opt, mem_pbs_opt, cluster)
    """

    monitor_jobs = ['1ed_1b_1ea']
    #monitor_jobs = ['1ed_10b_1ea', '1ed_10b_2ea', '1ed_10b_3ea', '1ed_11b_1ea', '1ed_11b_2ea', '1ed_11b_3ea', '1ed_12b_2ea', '1ed_12b_3ea', '1ed_13b_1ea', '1ed_13b_2ea', '1ed_14b_2ea', '1ed_14b_3ea', '1ed_15b_1ea', '1ed_15b_2ea', '1ed_15b_3ea', '1ed_16b_1ea', '1ed_16b_2ea', '1ed_16b_3ea', '1ed_1b_2ea', '1ed_1b_3ea', '1ed_2b_1ea', '1ed_2b_2ea', '1ed_2b_3ea', '1ed_3b_1ea', '1ed_3b_2ea', '1ed_3b_3ea', '1ed_4b_1ea', '1ed_4b_2ea', '1ed_4b_3ea', '1ed_5b_1ea', '1ed_5b_2ea', '1ed_5b_3ea', '1ed_6b_2ea', '1ed_6b_3ea', '1ed_7b_1ea', '1ed_7b_2ea', '1ed_7b_3ea', '1ed_8b_2ea', '1ed_8b_3ea', '1ed_9b_1ea', '1ed_9b_3ea', '2ed_10b_1ea', '2ed_10b_2ea', '2ed_10b_3ea', '2ed_11b_1ea', '2ed_11b_2ea', '2ed_11b_3ea', '2ed_12b_1ea', '2ed_12b_2ea', '2ed_13b_1ea', '2ed_13b_2ea', '2ed_13b_3ea', '2ed_14b_1ea', '2ed_14b_2ea', '2ed_14b_3ea', '2ed_15b_2ea', '2ed_15b_3ea', '2ed_16b_1ea', '2ed_16b_2ea', '2ed_16b_3ea', '2ed_1b_1ea', '2ed_1b_2ea', '2ed_1b_3ea', '2ed_2b_1ea', '2ed_2b_2ea', '2ed_2b_3ea', '2ed_3b_1ea', '2ed_3b_2ea', '2ed_3b_3ea', '2ed_4b_1ea', '2ed_4b_2ea', '2ed_4b_3ea', '2ed_5b_1ea', '2ed_5b_2ea', '2ed_5b_3ea', '2ed_6b_1ea', '2ed_6b_2ea', '2ed_6b_3ea', '2ed_7b_1ea', '2ed_7b_2ea', '2ed_7b_3ea', '2ed_8b_1ea', '2ed_8b_2ea', '2ed_8b_3ea', '2ed_9b_2ea', '3ed_10b_3ea', '3ed_11b_1ea', '3ed_11b_2ea', '3ed_11b_3ea', '3ed_12b_1ea', '3ed_12b_2ea', '3ed_12b_3ea', '3ed_13b_1ea', '3ed_13b_2ea', '3ed_13b_3ea', '3ed_14b_2ea', '3ed_15b_1ea', '3ed_15b_2ea', '3ed_15b_3ea', '3ed_16b_1ea', '3ed_16b_2ea', '3ed_16b_3ea', '3ed_1b_1ea', '3ed_1b_2ea', '3ed_1b_3ea', '3ed_2b_1ea', '3ed_2b_2ea', '3ed_2b_3ea', '3ed_3b_1ea', '3ed_3b_2ea', '3ed_3b_3ea', '3ed_4b_1ea', '3ed_4b_2ea', '3ed_4b_3ea', '3ed_5b_1ea', '3ed_5b_2ea', '3ed_5b_3ea', '3ed_6b_2ea', '3ed_6b_3ea', '3ed_7b_1ea', '3ed_7b_2ea', '3ed_7b_3ea', '3ed_8b_1ea', '3ed_8b_2ea', '3ed_8b_3ea', '3ed_9b_1ea', '3ed_9b_2ea', '3ed_9b_3ea', '5ed_10b_1ea', '5ed_10b_2ea', '5ed_10b_3ea', '5ed_11b_1ea', '5ed_11b_2ea', '5ed_11b_3ea', '5ed_12b_2ea', '5ed_12b_3ea', '5ed_13b_1ea', '5ed_13b_2ea', '5ed_13b_3ea', '5ed_14b_1ea', '5ed_14b_2ea', '5ed_14b_3ea', '5ed_15b_1ea', '5ed_15b_3ea', '5ed_16b_2ea', '5ed_16b_3ea', '5ed_1b_2ea', '5ed_1b_3ea', '5ed_2b_1ea', '5ed_2b_2ea', '5ed_3b_2ea', '5ed_3b_3ea', '5ed_4b_1ea', '5ed_4b_2ea', '5ed_4b_3ea', '5ed_5b_2ea', '5ed_5b_3ea', '5ed_6b_1ea', '5ed_6b_2ea', '5ed_6b_3ea', '5ed_7b_1ea', '5ed_7b_2ea', '5ed_7b_3ea', '5ed_8b_2ea', '5ed_8b_3ea', '5ed_9b_1ea', '5ed_9b_2ea', '5ed_9b_3ea', '6ed_10b_1ea', '6ed_10b_2ea', '6ed_10b_3ea', '6ed_11b_1ea', '6ed_11b_2ea', '6ed_11b_3ea', '6ed_12b_1ea', '6ed_12b_3ea', '6ed_13b_2ea', '6ed_13b_3ea', '6ed_14b_2ea', '6ed_14b_3ea', '6ed_15b_1ea', '6ed_15b_3ea', '6ed_16b_1ea', '6ed_16b_2ea', '6ed_1b_1ea', '6ed_1b_2ea', '6ed_2b_2ea', '6ed_3b_1ea', '6ed_4b_1ea', '6ed_4b_3ea', '6ed_5b_3ea', '6ed_6b_1ea', '6ed_6b_2ea', '6ed_6b_3ea', '6ed_7b_1ea', '6ed_7b_3ea', '6ed_8b_1ea', '6ed_8b_2ea', '6ed_8b_3ea', '6ed_9b_1ea', '6ed_9b_2ea', '7ed_10b_1ea', '7ed_10b_2ea', '7ed_10b_3ea', '7ed_11b_1ea', '7ed_11b_2ea', '7ed_12b_2ea', '7ed_13b_1ea', '7ed_13b_2ea', '7ed_13b_3ea', '7ed_14b_1ea', '7ed_14b_3ea', '7ed_15b_1ea', '7ed_15b_2ea', '7ed_15b_3ea', '7ed_16b_1ea', '7ed_16b_2ea', '7ed_16b_3ea', '7ed_1b_1ea', '7ed_1b_2ea', '7ed_1b_3ea', '7ed_2b_1ea', '7ed_2b_2ea', '7ed_2b_3ea', '7ed_3b_1ea', '7ed_3b_3ea', '7ed_4b_1ea', '7ed_4b_2ea', '7ed_4b_3ea', '7ed_5b_1ea', '7ed_5b_3ea', '7ed_6b_1ea', '7ed_6b_2ea', '7ed_6b_3ea', '7ed_7b_2ea', '7ed_7b_3ea', '7ed_8b_1ea', '7ed_8b_2ea', '7ed_8b_3ea', '7ed_9b_2ea', '7ed_9b_3ea', 'TPA2_10b_1ea', 'TPA2_10b_2ea', 'TPA2_10b_3ea', 'TPA2_11b_2ea', 'TPA2_11b_3ea', 'TPA2_12b_1ea', 'TPA2_12b_2ea', 'TPA2_13b_1ea', 'TPA2_13b_2ea', 'TPA2_13b_3ea', 'TPA2_14b_1ea', 'TPA2_14b_2ea', 'TPA2_14b_3ea', 'TPA2_15b_1ea', 'TPA2_15b_2ea', 'TPA2_15b_3ea', 'TPA2_16b_1ea', 'TPA2_16b_2ea', 'TPA2_16b_3ea', 'TPA2_1b_1ea', 'TPA2_1b_2ea', 'TPA2_1b_3ea', 'TPA2_2b_1ea', 'TPA2_2b_2ea', 'TPA2_2b_3ea', 'TPA2_3b_1ea', 'TPA2_3b_2ea', 'TPA2_3b_3ea', 'TPA2_4b_1ea', 'TPA2_4b_2ea', 'TPA2_4b_3ea', 'TPA2_5b_1ea', 'TPA2_5b_2ea', 'TPA2_5b_3ea', 'TPA2_6b_1ea', 'TPA2_6b_2ea', 'TPA2_6b_3ea', 'TPA2_7b_1ea', 'TPA2_7b_2ea', 'TPA2_7b_3ea', 'TPA2_8b_2ea', 'TPA2_8b_3ea', 'TPA2_9b_1ea', 'TPA2_9b_2ea', 'TPA2_9b_3ea', '2ed_9b_3ea', '7ed_9b_1ea', 'TPA2_4b_3ea', '1ed_12b_1ea', '3ed_10b_2ea', '7ed_5b_2ea', '5ed_15b_2ea', '2ed_12b_3ea', '3ed_1b_1ea', '6ed_5b_1ea', '3ed_14b_3ea', '6ed_15b_2ea', '2ed_2b_3ea', '7ed_7b_1ea', 'TPA2_11b_1ea', '7ed_3b_2ea', 'TPA2_8b_1ea', 'TPA2_1b_1ea', '3ed_2b_2ea', '7ed_11b_3ea', '1ed_5b_2ea', '6ed_7b_2ea']
    submitOpt(monitor_jobs)
    #print(monitor_jobs)
    complete = jobResubmit(monitor_jobs, resubmit_delay_min, resubmit_max_attempts,
                           method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                           method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                           cluster
                           )
    '''
    module load python
    source activate rdkit
    home6/r2532/chem/dyemoleculecata/
    '''
main()

