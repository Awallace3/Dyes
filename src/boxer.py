import os
import json
import pandas as pd
from homo_lumo_boxer_csv import *

def box0(x):
    red = {}
    name = []
    with open(x,"r") as read_file:
        data = json.load(read_file)
        for mol in data["molecules"]:
            for exc in mol["lsf"]:
                if exc['exc']==1:
                    if exc['nm']>=800:
                        name.append(mol['name'])
                        #print(exc['nm'])
                        red[mol['name']] =  (exc['nm'],exc['HOMO'],exc['LUMO'])
    print(len(name))
    print(red)

            

 
    return red


def box1(x):
    red = {}
    name = []
    with open(x,"r") as read_file:
        data = json.load(read_file)
        for mol in data["molecules"]:
            for exc in mol["lsf"]:
                if exc['exc']==1:
                    if exc['nm']>=600 and exc['nm']<800:
                        name.append(mol['name'])
                        #print(exc['nm'])
                        red[mol['name']] =  (exc['nm'],exc['HOMO'],exc['LUMO'])
    print(len(name))
    print(red)

 
                        

    return red

def box2(x):
    red = {}
    name = []
    with open(x,"r") as read_file:
        data = json.load(read_file)
        for mol in data["molecules"]:
            for exc in mol["lsf"]:
                if exc['exc']==1:
                    if exc['nm']>=400 and exc['nm']<600:
                        name.append(mol['name'])
                        #print(exc['nm'])
                        red[mol['name']] =  (exc['nm'],exc['HOMO'],exc['LUMO'])
    print(len(name))
    print(red)
            
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
    print(df)
    
    



    return df


def main():
    os.chdir('../')
    filename = 'json_files/results_exc.json'
    filename = 'json_files/test2.json'
    #filename = '/Users/tsantaloci/Desktop/python_projects/austin/Dyes/json_files/benchmarks_exc.json'
    print('Start')
    print(' ')
    print(' ')
    wavelength = {}
    homo = {}
    lumo = {}
    red = {}
    names = []
#    wavelength_range = '800-1000'
    wavelength_range = '600-800'
#    wavelength_range = '400-600'
    
    if wavelength_range == '800-1000':
        red = box0(filename)
    #    print(names[0])
    #print(red)
        for name in red.keys():
            if 'TPA' in name:
                name 
            else:
                names.append(name)
                wavelength[name]=red[name][0]
                lumo[name]=red[name][1]
                homo[name]=red[name][2]
    #    ranker(homo,lumo,wavelength,names)
    if wavelength_range == '600-800':
        red = box1(filename)
    #    print(names[0])
    #print(red)
        for name in red.keys():
            if 'TPA' in name:
                name 
            else:
                names.append(name)
                wavelength[name]=red[name][0]
                lumo[name]=red[name][1]
                homo[name]=red[name][2]
    #    ranker(homo,lumo,wavelength,names)
    

    if wavelength_range == '400-600':
        red = box2(filename)
    #    print(names[0])
    #print(red)
        for name in red.keys():
            if 'TPA' in name:
                name 
            else:
                names.append(name)
                wavelength[name]=red[name][0]
                lumo[name]=red[name][1]
                homo[name]=red[name][2]
      #  ranker(homo,lumo,wavelength,names)
     

       
        




    #ranker(homo,lumo,wavelength,names)
    print('The amount of dyes in the region')
    print(len(red))


            
    if wavelength_range == '800-1000':
        df = ranker(homo,lumo,wavelength,names)
        df.to_csv('data_analysis/800_1000.csv',index=False)
        file = 'data_analysis/800_1000.csv'
        numbs = HOMO_LUMO_dict(file)
        #print(numbs)
        optimal_list = []
        for name in numbs.keys():
            if numbs[name][0]>=-3.75:
                optimal_list.append(name)
        filename = open('data_analysis/g_800_1000.csv', 'w+')
        for i in optimal_list:
    
            #print(i)
            a = str(i) + ',' + str(round(numbs[i][1], 2)) + ',' + str(
            round(numbs[i][0], 2)) + ',' + str(round(numbs[i][2], 2))
            filename.write(str(a) + '\n')
        filename.close()
      #  print(optimal_list)
        print('amount of optimal dyes ')
        print(len(optimal_list))
        scatter_plot('data_analysis/g_800_1000.csv')
    



    

    if wavelength_range == '600-800':
        df = ranker(homo,lumo,wavelength,names)
        df.to_csv('data_analysis/600_800.csv',index=False)
        file = 'data_analysis/600_800.csv'
        numbs = HOMO_LUMO_dict(file)
        #print(numbs)
        optimal_list = []
        for name in numbs.keys():
            if numbs[name][0]>=-3.75:
                optimal_list.append(name)
        filename = open('data_analysis/g_600_800.csv', 'w+')
        for i in optimal_list:
    
            #print(i)
            a = str(i) + ',' + str(round(numbs[i][1], 2)) + ',' + str(
            round(numbs[i][0], 2)) + ',' + str(round(numbs[i][2], 2))
            filename.write(str(a) + '\n')
        filename.close()
      #  print(optimal_list)
        print('amount of optimal dyes ')
        print(len(optimal_list))
        scatter_plot('data_analysis/g_600_800.csv')
   


    '''
    if wavelength_range == '400-600':
        df = ranker(homo,lumo,wavelength,names)
        df.to_csv("data_analysis/400_600.csv",index=False)
        file = 'data_analysis/400_600.csv'
        numbs = HOMO_LUMO_dict(file)
        optimal_list = []
        for name in numbs.keys():
            optimal_list.append(name)
            filename = open('data_analysis/g_400_600.csv', 'w+')
        for i in optimal_list:
            print(i)
            a = str(i) + ',' + str(round(numbs[i][1], 2)) + ',' + str(
            round(numbs[i][0], 2)) + ',' + str(round(numbs[i][2], 2))
            filename.write(str(a) + '\n')
        print(optimal_list)
        filename.close()
        scatter_plot('data_analysis/g_400_600.csv')
    '''

    


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
