import os
import glob
# import molecule_json
from .molecule_json import Excitation, Excitation_exc
from . import molecule_json
from .ES_extraction import ES_extraction
# from .ES_extraction import ES_extraction
# from .molecule_json import Excitation, Excitation_exc


def cleanLine(line):
    aList = []
    cropped_line = line.rstrip()
    for i in range(2, 10):
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


def absorpt(path,
            method_mexc,
            basis_set_mexc,
            solvent='',
            exc_json=False,
            states=3):
    filename = open(path, 'r')

    num = 0

    nregion = False
    excitedState = " Excited State   "
    data = []
    excitedStatenum = 0
    jobComplete = False

    for n, j in enumerate(filename):
        if 'Normal termination' in j:
            jobComplete = True
    if not jobComplete:
        print("JOB INCOMPLETE", path)
        return []
    filename.close()
    with open(path, 'r') as fp:
        lines = fp.readlines()
    for n, i in enumerate(lines):
        if ' Excitation energies and oscillator strengths:' in i:
            nregion = True
        if nregion:
            if excitedState in i:
                excitedStatenum += 1
                if excitedStatenum > states:
                    break
            if "SavETr:" in i:
                print('breaking')
                break
            data.append(i)

    data = data[2:]
    data2 = []
    for n, i in enumerate(data):
        i = i.replace('->', ' ').replace('<-', ' ')
        x = cleanLine(i)
        if x == []:
            continue
        data2.append(x)
    excitations = []
    occVal, virtVal = ES_extraction(path)
    if occVal == 0 and 0 == virtVal:
        print(path, occVal, virtVal)
    for n, x in enumerate(data2):
        if x[0] == 'Excited':
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
                mol.setMethod_basis_set("%s/%s" %
                                        (method_mexc, basis_set_mexc))
            else:
                mol.setMethod_basis_set(
                    "%s/%s_%s" %
                    (method_mexc, basis_set_mexc, clean_solvent(solvent)))

        else:
            if x[0] != 'This' and x[0] != 'Total' and x[0] != 'Copying':
                orbitalList.append(int(x[0]))
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
