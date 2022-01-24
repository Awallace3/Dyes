import json
import os
import glob
import itertools
import subprocess
import time
import sys
from operator import add, sub
import numpy as np

from error_mexc_dyes_v3 import gaussianpbsFiles 
from error_mexc_dyes_v3 import gaussianInputFiles
import absorpt
import molecule_json
sys.path.insert(1,'..')
from final import smilesRingCleanUp
from final import add_qsub_dir
from final import collectLocalStructures
from final import permutationDict
from final import generateMolecules
from final import jobResubmit_v2

def user(x,y):
    filename = open(x+'/'+"user",'w+')
    filename.write(y)
    filename.close()
    return

def combiner(method,data):
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
    jobResubmit_v2(
        monitor_jobs,
        data["generateMolecules"]["resubmit_delay_min"],
        data["generateMolecules"]["resubmit_max_attempts"],
        data["generateMolecules"]["method_opt"],
        data["generateMolecules"]["basis_set_opt"],
        data["generateMolecules"]["mem_com_opt"],
        data["generateMolecules"]["mem_pbs_opt"],
        data["excitation"]["method_mexc"],
        data["excitation"]["basis_set_mexc"],
        data["excitation"]["mem_com_mexc"],
        data["excitation"][ "mem_pbs_mexc"],
        data["generateMolecules"][ "cluster"],
        data["path"]["path_to_results"],
        method,
        data["generateMolecules"]["max_queue"],
        data["generateMolecules"]["results_json"]) 

    return
def pbs(data):
    for name in data["geomopt"]["dyeoptlist"]:
        if data["geomopt"]["procedure"]=='opt':
            gaussianpbsFiles( data["geomopt"]["method_opt"],
                data["geomopt"]["basis_set_opt"],data["geomopt"]["mem_com_opt"],
                data["geomopt"]["mem_pbs_opt"],data["geomopt"]["cluster"],name,baseName='mex', outName='mexc_o')


        if data["geomopt"]["procedure"]=='exc':
            gaussianpbsFiles( data["geomopt"]["method_opt"],
                data["geomopt"]["basis_set_opt"],data["geomopt"]["mem_com_opt"],
                data["geomopt"]["mem_pbs_opt"],data["geomopt"]["cluster"],name,baseName='mexc', outName='mexc_o') 
        os.chdir(data["path"]["path_to_results"])
    return

def opt(data):
    for name in data["geomopt"]["dyeoptlist"]:
        if data["geomopt"]["procedure"]=='opt':
            gaussianInputFiles(data["geomopt"]["method_opt"],
                           data["geomopt"]["basis_set_opt"], 
                           data["geomopt"]["mem_com_opt"], 
                           data["geomopt"]["mem_pbs_opt"], 
                           data["geomopt"]["cluster"],
                           baseName='mex', 
                           procedure='OPT',
                           data='', 
                           dir_name=name, 
                           solvent=data["geomopt"]["solvent"],
                           outName='mexc_o'
                            )
        os.chdir(data['path']["path_to_results"])
    return   






            
def add_methods(data):
    return data["add_methods"]

def resubmit(method,data):
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
        data["path"]["path_to_results"],
        method,
        data["excitation"]["max_queue"], 
        data["excitation"]["results_json"]
        )


    return         



def qsuber(data):
    os.chdir(data["path"]["path_to_results"])
    for name in data["geomopt"]["dyeoptlist"]:
        os.chdir(name)
        os.system('qsub mex.pbs')
        os.chdir('..')
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
            add_methods_1 = add_methods(data) 
            combiner(add_methods_1,data)
        ans3 = data["geomopt"]["enable"]
        ans3 = ans3.lower()
        if ans3=="true":
            os.chdir(data["path"]["path_to_results"])
            pbs(data)
            opt(data)
            if data["geomopt"]["submit"]=="no":
                qsuber(data)

        ans4 = data['excitation']['enable']
        ans4=ans4.lower()
        if ans4=='true':
            os.chdir(data['path']['path_to_final'])
            add_methods_1 = add_methods(data) 
            print(add_methods_1)
            resubmit(add_methods_1,data)
        ans5 = data['error']["enable"]
        ans5=ans5.lower()
        if ans5=='true':
            error_reader()

        
    return
main()
