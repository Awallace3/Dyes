import numpy as np
import os
import itertools
import glob
import subprocess
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
                smiles = smiles.rstrip()
                localStructuresDict['local{0}'.format(num+1)].append(smiles)
        os.chdir("..")
        number_locals += 1
    #print(localStructuresDict)
    
    return localStructuresDict

def permutationDict(localStructuresDict):

    pre_perm = []

    for key, value in localStructuresDict.items():
        pre_perm = pre_perm + [value]

    post_perm = list(itertools.product(*pre_perm))
    print(post_perm)        
    
    return post_perm

def smilesRingCleanUp(f, s, t):
    combinedString = ''
    current_val = 0
    lst1 = []
    claimed = []
    double = []

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

    
    print(lst1)
    print(claimed)

    return combinedString


def generateMolecules (smiles_tuple_list): 
    
    #print(number_locals)
    #print(smiles_tuple_list)
    xyzDict = {}


    for num, i in enumerate(smiles_tuple_list):
        #if num > 1:
        #    return xyzDict
        first, second, third = i
        #combinedString = smilesRingCleanUp(first, second, third)
        first = first.replace("1", "7")
        first = first.replace("2", "6")
        second = second.replace("1", "5")
        second = second.replace("2", "4")
        line = first + "." + second + "." + third
        #print(line)
        #print(num)
        print("line{0}:".format(num), line)
        line = line.replace("BBA", "9")
        line = line.replace("BBD", "8")
        print("line{0}:".format(num), line)
        file = open('results/smiles{0}.smi'.format(num+1), 'w+')
        file.write(line)
        file.close()
        
        #cmd = "obabel -ismi results/smiles{0}.smi -oxyz output.xyz --gen3D".format(num+1)
        cmd = "obabel -ismi results/smiles{0}.smi -oxyz --gen3D".format(num+1)
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
        xyzDict["geom{0}".format(num+1)] = carts_cleaned
        print('loop')
    #print(xyzDict)
    return xyzDict

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

def writeInputFiles (xyzDict):
    os.chdir("inputs")
    for key, value in xyzDict.items():
        os.mkdir(key)
        file = open( key + "/" + "mex"+".com", 'w+')
        file.write("#N B3LYP/6-311G(d,p) OPT  \n")
        file.write("\n")
        file.write("Name\n\n")
        file.write("0 1\n")
        for line in value:
            file.write(line)
            file.write("\n")
        file.close()
        file = open( key + "/" + "mex" + ".pbs", 'w+')   #pbs for sequoia
        file.write("#!/bin/sh")
        file.write("\n")
        file.write("#PBS -N " + "mex")
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
        file.write("/usr/local/apps/bin/g09setup " + "mex" + '.com ' + "mex" + '.out ')




        file.close()
        """
        file = open( key + "/" + "mex" + ".pbs", 'w+') # pbs for maple
        file.write("#!/bin/sh")
        file.write("\n")
        file.write("#PBS -N mex")
        file.write("\n")
        file.write("#PBS -S /bin/sh")
        file.write("\n")
        file.write("#PBS -j oe")
        file.write("\n")
        file.write("#PBS -m abe")
        file.write("\n")
        file.write("#PBS -l mem=10gb")
        file.write("\n")
        file.write("#PBS -l nodes=1:ppn=1")
        file.write("\n")
        file.write("")
        file.write("\n")
        file.write("export g16root=/usr/local/apps/")
        file.write("\n")
        file.write("")
        file.write("scrdir=/tmp/bnp.$PBS_JOBID")
        file.write("\n")
        file.write("")
        file.write("\n")
        file.write("mkdir -p $scrdir")
        file.write("\n")
        file.write("export GAUSS_SCRDIR=$scrdir")
        file.write("\n")
        file.write("export OMP_NUM_THREADS=1")
        file.write("\n")
        file.write("")
        file.write("\n")
        file.write("printf 'exec_host = '")
        file.write("\n")
        file.write("head -n 1 $PBS_NODEFILE")
        file.write("\n")
        file.write("")
        file.write("\n")
        file.write("cd $PBS_O_WORKDIR")
        file.write("\n")
        file.write("g16 " + "mex" + ".com " + "mex" + ".out ")






        file.close()
        """
          
    return

def make_opt_files():
    """ Combines the geometry output and the constrained output. Then makes the .com and .pbs files in a subdirectory """

    data = ""

    with open('tmp.txt') as fp:
        data = fp.read()

    # Reading data from file2
    charges = "0 1"

    new_dir = "mexc"
    os.mkdir(new_dir)

    with open(new_dir + '/mexc.com', 'w') as fp:
        fp.write("%mem=1600mb\n")
        fp.write("%nprocs=4\n")
        fp.write("#N TD(NStates=25) B3lYP/6-311G(d,p)\n")
        fp.write("\n")
        fp.write("Name ModRedundant - Minimalist working constrained optimisation\n")
        fp.write("\n")
        fp.write(charges + "\n")
        fp.write(data)
        fp.write("\n")

    with open(new_dir + '/mexc.pbs', 'w') as fp:
        fp.write("#!/bin/sh\n")
        fp.write("#PBS -N mexc\n#PBS -S /bin/bash\n#PBS -j oe\n#PBS -m abe\n#PBS -l")
        fp.write("mem=15gb\n")
        fp.write(
            "#PBS -l nodes=1:ppn=4\n#PBS -q gpu\n\nscrdir=/tmp/$USER.$PBS_JOBID\n\n")
        fp.write(
            "mkdir -p $scrdir\nexport GAUSS_SCRDIR=$scrdir\nexport OMP_NUM_THREADS=1\n\n")
        fp.write(
            """echo "exec_host = $HOSTNAME"\n\nif [[ $HOSTNAME =~ cn([0-9]{3}) ]];\n""")
        fp.write("then\n")
        fp.write(
            "  nodenum=${BASH_REMATCH[1]};\n  nodenum=$((10#$nodenum));\n  echo $nodenum\n\n")
        fp.write(
            """  if (( $nodenum <= 29 ))\n  then\n    echo "Using AVX version";\n""")
        fp.write(
            "    export g16root=/usr/local/apps/gaussian/g16-b01-avx/\n  elif (( $nodenum > 29 ))\n")
        fp.write("""  then\n    echo "Using AVX2 version";\n    export g16root=/usr/local/apps/gaussian/g16-b01-avx2/\n  else\n""")
        fp.write("""    echo "Unexpected condition!"\n    exit 1;\n  fi\nelse\n""")
        fp.write("""  echo "Not on a compute node!"\n  exit 1;\nfi\n\n""")
        fp.write(
            "cd $PBS_O_WORKDIR\n. $g16root/g16/bsd/g16.profile\ng16 mexc.com mexc.out\n\nrm -r $scrdir\n")

def main():
    print("\n\tstart\n")
    three_types = ["eDonors", "backbones", "eAcceptors"] # Name of subdirectories holding the local structures

    localStructuresDict = collectLocalStructures(three_types) # p

    smiles_tuple_list = permutationDict(localStructuresDict)

    xyzDict = generateMolecules(smiles_tuple_list)

    writeInputFiles(xyzDict)
    
main()