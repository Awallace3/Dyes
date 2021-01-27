import numpy as np
import os
import itertools
import glob
import subprocess
# requires obabel installed...
    # brew install obabel


""" 
def permutationDictOG (BB_lst, ED_lst, EA_lst ):


    a = np.zeros((1,4))
    b = np.zeros((2,4))
    c = np.zeros((3,4))
    d = np.zeros((4,4))
    e = np.zeros((5,4))
    f = np.zeros((6,4))
    g = np.zeros((7,4))



    #print(g)
    testing with lists...
    backbone_lst = [ [[0, 0, 0, 0], [0,0,0,0]] ,[[1,1,1,1], [1,1,1,1]], [[2,2,2,2], [2,2,2,2]],[[3,3,3,3],[3,3,3,3]] ]               # 3
    electron_acceptor_lst = [ [[4,4,4,4], [4,4,4,4]] ]      # 4
    electron_donor_lst = [ [[5,5,5,5], [5,5,5,5]],[[6,6,6,6], [6,6,6,6]] ]         # 6

    backbone_lst = [ a, b, c ]
    electron_acceptor_lst = [ d, e]
    electron_donor_lst = [f, g]

    s = [backbone_lst] + [electron_acceptor_lst] + [electron_donor_lst]

    k = list(itertools.product(*s)) # produces permutation, but may want configurations instead
    permutation_num = len(k) 

    print(permutation_num) 

    geom_dict = {}

    for num, i in enumerate(k):
        # if you want each array still seperated uncomment line 34...
        #geom_dict['geom{0}'.format(num+1)] = [i]
        # if you want to arrays concatenated use the lines 36,37, and 38...
        first, second, third = i
        combined = np.concatenate((first, second, third))
        geom_dict['geom{0}'.format(num+1)] = [combined]
        
    first_molecule = geom_dict['geom1'][0]
    print(first_molecule)

""" 

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
    
    return localStructuresDict, number_locals

def permutationDict(localStructuresDict):

    pre_perm = []

    for key, value in localStructuresDict.items():
        pre_perm = pre_perm + [value]

    post_perm = list(itertools.product(*pre_perm))
    #print(post_perm)        
    
    return post_perm

def generateMolecules (smiles_tuple_list, number_locals): 

    #print(number_locals)
    #print(smiles_tuple_list)
    for num, i in enumerate(smiles_tuple_list):
        first, second, third = i
        line = first + "." + second + "." + third
        print(line)
        print(num)
        file = open('results/smiles{0}.smi'.format(num+1), 'w+')
        file.write(line)
        file.close()
        cmd = "obabel -ismi smiles{0}.smi -oxyz output.xyz --gen3D".format(num+1)
        subprocess.call(cmd, shell=True)
        #with open('smiles{0}.smi'.format(num+1)):
        #    f.write(line)
        #*y = i
        #print(y)

    return

def main():
    print("\n\tstart\n")
    three_types = ["eDonors", "backbones", "eAcceptors"] # Name of subdirectories holding the local structures

    localStructuresDict, number_locals = collectLocalStructures(three_types)
    #print(localStructuresDict)                

    smiles_tuple_list = permutationDict(localStructuresDict)

    generateMolecules(smiles_tuple_list, number_locals)

    #out_files = glob.glob(".out")
main()