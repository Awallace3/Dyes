import os
import glob
import molecule_json

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

def absorpt(path, method_mexc, basis_set_mexc):
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
                print("JOB INCOMPLETE")
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
        for n,x in enumerate(data2):
                #print(x)
                if x[0] == 'Excited':
                        #print(x)
                        mol = molecule_json.Excitation()
                        mol.setExc(int(x[2][0]))
                        mol.setNm(float(x[6]))
                        mol.setOsci(float(x[8][2:]))
                        orbitalList = []
                        mol.setMethod_basis_set("%s/%s" % (method_mexc, basis_set_mexc))
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
                                excitations.append(mol)
                elif n == len(data2):
                        mol.setOrbital_Numbers(orbitalList)
                        excitations.append(mol)
        return excitations
