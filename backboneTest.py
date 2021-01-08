import numpy as np
import os
import itertools

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