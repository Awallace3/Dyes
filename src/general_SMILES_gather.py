from ast import Index
import os
import json
import pandas as pd
import numpy as np
import subprocess
import sys

def dataset_json(file,name):
    '''
    reads dataset json file and gathers the general SMILES strings
    '''
    a = open(file)
    data = json.load(a)
    df = {
        'Name':[],
        'SMILES':[]
    }
    for i in data['molecules']:
        #print(i['name'])
        #for nam in name: 
        df['Name'].append(i['name'])
        df['SMILES'].append(i['SMILES'])
    df = pd.DataFrame(df)
    df.to_csv('../data_analysis/dotsmiles.csv',index=False)
    a.close()



    return df

def conv_dot_to_gen_smiles(file):
    '''
    reads a csv file that has the name of theoretical dye as index 1 and a dot formatted SMILES string as index 2. The function converts the dot SMILES string to Cartesian coordinates and then changes the Cartesian coordinates to general SMILES strings and inputs them into a csv.
    '''
    filename = open(file,'r')
    data = filename.readlines()
    dic = {}
    for line in data:
        #print(line)
        line = line.split(',')
        dic[line[0]]=line[1]
  #  for name in dic.keys():
    name2 = ['1ed_1b_1ea','1ed_1b_2ea']
    df = {
        'Name':[],
        'SMILE':[]
    }
    for name in dic.keys(): 
   # for name in name2:
        print(name)
        cmd = "obabel -:" + "'" +str(dic[name]).replace('\n','') +"'" + " -oxyz --gen3D -O "+'../smiles/'+ str(name) + ".xyz"
      #  print(cmd)
        os.system(cmd)
        filename2 = open('../smiles/'+str(name)+'.smi','w')
        #filename.close()
        cmd = "obabel -ixyz " + "'"+ '../smiles/'+str(name)+'.xyz' +"'"+ " -osmi" + ' ../smiles/' + str(name)+'.smi -as'
        os.system(cmd)
        carts = subprocess.check_output(cmd, shell=True).decode(sys.stdout.encoding).strip()
        carts = str(carts).replace('test.xyz','').replace('\t','')
        df['Name'].append(name)
        df['SMILE'].append(carts)
    df = pd.DataFrame(df)
    df.to_csv('../data_analysis/gensmiles.csv',index=False)

    print(df)
    filename.close()

    return

def list_to_name(file):
    '''
    gathers a list of specfic names of theoretical dyes from an custom made csv file. the custom made csv file just needs the name to be the first index
    '''
    name = []
    filename = open(file,'r')
    data = filename.readlines()
    for line in data:
        line = line.split(',')
        name.append(line[0])
    filename.close()
    return name

def specific_SMILES_to_df(dic,names):
    '''
    looks for specific smiles strings from the csv file that the conv_dot_to_gen_smiles function
    '''
    filename = open(dic,'r')
    data = filename.readlines()
    name_dict = {}
    for line in data:
       # print(line)
        line=line.split(',')
        name_dict[line[0]]=line[1]
    
    smiles = []
    for name in names:
        name_dict[name]
    print(len(smiles))

    filename.close()

    

    return

def smile_json(json1,name_list):
    a = open(json1)
    data = json.load(a)
    final = {}
    #print(data)


    for i in data:
        for x in name_list:
            if i == x:
                final[i]=data[i]
    '''
    lll = []
    for name in name_list:
        name=name.replace('\n','')
        lll.append(name)
    for i in lll:
        print(data[i])
    '''
    '''
    for i in data:
        type(i)
    '''
    #    for name in name_list:
    #        print(name)
        #    print(data[name])
    '''
    for name in name_list:
        print(data[name])
    '''


    return final


def conv_dot_to_gen_smiles_dict(dic):
    '''
    reads a dictionary that has the name of theoretical dye as key and a dot formatted SMILES string as value. The function converts the dot SMILES string to Cartesian coordinates and then changes the Cartesian coordinates to general SMILES strings and inputs them into a csv.
    '''
   
  #  for name in dic.keys():
    
    df = {
        'Name':[],
        'SMILE':[]
    }
    for name in dic.keys(): 
   # for name in name2:
        print(name)
        cmd = "obabel -:" + "'" +str(dic[name]).replace('\n','') +"'" + " -oxyz --gen3D -O "+'../smiles/'+ str(name) + ".xyz"
      #  print(cmd)
        os.system(cmd)
        filename2 = open('../smiles/'+str(name)+'.smi','w')
        #filename.close()
        cmd = "obabel -ixyz " + "'"+ '../smiles/'+str(name)+'.xyz' +"'"+ " -osmi" + ' ../smiles/' + str(name)+'.smi -as'
        os.system(cmd)
        carts = subprocess.check_output(cmd, shell=True).decode(sys.stdout.encoding).strip()
        carts = str(carts).replace('test.xyz','').replace('\t','')
        df['Name'].append(name)
        df['SMILE'].append(carts)
    df = pd.DataFrame(df)
    df.to_csv('../data_analysis/gensmiles_upt.csv',index=False)

    print(df)
    

    return

def helper(file):
    new = {}
    with open(file,'r') as fp:
        data = fp.readlines()
        for line in data[1:]:
            if line == '\n':
                pass
            else:
                line=line.split('../smiles')
                new[line[0]]=line[1]
    
    with open(file,'w') as fp:
        fp.write('Name,SMILES\n')
        for name in new.keys():
            fp.write(name+','+new[name])
    


    return


def main():
    '''
    reads json file to make a csv of the general SMILES strings for paper 
    '''
    data_json = '../json_files/results_ds5.json'
    file_csv = '../data_analysis/SMILES_DICT.csv'
    file_name = '../data_analysis/Absorption_test.csv'
    smiles_json = '../json_files/smiles.json'

    total_SMILES_dict = '../data_analysis/Total_SMILES_str.csv'
   # conv_dot_to_gen_smiles(file_csv)
    
    name_list = list_to_name(file_name)
    spec = smile_json(smiles_json,name_list)
    conv_dot_to_gen_smiles_dict(spec)
    
    #helper('../data_analysis/gensmiles.csv')

   # specific_SMILES_to_df(total_SMILES_dict,name_list)
   # dataset_json(data_json,name_list)

    return
main()