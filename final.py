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
    #print(post_perm)        
    
    return post_perm

def generateMolecules (smiles_tuple_list): 

    #print(number_locals)
    #print(smiles_tuple_list)
    xyzDict = {}


    for num, i in enumerate(smiles_tuple_list):
        first, second, third = i
        first = first.replace("1", "7")
        first = first.replace("2", "6")
        second = second.replace("1", "5")
        second = second.replace("2", "4")
        line = first + "." + second + "." + third
        #print(line)
        #print(num)
        line = line.replace("BBA", "9")
        line = line.replace("BBD", "8")
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
        for n, i in enumerate(carts[0]):
            if n > 1:
                carts_cleaned.append(i)
            #print(i)
        del carts_cleaned[-1]
        xyzDict["geom{0}".format(num+1)] = carts_cleaned
        print('loop')
    print(xyzDict)
    return xyzDict

def writeFiles (xyzDict):
    for key, value in xyzDict.items():
        file = open("inputs/" + key, 'w+')
        for line in value:
            file.write(line)
            file.write("\n")
        file.close()
    return


def main():
    print("\n\tstart\n")
    three_types = ["eDonors", "backbones", "eAcceptors"] # Name of subdirectories holding the local structures

    localStructuresDict = collectLocalStructures(three_types) # p

    smiles_tuple_list = permutationDict(localStructuresDict)

    xyzDict = generateMolecules(smiles_tuple_list)

    writeFiles(xyzDict)
main()