import os
import glob
import molecule_json
from molecule_json import Excitation, Excitation_exc
from ES_extraction import ES_extraction

def cleanLine(line):
    aList = []
    cropped_line = line.rstrip()
    for i in range(2,10):
        k = ' ' * i
        cropped_line = cropped_line.replace(k, " ")
    cropped_line = cropped_line.split(" ")
    
    for i in cropped_line:
        if i == '':
            continue
        else: 
            aList.append(i)
    return aList

def clean_solvent(solvent):
        return solvent.replace('-', '').replace(',', '')

def absorpt(path, method_mexc, basis_set_mexc, solvent='', exc_json=False):
        filename = open(path,'r')
        
        num = 0
        
        nregion = False
        excitedState = " Excited State   "
        data = []
        excitedStatenum = 0
        jobComplete = False 
        for n, j in enumerate(filename):
                if 'Normal termination' in j:
                        jobComplete = True
        if jobComplete == False:

                print("JOB INCOMPLETE", path)
                return []
        filename.close()
        with open(path, 'r') as fp:
                lines = fp.readlines()
        for n, i in enumerate(lines):
                if ' Excitation energies and oscillator strengths:' in i:
                        nregion = True
                        num = n
                if nregion:
                        if excitedState in i:
                                excitedStatenum += 1
                                if excitedStatenum >= 4:
                                        break
                        data.append(i)
                        
        data = data[2:]
        data2 = []
        for n,i in enumerate(data):
                # new line
                i = i.replace('->', ' ')
                #
                x = cleanLine(i)
                if x == []:
                        continue
                data2.append(x)
        
        #print(data2)
        excitations = []
        occVal, virtVal = ES_extraction(path)
        if occVal == 0 and 0 == virtVal:
                print(path, occVal, virtVal)
        for n,x in enumerate(data2):
                #print(x)
                if x[0] == 'Excited':
                        #print(x)
                        if exc_json:
                                mol = Excitation_exc()
                                mol.setHOMO(occVal)
                                mol.setLUMO(virtVal)
                        else:
                                mol = molecule_json.Excitation()
                                print('reg')
                        mol.setExc(int(x[2][0]))
                        mol.setNm(float(x[6]))
                        mol.setOsci(float(x[8][2:]))
                        orbitalList = []
                        if solvent == '':
                                mol.setMethod_basis_set("%s/%s" % (method_mexc, basis_set_mexc))
                        else: 
                                mol.setMethod_basis_set("%s/%s_%s" % (method_mexc, basis_set_mexc, clean_solvent(solvent)))

                else:
                        if x[0] != 'This' and x[0] != 'Total' and x[0] != 'Copying':
                                orbitalList.append(int(x[0]))
                                # line swapped after replacing -> with wb
                                #orbitalList.append(int(x[1][2:]))
                                orbitalList.append(int(x[1]))
                                orbitalList.append(float(x[2]))
                if n < len(data2):
                        if x[0] == 'Excited':
                                mol.setOrbital_Numbers(orbitalList)
                                excitations.append(mol.toDict())
                elif n == len(data2):
                        mol.setOrbital_Numbers(orbitalList)
                        excitations.append(mol.toDict())
        
        
        return excitations
