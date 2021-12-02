import os
import pandas as pd
import numpy as np

def grepper(name):
    cmd = 'grep -A1 ' + "'Alpha  occ. eigenvalues' " + str(name) +  '/mex.out' + '>' + str(name)+  '/' + 'orbs.out'
    #print(cmd)
    os.system(cmd)


    return

def LUMO(name):
    filename = open(str(name)+ '/' + 'orbs.out','r')
    data = filename.readlines()
    lll = data[-1].split(' ')
    #print(lll)
    if lll[7] == '':
     # print(lll[8])
      LUMO = float(lll[8])*27.2114
    else:
      LUMO = float(lll[7])*27.2114
   # LUMO = abs(LUMO)-3.9
    #print((name,'LUMO',method,LUMO))
  #  for i in filename:
  #      print(i)



    return [name,'LUMO',str(LUMO)]

def HOMO(name):
    filename = open(str(name)+ '/' + 'orbs.out','r')
    data = filename.readlines()
    print(data[-2])
  #  print(lll)
    lll = data[-2].split(' ')
    #print(lll)
    HOMO = float(lll[-1])*27.2114
  #  HOMO = abs(HOMO)-4.2
    #print((name,'HOMO',method,HOMO))

    return [name,'HOMO',str(HOMO)] 

def pandass(HOMO,LUMO):
    hom = np.array(HOMO)
    lum = np.array(LUMO)

    
    #print(HOMO)
    df =  pd.DataFrame(hom,columns=['Name','Type','Energy (eV)'])
    print(df)
    df_2 = pd.DataFrame(lum,columns=['Name','Type','Energy (eV)']) 
    print(df_2)
    HOMOenerg = []
    HOMOname = []
    LUMOname = []
    LUMOenerg = []
    for i in HOMO:
      HOMOname.append(i[0])
      HOMOenerg.append(round(float(i[2]),4))
    for x in LUMO:
      LUMOname.append(x[0])
      LUMOenerg.append(round(float(x[2]),4))

    d = {'Name':HOMOname,'HOMO': HOMOenerg,'LUMO:':LUMOenerg}
    df_3 = pd.DataFrame(data=d)
    df_3.to_csv('data.csv',index=False)




    return

def Main():
    path_to_files = '../DFTpieces/eAcceptor/'
    path_to_files = '../DFTpieces/eDonor/'
    path_to_files = '../DFTpieces/Backbone/'
    os.chdir(path_to_files)
    #name = ['NL2','AP25','JW1','R4']
    # method = ['mexc','mexc_dichloromethane','pbe1pbe','pbe1pbe_dichloromethane']
    # name =  ['DQ5', 'S-DAHTDTT', 'NKX-2883', 'S3', 'HKK-BTZ4', 'TPA-T-TTAR-A', 'NL7', 'NL8', 'AP3', 'NL11', 'C271',  'IQ4', 'WS-55', 'SGT-130', 'FNE52', 'IQ21', 'SGT-136', 'D-DAHTDTT', 'R6', 'TPA-TTAR-A', 'T-DAHTDTT', 'TH304', 'NL4', 'C258', 'TTAR-9', 'SGT-121', 'TTAR-15', 'NL2', 'SGT-129', 'FNE32', 'BTD-1', 'Y123', 'C272', 'FNE34', 'IQ6', 'TP1', 'TTAR-B8', 'R4', 'TPA-T-TTAR-T-A','ZL003','WS-6','NL4','NL6','JW1','AP25']
   # methods = ['mexc', 'pbe1pbe','bhandlyp']
    name = ['10ea','11ea','1ea','2ea','3ea','4ea','5ea','6ea','7ea','8ea','9ea']   
    name = ['10ed','11ed','12ed','1ed','2ed','3ed','5ed','6ed','7ed','9ed']
    ## Full backbone list ##
    name = ['4b', '1b', '32b', '3b', '24b', '27b', '22b', '2b', '14b', '17b', '12b', '9b', '31b', '34b', '8b', '26b', '21b', '29b', '7b', '16b', '11b', '19b', '35b', '30b', '33b', '6b', '25b', '20b', '23b', '5b', '15b', '10b', '18b', '13b']

    name = ['4b', '1b', '32b', '3b', '24b',  '22b', '2b', '14b', '17b', '12b', '9b', '31b', '34b', '8b',  '21b', '29b', '7b', '16b', '11b', '19b', '35b', '30b', '33b', '6b', '25b', '20b', '23b', '5b', '15b', '10b', '18b', '13b']
   # method = ['mexc','mexc_dichloromethane',]

    HOMO_1 = []
    LUMO_1 = []
    for bench in name:
      #  for meth in methods:
        print(bench)
        grepper(bench)
        HOMO_1.append(HOMO(bench))
        LUMO_1.append(LUMO(bench))
    pandass(HOMO_1,LUMO_1)

    return    
Main()
