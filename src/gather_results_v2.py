import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from homo_lumo import *

def cam_dict(data,num):
    method = "CAM-B3LYP/6-311G(d,p)" 
    camexc = {}
    for name in data["molecules"][num]["excitations"]:
        if name["exc"] == 1:
            if name["method_basis_set"] == "CAM-B3LYP/6-311G(d,p)" :
                camexc[data["molecules"][num]["name"]]=name["nm"] 
    return camexc




def bhandhlyp_dict(data,num):
    bhandhlyp = {}
    for name in data["molecules"][num]["excitations"]:
        if name["exc"] == 1:
            if name["method_basis_set"] == "bhandhlyp/6-311G(d,p)":
                bhandhlyp[data["molecules"][num]["name"]]=name["nm"] 
    return bhandhlyp


def pbe_dict(data,num):
     
    pbe = {}
    for name in data["molecules"][num]["excitations"]:
        if name["exc"] == 1:
            if name["method_basis_set"] == "PBE1PBE/6-311G(d,p)":
                #print(name)
                pbe[data["molecules"][num]["name"]]=name["nm"] 
    return pbe

def exp_dict(data,num):
    exp = {}
    nm = data["molecules"][num]['exp']
    name = data["molecules"][num]['name'] 
    exp[name]=nm
    #print(exp)

    return exp

def main():
    filename = open('../Benchmark/benchmarks_exc.json')
    data = json.load(filename)
    method = ["CAM-B3LYP/6-311G(d,p)","bhandhlyp/6-311G(d,p)","PBE1PBE/6-311G(d,p)"]
    cam = {}
    bhandlyp = {}
    pbe = {}
    exp = {}
    
    
        
    for num,name in enumerate(data["molecules"]):
        exp.update(exp_dict(data,num))
        for meth in method:
            if meth == "CAM-B3LYP/6-311G(d,p)":
                cam.update(cam_dict(data,num))
            if meth == "bhandhlyp/6-311G(d,p)" :
                bhandlyp.update(bhandhlyp_dict(data,num))
            if meth == "PBE1PBE/6-311G(d,p)":
                pbe.update(pbe_dict(data,num)) 
    print(exp)
    
   

            
 

    return
main()