import os
import json
import pandas as pd

def box0(x):
    red = {}
    name = []
    with open(x,"r") as read_file:
        data = json.load(read_file)
        #print(data["molecules"][1])
        for mol in data["molecules"]:
            #print(mol['name'])
            cam,pbe= 0,0
            camhomo,camlumo = 0,0
            pbehomo,pbelumo = 0,0
            for exc in mol["excitations"]:
                if exc['exc'] == 1:
                    if exc["method_basis_set"]=='CAM-B3LYP/6-311G(d,p)':
                        cam += exc['nm']
                        #print(cam)
                        camhomo += exc['HOMO']
                        camlumo += exc['LUMO']

                    if exc["method_basis_set"]=='PBE1PBE/6-311G(d,p)':
                        pbe += exc['nm']
                        pbehomo += exc['HOMO']
                        pbelumo += exc['LUMO'] 

            try:
                h = 6.626e-34
                c = 3e17
                Joules_to_eV = 1.602e-19
             #   print(cam)
                cam = 1239.8/cam
                #print(cam)
                pbe = 1239.8/pbe
                
                lsf =  cam * 1.3125 + pbe * -0.4746  # nm
               # print(lsf)
                lsf = 1239.8/lsf
           #     print(lsf)

                lsfhomo = camhomo*1.11663268 + pbehomo* -0.29145692# eV
                lsflumo = camlumo*-0.01785889 +pbelumo* 1.22883249 # eV )
                if lsf >=800 and lsf <= 1000 :
                    #'name,camexc,pbeexc,lsfexc,lsfhomo,lsflumo
                    name.append(mol['name'])
                    red[mol['name']]=(cam,pbe,lsf,lsfhomo,lsflumo)
            except ZeroDivisionError:
                pass
           #     print((mol['name'],'Excited states is zero in .json '))
    return red


def box1(x):
    red = {}
    name = []
    with open(x,"r") as read_file:
        data = json.load(read_file)
        #print(data["molecules"][1])
        for mol in data["molecules"]:
            #print(mol['name'])
            cam,pbe= 0,0
            camhomo,camlumo = 0,0
            pbehomo,pbelumo = 0,0
            for exc in mol["excitations"]:
                if exc['exc'] == 1:
                    if exc["method_basis_set"]=='CAM-B3LYP/6-311G(d,p)':
                        cam += exc['nm']
                        #print(cam)
                        camhomo += exc['HOMO']
                        camlumo += exc['LUMO']

                    if exc["method_basis_set"]=='PBE1PBE/6-311G(d,p)':
                        pbe += exc['nm']
                        pbehomo += exc['HOMO']
                        pbelumo += exc['LUMO'] 

            try:
                h = 6.626e-34
                c = 3e17
                Joules_to_eV = 1.602e-19
             #   print(cam)
                cam = 1239.8/cam
                #print(cam)
                pbe = 1239.8/pbe
                
                lsf =  cam * 1.3125 + pbe * -0.4746  # nm
               # print(lsf)
                lsf = 1239.8/lsf
           #     print(lsf)

                lsfhomo = camhomo*1.11663268 + pbehomo* -0.29145692# eV
                lsflumo = camlumo*-0.01785889 +pbelumo* 1.22883249 # eV )
                if lsf >=600 and lsf < 800 :
                    #'name,camexc,pbeexc,lsfexc,lsfhomo,lsflumo
                    name.append(mol['name'])
                    red[mol['name']]=(cam,pbe,lsf,lsfhomo,lsflumo)
            except ZeroDivisionError:
                pass
                        

    return red

def box2(x):
    red = {}
    name = []
    with open(x,"r") as read_file:
        data = json.load(read_file)
        #print(data["molecules"][1])
        for mol in data["molecules"]:
            #print(mol['name'])
            cam,pbe= 0,0
            camhomo,camlumo = 0,0
            pbehomo,pbelumo = 0,0
            for exc in mol["excitations"]:
                if exc['exc'] == 1:
                    if exc["method_basis_set"]=='CAM-B3LYP/6-311G(d,p)':
                        cam += exc['nm']
                        #print(cam)
                        camhomo += exc['HOMO']
                        camlumo += exc['LUMO']

                    if exc["method_basis_set"]=='PBE1PBE/6-311G(d,p)':
                        pbe += exc['nm']
                        pbehomo += exc['HOMO']
                        pbelumo += exc['LUMO'] 

            try:
                h = 6.626e-34
                c = 3e17
                Joules_to_eV = 1.602e-19
             #   print(cam)
                cam = 1239.8/cam
                #print(cam)
                pbe = 1239.8/pbe
                
                lsf =  cam * 1.3125 + pbe * -0.4746  # nm
               # print(lsf)
                lsf = 1239.8/lsf
           #     print(lsf)

                lsfhomo = camhomo*1.11663268 + pbehomo* -0.29145692# eV
                lsflumo = camlumo*-0.01785889 +pbelumo* 1.22883249 # eV )
                if lsf >=400 and lsf < 600 :
                    #'name,camexc,pbeexc,lsfexc,lsfhomo,lsflumo
                    name.append(mol['name'])
                    red[mol['name']]=(cam,pbe,lsf,lsfhomo,lsflumo)
            except ZeroDivisionError:
                pass

    return red



def ranker(homo,lumo,wavelength,name):
    rank_homo = sorted(homo.values())
    rank_lumo = sorted(lumo.values(),reverse=True)
    rank_wavelength = sorted(wavelength.values(),reverse=True)

    ranking_homo = {}
    for i in rank_homo:
        for x in name:
            if homo[x]==i:
                ranking_homo[x]=i
    ranking_lumo = {}
    for i in rank_lumo:
        for x in name:
            if lumo[x]==i:
                ranking_lumo[x]=i
    ranking_wavelength = {}
    for i in rank_wavelength:
        for x in name:
            if wavelength[x]==i:
                ranking_wavelength[x]=i
    
        
    df = {"HOMO Ranks":ranking_homo.keys()," HOMO Values":ranking_homo.values(),"LUMO Ranks":ranking_lumo.keys(),"LUMO Values":ranking_lumo.values(),"Wavelength Ranks":ranking_wavelength.keys(),"Wavelength Values":ranking_wavelength.values()}
    df = pd.DataFrame(df)
    
    



    return df


def main():
    os.chdir('../')
    filename = 'json_files/results_exc.json'
    #filename = 'Benchmark/benchmarks_exc.json'
    print('800-1000')
    print(' ')
    print(' ')
    wavelength = {}
    homo = {}
    lumo = {}
    names = []
   # for name in box0(filename).keys():
  #  for name in box1(filename).keys():
    for name in box2(filename).keys():
       # print(box2(filename)[name][3])
        '''
        wavelength[name]=box0(filename)[name][2] 
        homo[name]=box0(filename)[name][3] 
        lumo[name]=box0(filename)[name][4]
        names.append(name)
        '''
        

     #   print(box1(filename)[name][3]) 
        
        '''        
        print(name) 
        wavelength[name]=box1(filename)[name][2] 
        homo[name]=box1(filename)[name][3] 
        lumo[name]=box1(filename)[name][4]
        names.append(name)
        '''
        
        
        
        
        print(box2(filename)[name][0]) 
        wavelength[name]=box2(filename)[name][2] 
        homo[name]=box2(filename)[name][3] 
        lumo[name]=box2(filename)[name][4] 
        names.append(name)
        
        
        
    """
    
   # print(' ')
    best_homo = min(homo.values())
    worst_homo = max(homo.values())
    #print(best_homo)
    best_lumo = max(lumo.values())
    worst_lumo = min(lumo.values())
    best_wavelength = max(wavelength.values())
    worst_wavelength = min(wavelength.values())
    '''
    for key in names:
        if homo[key]== best_homo:
            print(('BEST HOMO',key,best_homo,homo[key],lumo[key],wavelength[key]))
        if homo[key] == worst_homo:
            print(('Worst HOMO',key,worst_homo,homo[key],lumo[key],wavelength[key]))
        if lumo[key]==best_lumo:
            print(('BEST LUMO',key,best_lumo,homo[key],lumo[key],wavelength[key]))
        if lumo[key]==worst_lumo:
            print(('Worst LUMO',key,worst_lumo,homo[key],lumo[key],wavelength[key]))

        if wavelength[key]==best_wavelength:
            print(('BEST Wavelength',key,best_wavelength,homo[key],lumo[key],wavelength[key]))
        if wavelength[key] == worst_wavelength:
            print(('WORST wavelength',key,worst_wavelength,homo[key],lumo[key],wavelength[key]))

    '''
    """
    df = ranker(homo,lumo,wavelength,names)
    print(df)
    df.to_csv("Top400.csv",index=False)

   



    
    #print(homo)
    print(' ')
    """
    print(box1(filename))
    print(' ')
    print('600-800')
    print(' ')
    print(box2(filename))
    print(' ')
    print('400-600')
    print(' ')
    """
    return
main()