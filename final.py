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
                #print(smiles)
                smiles[0] = smiles[0].rstrip()
                #smiles = smiles.rstrip()

                #print(j[:-4])
                localStructuresDict['local{0}'.format(num+1)].append((smiles[0], j[:-4], smiles[1]))

        os.chdir("..")
        number_locals += 1
    #print(localStructuresDict)
    
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
    """
    for n, ch in enumerate(f):
        if ch.isnumeric():
            #print(ch)
            lst1.append([int(ch), n, 1])
    for n, ch in enumerate(s):
        if ch.isnumeric():
            #print(ch)
            lst1.append([int(ch), n, 2])
    for n, ch in enumerate(t):
        if ch.isnumeric():
            #print(ch)
            lst1.append([int(ch), n, 3])
    
    for i in range(len(lst1)):
        if st1[i][0] not in claimed:
            claimed.append(st1[i][0])
            double.append(st1[i][0])
        else:
            if st1[i][0] in double:
                continue

    """
    #print(lst1)
    #print(claimed)

    return line, name, formalName


def generateMolecules (smiles_tuple_list): 
    if not os.path.exists("inputs"):
        os.mkdir('inputs')
    #print(number_locals)
    #print(smiles_tuple_list)
    xyzDict = {}
    monitor_jobs = []

    for num, i in enumerate(smiles_tuple_list):
        #if num > 1:
        #    return xyzDict
        #print(i)
        first, second, third = i
        print(first, second, third)
        line, name, formalName = smilesRingCleanUp(first, second, third)

        exists = os.path.isdir("inputs/" + name)
        if exists:
            print("directory already exists for inputs/%s or called %s\n" % (name, formalName))
            continue
        else:
            print("making a new directory for %s or called %s\n" % (name, formalName))
            #print(name)
         
            

        #first = first.replace("1", "7")
        #first = first.replace("2", "6")
        #second = second.replace("1", "5")
        #second = second.replace("2", "4")
        #line = first + "." + second + "." + third
        #print(line)
        #print(num)
        print("line{0}:".format(num), line)
        line = line.replace("BBA", "9")
        line = line.replace("BBD", "8")
        print("line{0}:".format(num), line)
        if not os.path.exists('results'):
            os.mkdir('results')
        file = open('results/{0}.smi'.format(name), 'w+')
        file.write(line)
        file.close()
        
        #cmd = "obabel -ismi results/smiles{0}.smi -oxyz output.xyz --gen3D".format(num+1)
        cmd = "obabel -ismi results/{0}.smi -oxyz --gen3D".format(name)
        ### To generate Pictures 
       # smipic = "obabel results/{0}.smi -O results/{0}.png".format(name)
        carts = subprocess.check_output(cmd, shell=True)
        subprocess.call(cmd, shell=True)
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
        xyzDict["{0}".format(name+";;;"+formalName)] = carts_cleaned
        monitor_jobs.append(name)
        print(monitor_jobs)
        print('loop')
    #print(xyzDict)
    #print(name+";;;"+formalName)
    return xyzDict, monitor_jobs

"""
def writeInputFiles (xyzDict):
    os.chdir("inputs")
    for key, value in xyzDict.items():
        os.mkdir(key)
        file = open( key + "/" + key, 'w+')
        for line in value:
            file.write(line)
            file.write("\n")
        file.close()
    return
"""

def writeInputFiles (xyzDict, method_opt, basis_set_opt):
    if not os.path.exists("inputs"):
        os.mkdir('inputs')
    os.chdir("inputs")
    
    for key, value in xyzDict.items():
        nameSplit = key.split(";;;")
        name = nameSplit[0]
        formalName = nameSplit[1]

        print(nameSplit)
        os.mkdir(name)
        err = subprocess.call("touch %s/info.json" % name, shell=True)
        mol = Molecule()
        mol.setName(name)
        mol.setParts(formalName)
        mol.setLocalName(name)
        mol.sendToFile('%s/info.json' % name)
        subprocess.call("touch " + name + "/" + formalName, shell=True)
        #file = open(name + "/" + formalName, "w+")
        #file.write(' ')
        #file.close()

        """
        Add image depictions
        value in this loop is going to be each molecules cartesian coordinates
        """
        #cmd = "obabel ../results/" + name + ".smi -O {0}/".format(name) + name + ".png"
        #carts = subprocess.check_output(cmd, shell=True)
        data = ''
        for line in value:
            data += line+'\n'
            

        error_mexc_dyes_v1.gaussianInputFiles(
                    0, method_opt, 
                    basis_set_opt, mem_com_opt, 
                    mem_pbs_opt, cluster, 
                    baseName=name, procedure='OPT', data=data 
        )
        '''
        file = open( name + "/mex.com", 'w+')
        file.write("")
        file.write("#N %s/%s OPT \n" % (method_opt, basis_set_opt))
        file.write("\n")
        file.write("{0}\n\n".format(formalName))
        file.write("0 1\n")
        for line in value:
            file.write(line)
            file.write("\n")
        file.write(" " + "\n")
#   file.write(#"name of electron donor:" + 1ed.smi + name\n)
#   file.write(#"name of backbone: " + 1ea.smi + name\n)
#   file.write(#"name of electron acceptor: " + 1ea.smi + name\n)
        file.close()

        file = open( name + "/mex.pbs", 'w+')   #pbs for sequoia
        file.write("#!/bin/sh")
        file.write("\n")
        file.write("#PBS -N " + str(name))
        file.write("\n")
        file.write("#PBS -S /bin/sh")
        file.write("\n")
        file.write("#PBS -j oe")
        file.write("\n")
        file.write("#PBS -m abe")
        file.write("\n")
        file.write("#PBS -l cput=4000:00:00")
        file.write("\n")
        file.write("#PBS -l mem=10gb")
        file.write("\n")
        file.write("#PBS -l nodes=1:ppn=1")
        file.write("\n")
        file.write("#PBS -l file=100gb")
        file.write("\n")
        file.write("")
        file.write("\n")
        file.write("export g09root=/usr/local/apps/")
        file.write("\n")
        file.write(". $g09root/g09/bsd/g09.profile")
        file.write("\n")
        file.write("")
        file.write("\n")
        file.write("scrdir=/tmp/bnp.$PBS_JOBID")
        file.write("\n")
        file.write("mkdir -p $scrdir")
        file.write("\n")
        file.write("export GAUSS_SCRDIR=$scrdir")
        file.write("\n")
        file.write("export OMP_NUM_THREADS=1")
        file.write("\n")
        file.write("")
        file.write("printf 'exec_host = '")
        file.write("\n")
        file.write("head -n 1 $PBS_NODEFILE")
        file.write("\n")
        file.write("")
        file.write("\n")
        file.write("cd $PBS_O_WORKDIR")
        file.write("\n")
        file.write("/usr/local/apps/bin/g09setup " +" mex.com mex.out")
        file.close()
        os.chdir(name)
        print(os.getcwd())
        #os.system('qsub mex.pbs')
        os.chdir('..')
        '''
    
    os.chdir('..')
        
    return

def jobResubmit(monitor_jobs, min_delay, number_delays,
                method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
                method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
                cluster
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
    cluster_list = glob.glob("inputs/*")
    print(cluster_list)
    complete = []
    resubmissions = []
    for i in range(len(monitor_jobs)):
        complete.append(0)
        resubmissions.append(2)
    calculations_complete = False
    # comment change directory below in production
    os.chdir('inputs')
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
                mexc_check_out_complete = glob.glob('mexc/mexc_o*')
                

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
                    resubmissions, delay, cluster
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
    
    '''
    print("\n\tstart\n")
    three_types = ["eDonors", "backbones", "eAcceptors"] # Name of subdirectories holding the local structures

    localStructuresDict = collectLocalStructures(three_types) # p

    smiles_tuple_list = permutationDict(localStructuresDict)
    
    xyzDict, monitor_jobs = generateMolecules(smiles_tuple_list)
    '''
    
    resubmit_delay_min = 0.01 # 60 * 12
    resubmit_max_attempts = 40

    # geometry optimization options
    method_opt = "B3LYP"
    #method_opt = "HF"
    basis_set_opt = "6-311G(d,p)"
    #basis_set_opt = "6-31G"
    mem_com_opt = "1600"  # mb
    mem_pbs_opt = "10"  # gb

    # TD-DFT options
    method_mexc = "B3lYP"
    basis_set_mexc = "6-311G(d,p)"
    mem_com_mexc = "1600"  # mb
    mem_pbs_mexc = "10"  # gb"
    cluster='map' 

    # comment for testing
    #writeInputFiles(xyzDict, method_opt, basis_set_opt)
    print(os.getcwd())
    monitor_jobs = ['1ed_1b_1ea']

    #print(monitor_jobs)
    
    #complete = jobResubmit(monitor_jobs, resubmit_delay_min, resubmit_max_attempts,
    #                       method_opt, basis_set_opt, mem_com_opt, mem_pbs_opt,
    #                       method_mexc, basis_set_mexc, mem_com_mexc, mem_pbs_mexc,
    #                       cluster
    #                       )
    
    

main()

