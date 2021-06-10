import os
import glob
import subprocess

def ES_extraction(path):
    occupied = 'Alpha  occ. eigenvalues --'
    virtual = 'Alpha virt. eigenvalues --'
    occLst = []
    virtLst = []
    with open(path, 'r') as fp:
        lines = fp.readlines()
    #print(lines)
    for i in lines:
        if occupied in i:
            occLst.append(i)
        if virtual in i:
            virtLst.append(i)
    if len(occLst) == 0 and len(virtLst) == 0:
        print("ES_extraction error: Found no data in %s" % path)
        return 0, 0
    occLst = occLst[-1].split('  ')
    virtLst = virtLst[0].split('  ')
    
    occVal = float(occLst[-1].replace('\n', "").replace(" ", ""))
    virtVal = float(virtLst[1].replace(" ", ''))

    # converted to eV and abs val
    occVal = abs(occVal*27.211385)
    virtVal = abs(virtVal*27.211385)

    occVal = occVal -4.2 
    virtVal = virtVal -3.9
    #print('scaling:',occVal, virtVal)
    return occVal, virtVal
#ES_extraction('../ES/ES.out')