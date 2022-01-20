import json
import os
import glob
import itertools
import subprocess
import time
import sys
from operator import add, sub
import numpy as np
from error_mexc_dyes_v2 import make_input_files_no_constraints
from error_mexc_dyes_v2 import gaussianInputFiles
import absorpt
import molecule_json
sys.path.insert(1,'..')
from final import collectLocalStructures
from final import permutationDict
from final import generateMolecules
from final import jobResubmit_v2

def user(x,y):
    filename = open(x+'/'+"user",'w+')
    filename.write(y)
    filename.close()
    return

def combiner(data):
    three_types = data["generateMolecules"]["three_types"]
    banned = data["generateMolecules"]["banned"]
    
    localStructuresDict = collectLocalStructures(three_types,banned)
    smiles_tuple_list = permutationDict(localStructuresDict)
    print("smiles_tuple_list", smiles_tuple_list)
    monitor_jobs = generateMolecules(smiles_tuple_list, 
                                data["generateMolecules"]["method_opt"],
                                data["generateMolecules"]["basis_set_opt"],
                                data["generateMolecules"]["mem_com_opt"],
                                data["generateMolecules"]["mem_pbs_opt"],
                                data["generateMolecules"]["cluster"])                       
    return

def optimization(data):
    if data["geomopt"]["enable"]=="True":
        for name in data["geomopt"]["dyeoptlist"]:
            filename = open(name+'/mex.out','r')
            data2 = filename.readlines()
            total2 = []
            startgeom = []
            endgeom = []
            for num,line3 in enumerate(data2):
                zcoord = data2[num][33:]
                #print(zcoord)
                if 'Standard orientation' in line3:
                    startgeom.append(num)
                if '---------------------------------------------------------------------' in line3:
                    endgeom.append(num)

            xyzcoords = data2[startgeom[-1]+5:endgeom[-1]]       
            for i in xyzcoords:
                a = i.replace('  0  ',' ')
                atom = a[10:20]
                xcoord = a[30:45]
                ycoord = a[43:56]
                zcoord = a[57:67]
                total = atom + '   ' +  str(xcoord) +'   ' +  str(ycoord) + '   ' + str(zcoord)
                total2.append(total)
            filename2 = open('tmp.txt','w+')
            for xyz in total2:
                filename2.write(xyz)
            filename2.close()
            gaussianInputFiles(
            name,
            data["geomopt"]["method_opt"], 
            data["geomopt"]["basis_set_opt"],
            data["geomopt"]["mem_com_opt"],
            data["geomopt"]["mem_pbs_opt"],
            data["geomopt"]["cluster"],
            baseName='mex',
            procedure='OPT',
            data='',
            dir_name=name,
            solvent='',
            outName='mexc_o')
            os.chdir(name)
            ans = data["geomopt"]["submit"]
            ans = ans.lower() 
            if ans=="yes" :
                os.system('qsub mex.pbs')
                os.chdir(data["path"]["path_to_results"])
            else:
                os.chdir(data["path"]["path_to_results"])                   
    return
            
def add_methods(data):
    return data["add_methods"]

def resubmit(method,x):
    jobResubmit_v2(
        data["excitation"]["dyeList"],
        data["excitation"]["resubmit_delay_min"], 
        data["excitation"]["resubmit_max_attempts"],
        data["excitation"]["method_opt"],
        data["excitation"]["basis_set_opt"],
        data["excitation"]["mem_com_opt"],
        data["excitation"]["mem_pbs_opt"],
        data["excitation"]["method_mexc"], 
        data["excitation"]["basis_set_mexc"], 
        data["excitation"]["mem_com_mexc"], 
        data["excitation"][ "mem_pbs_mexc"],
        data["excitation"][ "cluster"], 
        data["path"]["results"],
        method,
        data["excitation"]["max_queue"], 
        data["excitation"]["results_json"]
        )


    return         

def main():
    filename = "inputs.json"
    with open(str(filename),"r") as read_file:
        data = json.load(read_file)
        user(data["path"]["path_to_final"],data["user"]["user"])

        ans2 = data["generateMolecules"]["enable"]
        ans2= ans2.lower() 
        if ans2=="true":
            os.chdir(data["path"]["path_to_final"])
            combiner(data)
        ans3 = data["geomopt"]["enable"]
        ans3 = ans3.lower()
        if ans3=="true":
            os.chdir(data["path"]["path_to_results"])
            optimization(data)
        ans4 = data['excitation']['enable']
        ans4=ans4.lower()
        if ans4=='true':
            os.chdir(data['path']['path_to_final'])
            add_methods_1 = add_methods(data) 
            print(add_methods_1)
            resubmit(add_methods_1,data)
    return
main()
