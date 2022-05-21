from ast import Index
import os
import json
import pandas as pd
import numpy as np
import pdfkit
import subprocess
import sys

def smiles_json(file):
    a = open(file)
    data = json.load(a)
    df = {
        'Name':[],
        'SMILES':[]
    }
    for i in data['molecules']:
        df['Name'].append(i['name'])
        df['SMILES'].append(i['generalSMILES'])
    df = pd.DataFrame(df)
    df.to_csv('../data_analysis/dotsmiles.csv',index=False)



    return df

def conv_dot_to_gen_smiles(file):
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

 







    return

def main():
    '''
    reads json file to make a csv of the general SMILES strings for paper 
    '''
    file_json = '../json_files/results_ds5.json'
    file_csv = '../data_analysis/SMILES_DICT.csv'
    smiles_json(file_json)
    conv_dot_to_gen_smiles(file_csv)
    return
main()