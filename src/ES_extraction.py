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
    
    for i in range(2,10):
        k = ' ' * i
        occLst[-1] = occLst[-1].replace(k, " ")
        virtLst[0] = occLst[0].replace(k, ' ')
    occLst = occLst[-1].split(' ')
    virtLst = virtLst[0].split(' ')
    
    #print(occLst, virtLst)
    #print(occLst[-1].replace('\n', ""), virtLst[5].replace(" ", ''))
    
    occVal = float(occLst[-1].replace('\n', "").replace(" ", ""))
    #virtVal = float(virtLst[5].replace(" ", ''))
    for i in virtLst:
        i = i.replace(" ", '')
        #print(i)
        try:
            i = float(i)
            virtVal = i
            break
        except:
            continue
        
    #print('virtVal', type(virtVal), virtVal)

    # converted to eV and abs val
    occVal = abs(occVal*27.211385)
    virtVal = abs(virtVal*27.211385)

    occVal = occVal -4.2 
    virtVal = virtVal -3.9
    #print('scaling:',occVal, virtVal)
    return occVal, virtVal
#ES_extraction('../ES/ES.out')

if __name__ == "__main__":
    ES_extraction()