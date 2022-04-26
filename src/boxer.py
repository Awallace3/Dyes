import os
import json
import pandas as pd
from homo_lumo_boxer_csv import *

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
                    if 'TPA' in mol['name']:
                        pass
                    else:
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
    
        
    df = {"LUMO Ranks":ranking_lumo.keys(),"LUMO Values":ranking_lumo.values(),
    "HOMO Ranks":ranking_homo.keys()," HOMO Values":ranking_homo.values(),
    "Wavelength Ranks":ranking_wavelength.keys(),"Wavelength Values":ranking_wavelength.values()}
    df = pd.DataFrame(df)
    
    



    return df


def main():
    os.chdir('../')
    filename = 'json_files/results_exc.json'
    #filename = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/json_files/benchmarks_exc.json'
    print('Start')
    print(' ')
    print(' ')
    wavelength = {}
    homo = {}
    lumo = {}
    names = []
#    wavelength_range = '800-1000'
#    wavelength_range = '600-800'
    wavelength_range = '400-600'
    if wavelength_range == '800-1000':
        for name in box0(filename).keys():
            if 'TPA' in name:
                pass
            else:
                print(name)
                wavelength[name]=box0(filename)[name][2] 
                homo[name]=box0(filename)[name][3] 
                lumo[name]=box0(filename)[name][4]
                names.append(name)
    if wavelength_range == '600-800':
        for name in box1(filename).keys():
            if 'TPA' in name:
                pass
            else:
                print(name)
                wavelength[name]=box1(filename)[name][2] 
                homo[name]=box1(filename)[name][3] 
                lumo[name]=box1(filename)[name][4]
                names.append(name)
    if wavelength_range == '400-600':
        for name in box2(filename).keys():
            if 'TPA' in name:
                pass
            else:
                wavelength[name]=box2(filename)[name][2] 
                homo[name]=box2(filename)[name][3] 
                lumo[name]=box2(filename)[name][4] 
                names.append(name)


        
    if wavelength_range == '800-1000':
        df = ranker(homo,lumo,wavelength,names)
        df.to_csv('data_analysis/800_1000.csv',index=False)
        file = 'data_analysis/800_1000.csv'
        numbs = HOMO_LUMO_dict(file)
        optimal_list = []
        for name in numbs.keys():
            optimal_list.append(name)
            filename = open('data_analysis/test.csv', 'w+')
        for i in optimal_list:
            print(i)
            a = str(i) + ',' + str(round(numbs[i][1], 2)) + ',' + str(
            round(numbs[i][0], 2)) + ',' + str(round(numbs[i][2], 2))
            filename.write(str(a) + '\n')
        filename.close()
        scatter_plot('data_analysis/test.csv')





    if wavelength_range == '600-800':
        df = ranker(homo,lumo,wavelength,names)
        df.to_csv("data_analysis/600_800.csv",index=False)
        file = 'data_analysis/600_800.csv'
        numbs = HOMO_LUMO_dict(file)
        optimal_list = []
        for name in numbs.keys():
            optimal_list.append(name)
            filename = open('data_analysis/test.csv', 'w+')
        for i in optimal_list:
            print(i)
            a = str(i) + ',' + str(round(numbs[i][1], 2)) + ',' + str(
            round(numbs[i][0], 2)) + ',' + str(round(numbs[i][2], 2))
            filename.write(str(a) + '\n')
        filename.close()
        scatter_plot('data_analysis/test.csv')



    if wavelength_range == '400-600':
        df = ranker(homo,lumo,wavelength,names)
        df.to_csv("data_analysis/400_600.csv",index=False)
        file = 'data_analysis/400_600.csv'
        numbs = HOMO_LUMO_dict(file)
        optimal_list = []
        for name in numbs.keys():
            optimal_list.append(name)
            filename = open('data_analysis/test.csv', 'w+')
        for i in optimal_list:
            print(i)
            a = str(i) + ',' + str(round(numbs[i][1], 2)) + ',' + str(
            round(numbs[i][0], 2)) + ',' + str(round(numbs[i][2], 2))
            filename.write(str(a) + '\n')
        print(optimal_list)
        filename.close()
        scatter_plot('data_analysis/test.csv')

    


    '''
    name = ['AP11','AP14','AP16','AP17','AP25','AP3','C218','JD21','JW1','ND1','ND2','ND3','NL11','NL12','NL13','NL2','NL4','NL5','NL7','NL6','ZL003','XY1','R6']
    '''
    '''
    df = {
        'Name':[],
        'HOMO':[],
        'LUMO':[],
        'Wave':[]
    }
    #print(homo.keys())

    for i in names:
        print(i)
        df['Name'].append(i)
        df['HOMO'].append(homo[i])
        df['LUMO'].append(lumo[i])
       # print(lumo[i])
        df['Wave'].append(wavelength[i])
    
    

    
    df = pd.DataFrame(df)
    df.to_csv("Top400.csv",index=False)
    '''

   




    return
if __name__ == '__main__':
    main()
