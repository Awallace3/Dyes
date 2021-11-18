import os
import pandas as pd
import numpy as np

def grepper(name,method):
    cmd = 'grep -A1 ' + "'Alpha  occ. eigenvalues' " + str(name) + '/' + str(method) + '/mexc.out' + '>' + str(name)+ '/' + str(method)+ '/' + 'orbs.out'
    #print(cmd)
    os.system(cmd)


    return

def LUMO(name,method):
    filename = open(str(name)+ '/' + str(method)+ '/' + 'orbs.out','r')
    data = filename.readlines()
    lll = data[-1].split(' ')
   #  print(lll)
    LUMO = float(lll[7])*27.2114
   # LUMO = abs(LUMO)-3.9
    #print((name,'LUMO',method,LUMO))
  #  for i in filename:
  #      print(i)



    return [name,'LUMO',method,str(LUMO)]

def HOMO(name,method):
    filename = open(str(name)+ '/' + str(method)+ '/' + 'orbs.out','r')
    data = filename.readlines()
  #  print(data[-2])
    lll = data[-2].split(' ')
    #print(lll)
    HOMO = float(lll[-1])*27.2114
  #  HOMO = abs(HOMO)-4.2
    #print((name,'HOMO',method,HOMO))


    return [name,'HOMO',method,str(HOMO)] 

def pandass(HOMO,LUMO):
    hom = np.array(HOMO)
    lum = np.array(LUMO)

    
    #print(HOMO)
    df =  pd.DataFrame(hom,columns=['Name','Type','Method','Energy (eV)'])
    print(df)
    df_2 = pd.DataFrame(lum,columns=['Name','Type','Method','Energy (eV)']) 
    print(df_2)




    return

def Main():
    path_to_files = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/testing_results'
    path_to_files = '/Users/tsantaloci/Desktop/writingpapers/Dye_Paper/dyes_method_paper/MOdyes'
    path_to_files = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/Benchmark/results'
    os.chdir(path_to_files)
#    name = ['ZL003','AP25','NL4','XY1','AP3']
    name = ['AP25','AP3','NL4','XY1','ZL003']
    name = ['R6']
    #method = ['mexc','mexc_dichloromethane','pbe1pbe','pbe1pbe_dichloromethane']
    #name =  ['DQ5', 'S-DAHTDTT', 'NKX-2883', 'S3', 'HKK-BTZ4', 'TPA-T-TTAR-A', 'NL7', 'NL8', 'AP3', 'NL11', 'C271',  'IQ4', 'WS-55', 'SGT-130', 'FNE52', 'IQ21', 'SGT-136', 'D-DAHTDTT', 'R6', 'TPA-TTAR-A', 'T-DAHTDTT', 'TH304', 'NL4', 'C258', 'TTAR-9', 'SGT-121', 'TTAR-15', 'NL2', 'SGT-129', 'FNE32', 'BTD-1', 'Y123', 'C272', 'FNE34', 'IQ6', 'TP1', 'TTAR-B8', 'R4', 'TPA-T-TTAR-T-A','ZL003','WS-6','NL4','NL6','JW1','AP25']
#    name = ['5ed_16b_4ea','7ed_16b_5ea','6ed_16b_4ea','6ed_16b_5ea','1ed_16b_4ea']
    method = ['mexc']
    #method = ['bhandhlyp']
#    method = ['pbe1pbe']
   # method = ['mexc','mexc_dichloromethane',]
    HOMO_1 = []
    LUMO_1 = []
    for bench in name:
        for meth in method:
            grepper(bench,meth)
            HOMO_1.append(HOMO(bench,meth))
            LUMO_1.append(LUMO(bench,meth))
    pandass(HOMO_1,LUMO_1)






    return    
Main()
