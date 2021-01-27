import numpy as np
import os
import itertools
import glob




def permutationDictOG (BB_lst, ED_lst, EA_lst ):


    a = np.zeros((1,4))
    b = np.zeros((2,4))
    c = np.zeros((3,4))
    d = np.zeros((4,4))
    e = np.zeros((5,4))
    f = np.zeros((6,4))
    g = np.zeros((7,4))



    #print(g)
    """ 
    testing with lists...
    backbone_lst = [ [[0, 0, 0, 0], [0,0,0,0]] ,[[1,1,1,1], [1,1,1,1]], [[2,2,2,2], [2,2,2,2]],[[3,3,3,3],[3,3,3,3]] ]               # 3
    electron_acceptor_lst = [ [[4,4,4,4], [4,4,4,4]] ]      # 4
    electron_donor_lst = [ [[5,5,5,5], [5,5,5,5]],[[6,6,6,6], [6,6,6,6]] ]         # 6 """

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

def collectLocalStructures (subdirectories):
    localStructuresDict = {}

    
    for num, i in enumerate(subdirectories):
        os.chdir(i)
        localStructuresDict['local{0}'.format(num+1)] = []
        localSmiles = glob.glob('*.smi')
        for j in localSmiles:
            with open(j) as f:
                smiles = f.read()
                localStructuresDict['local{0}'.format(num+1)].append(smiles)
        os.chdir("..")
    print(localStructuresDict)
    
    return localStructuresDict

def permutationDict(localStructuresDict):

    pre_perm = []

    for key, value in localStructuresDict.items():
        pre_perm = pre_perm + [value]
 #       #pre_perm.append(value)
  #      print(key, '-', value)
   #     for i in value:

#            with open(i) as f:
 #               smiles = f.read()

#
    post_perm = list(itertools.product(*))
    print(pre_perm)        

    #post_perm = list(itertools.product(*pre_perm))
    #print(post_perm)
    
    
    
    return 

def main():

    three_types = ["eDonors", "backbones", "eAcceptors"] # Name of subdirectories holding the local structures

    localStructuresDict = collectLocalStructures(three_types)
    #print(localStructuresDict)                

    permutationDict(localStructuresDict)

    #out_files = glob.glob(".out")

main()